import random
import time
from _socket import SO_REUSEADDR
from socket import (
    SOCK_DGRAM, AF_INET, socket, IPPROTO_UDP, SOL_SOCKET,
)

from constants import SERVER_ADDR, SERVER_PORT, BUFSIZE


if __name__ == '__main__':
    server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((SERVER_ADDR, SERVER_PORT))

    while True:
        raw_msg, addr = server_socket.recvfrom(BUFSIZE)

        if random.randint(0, 5) == 0:
            continue

        time.sleep(random.uniform(0.005, 0.5))

        msg = raw_msg.decode().upper()
        server_socket.sendto(msg.encode(), addr)

        print(msg)
