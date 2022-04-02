import base64
import logging
import smtplib
import ssl
from socket import socket, AF_INET, SOCK_STREAM

from utils import define_content_type, prepare_message

logger = logging.getLogger(__name__)


class EmailSender:
    def __init__(
        self,
        msg_path: str,
        from_addr: str,
        password: str,
        to_addr: str,
        host: str,
        port: int = 465,
        by_sockets: bool = False,
    ):
        content_type = define_content_type(msg_path)
        self._msg = prepare_message(msg_path, content_type, from_addr, to_addr)
        self._from_addr = from_addr
        self._to_addr = to_addr
        self._password = password
        self._host = host
        self._port = port
        self._bufsize = 1024
        self._by_sockets = by_sockets

    def _send_by_smtplib(self):
        smtp = smtplib.SMTP_SSL(host=self._host, port=self._port)
        smtp.ehlo()
        smtp.login(self._from_addr, self._password)

        logger.info('Logged successfully!')

        smtp.sendmail(self._from_addr, [self._to_addr], self._msg)
        smtp.close()

        logger.info('Message successfully sent!')

    def _socket_send(self, client_socket, encoded_msg):
        client_socket.send(encoded_msg)
        recv = client_socket.recv(self._bufsize).decode()
        logger.info(recv)

        return recv

    def _send_by_sockets(self):
        bufsize = 1024

        mailserver = ('smtp.mail.ru', self._port)

        client_socket = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))
        client_socket.connect(mailserver)
        recv = client_socket.recv(bufsize).decode()
        logger.info(recv)

        if recv[:3] != '220':
            logger.warning('220 reply not received from server.')

        cmd = 'HELO Name\r\n'.encode()
        recv = self._socket_send(client_socket, cmd)

        if recv[:3] != '250':
            logger.info('250 reply not received from server.')

        base64_str = ('\x00' + self._from_addr + '\x00' + self._password).encode()
        base64_str = base64.b64encode(base64_str)
        cmd = 'AUTH PLAIN '.encode() + base64_str + '\r\n'.encode()
        self._socket_send(client_socket, cmd)

        cmd = ('MAIL FROM: ' + self._from_addr + '\r\n').encode()
        self._socket_send(client_socket, cmd)

        cmd = ('RCPT TO: ' + self._to_addr + '\r\n').encode()
        self._socket_send(client_socket, cmd)

        cmd = 'DATA\r\n'.encode()
        self._socket_send(client_socket, cmd)

        self._socket_send(client_socket, self._msg + '\r\n.\r\n'.encode())

        cmd = 'QUIT\r\n'.encode()
        self._socket_send(client_socket, cmd)

        client_socket.close()

    def send_email(self):
        if self._by_sockets:
            self._send_by_sockets()
        else:
            self._send_by_smtplib()
