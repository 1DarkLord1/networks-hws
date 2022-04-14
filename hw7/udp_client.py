import datetime
from _socket import SO_REUSEADDR, timeout
from dataclasses import dataclass
from math import inf
from socket import (
    SOCK_DGRAM, AF_INET, socket, SOL_SOCKET,
)

from constants import BUFSIZE, SERVER_ADDR, SERVER_PORT


@dataclass
class StatCollector:
    rtt_min: float = inf
    rtt_max: float = 0
    rtt_sum: float = 0
    total_pkts: int = 0
    rcvd_pkts: int = 0

    def add(self, rtt: float):
        self.rtt_min = min(rtt, self.rtt_min)
        self.rtt_max = max(rtt, self.rtt_max)
        self.rtt_sum += rtt

        self.total_pkts += 1
        self.rcvd_pkts += 1

    def lost(self):
        self.total_pkts += 1

    def print_stat(self):
        loss_ratio = round((self.total_pkts - self.rcvd_pkts) / self.total_pkts * 100, 2)
        rtt_avg = self.rtt_sum / self.rcvd_pkts

        print(
            f'{self.total_pkts} packets transmitted, {self.rcvd_pkts} packets received, {loss_ratio}% packet loss'
        )
        print(
            f'rtt min/avg/max = {self.rtt_min * 1000:.3f}/{rtt_avg * 1000:.3f}/{self.rtt_max * 1000:.3f} ms\n'
        )


def extract_time(msg: str) -> datetime:
    chunks = msg.split()
    return datetime.datetime.strptime(f'{chunks[2]} {chunks[3]}', '%Y-%m-%d %H:%M:%S.%f')


if __name__ == '__main__':
    collector = StatCollector()

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    client_socket.settimeout(1)

    for i in range(10):
        client_socket.sendto(
            f'Ping {i + 1} {datetime.datetime.now()}'.encode(),
            (SERVER_ADDR, SERVER_PORT)
        )

        try:
            raw_msg, _ = client_socket.recvfrom(BUFSIZE)
        except timeout:
            collector.lost()
            print('Request timed out\n')
            continue

        msg = raw_msg.decode()

        print(msg)

        end = datetime.datetime.now()
        start = extract_time(msg)

        rtt = (end - start).total_seconds()

        collector.add(rtt)

        collector.print_stat()

        # print(f'RTT: {rtt}s\n')
