import logging
import time
from _socket import SO_REUSEADDR
from datetime import datetime
from socket import (
    SOCK_DGRAM, AF_INET, socket, IPPROTO_UDP, SOL_SOCKET, SO_BROADCAST,
)

logger = logging.getLogger(__name__)


def udp_br_client(hostaddr: str, port: int):
    bufsize = 1024
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    client_socket.bind((hostaddr, port))

    while True:
        msg, _ = client_socket.recvfrom(bufsize)
        logger.info(f'Time: {msg.decode()}')


def udp_br_server(hostaddr: str, port: int):
    server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    while True:
        curtime = datetime.now().strftime("%H:%M:%S").encode()
        server_socket.sendto(curtime, (hostaddr, port))
        logger.info(curtime)
        time.sleep(1)
