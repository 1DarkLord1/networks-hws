from constants import ADDR, CLIENT_PORT, SERVER_PORT
from stop_and_wait import StopAndWaitSocket

if __name__ == '__main__':
    input('Enter any text to start receiving file')

    socket = StopAndWaitSocket(ADDR, SERVER_PORT)
    socket.set_timeout(1000)
    socket.connect(ADDR, CLIENT_PORT)

    with open('files/data_on_server_received.txt', 'wb') as file:
        file.write(socket.recvall())

    with open('files/data_on_server.txt', 'rb') as file:
        data = file.read()

    socket.set_timeout(1)
    socket.sendall(data)
