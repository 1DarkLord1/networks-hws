# 3. Определение всех компьютеров в сети (6 баллов)


import socket

import PySimpleGUI as sg
import scapy.all as sc

IP = '192.168.1.7'
NETWORK_IP = '192.168.1.0'
MAC = 'FC-B3-BC-A6-38-AD'
HOST_NAME = socket.gethostbyaddr(IP)[0]


def arp_scan(ip: str) -> list:
    request = sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=ip)
    ans, _ = sc.srp(request, timeout=1, retry=1, verbose=False)

    return [
        {'IP': received.psrc, 'MAC': received.hwsrc}
        for _, received in ans
    ]


hosts = arp_scan(f'{NETWORK_IP}/24')

start_text = f'{"IP Address":30}{"MAC Address":30}{"Host name":30}'
text = start_text

layout = [
    [sg.ProgressBar(len(hosts), size=(60, 25), key='-PROGRESS_BAR-')],
    [sg.Submit('Start', key='-BEGIN-', size=(10, 2))],
    [sg.Text(start_text, size=(60, 20), key='-TEXT-', font=('Arial', 14))]
]

window = sg.Window('Scanner', layout)

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    if event == '-BEGIN-':
        text = start_text
        text += 'Current PC:\n'
        text += f'{IP:30}{MAC:30}{HOST_NAME:30}'
        text += 'Local network:\n'

        window['-TEXT-'].Update(text)

        for i, host in enumerate(hosts):
            ip, mac = host['IP'], host['MAC']

            if ip == IP:
                continue
            try:
                host_name = socket.gethostbyaddr(ip)[0]
            except Exception:
                host_name = 'Name not found'

            text += f'{str(ip):30}{str(mac):30}{str(host_name):30}'

            window['-TEXT-'].Update(text)
            window['-PROGRESS_BAR-'].UpdateBar(i + 1)

window.close()
