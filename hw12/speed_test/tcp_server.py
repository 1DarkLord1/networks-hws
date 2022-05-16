import PySimpleGUI as sg
import gui
import socket

from constants import PKT_SIZE
from utils import Receiver


if __name__ == '__main__':
  window = sg.Window('Получатель TCP', gui.server_layout)

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  while True:
      event, values = window.read()

      if event == 'Exit' or event == sg.WIN_CLOSED:
          break
      
      if event == '-ADDR-':
        try:
          server_addr = (values['-IP-'], int(values['-PORT-']))
        except Exception:
          sg.popup('Arguments parsing error', no_titlebar=True)
          continue
        
        server_socket.bind(server_addr)
        server_socket.listen(1)

        sg.popup('Success', no_titlebar=True)

      if event == '-RECEIVE-':
        # try:
          client_socket, _ = server_socket.accept()
          client_socket.settimeout(1)

          receiver = Receiver(client_socket, 'TCP')
          receiver.receive_all()
          receiver.calc_speed()

          window['-PKT RECEIVED-'].update(f'{receiver.pkt_num} of {receiver.total_pkt_num}')
          window['-SPEED-'].update(f'{receiver.speed} Bytes/S')
        # except Exception:
        #     sg.popup(
        #       'Data receiving failed',
        #       no_titlebar=True
        #     )
        #     continue
  
  server_socket.close()
  window.close()
