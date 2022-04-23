import netifaces as ni


if __name__ == '__main__':
    info = ni.ifaddresses('wlp0s20f3')[ni.AF_INET][0]
    print(f'Addr: {info["addr"]}')
    print(f'Netmask: {info["netmask"]}')
