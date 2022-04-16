from _socket import IPPROTO_UDP, SOL_SOCKET, SO_REUSEADDR, timeout
from random import randint
from socket import socket, AF_INET, SOCK_DGRAM


def calc_checksum(data: bytes, base: int = 16) -> int:
    data_size = len(data)
    chunks_count = data_size // base + (data_size % base != 0)
    checksum = 0

    for i in range(chunks_count):
        chunk = data[i * base:min((i + 1) * base, data_size)]
        n = int.from_bytes(chunk, 'big')
        checksum += n
        checksum %= 2 ** base

    return 2 ** base - 1 - checksum


def check_checksum(data: bytes, base: int = 16) -> bool:
    return calc_checksum(data, base) == 0


class StopAndWaitSocket:
    def __init__(self, addr: str, port: int):
        self._socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.bind((addr, port))

        self._num = 0
        self._PKTSIZE = 256
        self._BUFSIZE = 512
        self._BASE = 16
        self._pkts = set()

    def connect(self, addr: str, port: int) -> None:
        self._addr = (addr, port)

    def set_timeout(self, time_limit: float):
        self._socket.settimeout(time_limit)

    def _pack_msg(self, msg: bytes, num: int) -> bytes:
        msg_ = bytes([num]) + msg
        return calc_checksum(msg_, self._BASE).to_bytes(self._BASE, 'big') + msg_

    def recv(self) -> bytes:
        print(f'Pkt{self._num} waiting.')

        while True:
            try:
                raw_msg, addr = self._socket.recvfrom(self._BUFSIZE)

                if randint(0, 3) == 0:
                    raise timeout()
            except timeout:
                print(f'Time limit exceeded. Continue waiting pkt{self._num}...')
                continue

            if len(raw_msg) < self._BASE + 1:
                print(f'Wrong data length. Continue waiting pkt{self._num}...')
                continue

            if not check_checksum(raw_msg, self._BASE):
                print(f'Wrong checksum. Continue waiting pkt{self._num}...')
                continue

            num = raw_msg[self._BASE]

            if addr != self._addr:
                print(f'Pkt{num} received. Wrong addr. Continue waiting pkt{self._num}...')
                continue

            if num != self._num:
                if raw_msg in self._pkts:
                    print(f'Pkt{num} duplicate received. Continue waiting pkt{self._num}...')
                    self._socket.sendto(self._pack_msg(bytes(), num), addr)
                else:
                    print(f'Pkt{num} received. Wrong number. Continue waiting pkt{self._num}...')
                continue

            self._socket.sendto(self._pack_msg(bytes(), num), addr)
            self._num ^= 1
            self._pkts.add(raw_msg)

            print(f'Pkt{num} successfully received.\n')

            return raw_msg[self._BASE + 1:]

    def send(self, msg: bytes) -> None:
        print(f'Pkt{self._num} sending...')

        while True:
            self._socket.sendto(self._pack_msg(msg, self._num), self._addr)

            try:
                raw_msg, rcvd_addr = self._socket.recvfrom(self._BUFSIZE)

                if randint(0, 3) == 0:
                    raise timeout()
            except timeout:
                print(f'Time limit exceeded. Resending pkt{self._num}...')
                continue

            if len(raw_msg) < self._BASE + 1:
                print(f'Wrong data length. Resending pkt{self._num}...')
                continue

            if not check_checksum(raw_msg, self._BASE):
                print(f'Wrong checksum. Resending pkt{self._num}...')
                continue

            if rcvd_addr != self._addr:
                print(f'Pkt from wrong address received. Resending pkt{self._num}...')
                continue

            num = raw_msg[self._BASE]

            if num != self._num:
                print(f'ACK with wrong number received. Resending pkt{self._num}...')
                continue

            break

        self._num ^= 1

        print(f'ACK{self._num} has received. Pkt{self._num} sent successfully.\n')

    def sendall(self, msg: bytes) -> None:
        msg_size = len(msg)
        pkt_count = msg_size // self._PKTSIZE + (msg_size % self._PKTSIZE != 0)

        for i in range(pkt_count):
            chunk = msg[i * self._PKTSIZE:min((i + 1) * self._PKTSIZE, msg_size)]
            self.send(chunk)

        self._num = 0
        self._pkts.clear()

        print(f'Data sent successfully\n')

    def recvall(self) -> bytes:
        msg = bytes()

        while True:
            chunk = self.recv()

            msg += chunk

            if len(chunk) < self._PKTSIZE:
                break

        print(f'Data received successfully\n')

        self._num = 0
        self._pkts.clear()

        return msg
