import PySimpleGUI as sg
import gui
import socket
import datetime

from constants import PKT_SIZE
from utils import gen_pkt


if __name__ == '__main__':
  window = sg.Window('Отправитель UDP', gui.client_layout)

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  while True:
      event, values = window.read()

      if event == 'Exit' or event == sg.WIN_CLOSED:
          break
  
      if event == '-SEND-':
        try:
          server_addr = (values['-IP-'], int(values['-PORT-']))
          pkt_num = int(values['-PKT NUM-'])
        except Exception:
          sg.popup('Arguments parsing error', no_titlebar=True)
          continue

        try:
          client_socket.sendto(f'{pkt_num}'.encode(), server_addr)

          for i in range(pkt_num):
              cur_time = datetime.datetime.now()
              
              msg = f'{float(cur_time.timestamp())} '
              msg += f'{gen_pkt(PKT_SIZE - len(msg))}'

              client_socket.sendto(msg.encode(), server_addr)

          sg.popup('Success', no_titlebar=True)
        except Exception:
            sg.popup(
              'Data sending failed',
              'Check if server address is correct',
              no_titlebar=True
            )
            continue
        finally:
          client_socket.close()
      
  window.close()
