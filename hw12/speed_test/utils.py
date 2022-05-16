import datetime
import random
import socket

from constants import PKT_SIZE


def gen_pkt(size: int) -> str:
    data = ''

    for _ in range(size):
        data += str(random.randint(0, 9))

    return data


class Receiver:
    def __init__(self, server_socket, sock_type: str = 'UDP'):
        self.server_socket = server_socket
        self.sock_type = sock_type
        self.common_time: float = 0
        self.total_bytes_count: int = 0
        self.total_pkt_num: int = 0
        self.pkt_num: int = 0
        self.speed = -1

    def receive_pkt_num(self) -> None:
        if self.sock_type == 'UDP':
            raw_msg, _ = self.server_socket.recvfrom(PKT_SIZE)

            print(f'Pkt num received')

            msg = raw_msg.decode()

            self.total_pkt_num = int(msg)
        else:
            raw_msg = self.server_socket.recv(4)

            self.total_pkt_num = int.from_bytes(raw_msg, byteorder='big')

    def receive_pkt(self) -> None:
        try:
            if self.sock_type == 'UDP':
                raw_msg, _ = self.server_socket.recvfrom(PKT_SIZE)
            else:
                raw_msg = self.server_socket.recv(PKT_SIZE)

            print(f'Pkt #{self.pkt_num + 1} received')

            msg = raw_msg.decode()

            start_time_str, _ = msg.split()
            start_time = float(start_time_str)

            cur_time = datetime.datetime.now().timestamp()

            self.total_bytes_count += len(raw_msg)
            self.pkt_num += 1
            self.common_time += cur_time - start_time
        except socket.timeout:
            return

    def receive_all(self):
        self.receive_pkt_num()

        for _ in range(self.total_pkt_num):
            self.receive_pkt()

    def calc_speed(self):
        self.speed = round(self.total_bytes_count / self.common_time, 3)
