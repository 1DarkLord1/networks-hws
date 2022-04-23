import socket
import sys


def port_is_free(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free = sock.connect_ex((host, port))
    sock.close()

    return free == 0


if __name__ == '__main__':
    """ Input format: python 3 ports.py <addr> <port lower value> <port upper value> """

    addr = sys.argv[1]
    portl = int(sys.argv[2])
    portr = int(sys.argv[3])

    print(f'Free ports:')

    for port in range(portl, portr):
        if port_is_free(addr, port):
            print(port)
