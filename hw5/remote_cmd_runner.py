import logging

from socket import (
    socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR,
)
from subprocess import call

logger = logging.getLogger(__name__)


def receive_data(conn):
    bufsize = 1024
    msg = bytes()

    while True:
        chunk = conn.recv(bufsize)
        msg += chunk

        if len(chunk) < bufsize:
            break

    return msg.decode()


def handle_conn(conn):
    msg = receive_data(conn)
    res = call(msg, shell=True)
    conn.send(str(res).encode())
    conn.close()


def cmd_runner_server(hostaddr: str, port: int):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((hostaddr, port))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()
        logger.info(f'Connected with client: {addr}')
        handle_conn(conn)


def cmd_runner_client(hostaddr: str, port: int, cmd: str):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    client_socket.connect((hostaddr, port))
    client_socket.sendall(cmd.encode())

    answer = receive_data(client_socket)
    logger.info(f'Return code: {answer}')
    client_socket.close()
