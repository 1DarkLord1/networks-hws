import netifaces as ni


if __name__ == '__main__':
    for interface in ni.interfaces():
        print(interface)

        info = ni.ifaddresses(interface)[ni.AF_INET][0]

        print(f'Addr: {info["addr"]}')
        print(f'Netmask: {info["netmask"]}\n')
