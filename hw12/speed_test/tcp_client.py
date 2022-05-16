import PySimpleGUI as sg
import gui
import socket
import datetime
import time

from constants import PKT_SIZE
from utils import gen_pkt


if __name__ == '__main__':
  window = sg.Window('Отправитель TCP', gui.client_layout)

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
          client_socket.connect(server_addr)
          client_socket.sendall(f'{pkt_num}'.encode())

          for i in range(pkt_num):
              cur_time = datetime.datetime.now()
              
              msg = f'{float(cur_time.timestamp())} '
              msg += f'{gen_pkt(PKT_SIZE - len(msg))}'

              client_socket.sendall(msg.encode())

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
