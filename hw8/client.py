from constants import ADDR, CLIENT_PORT, SERVER_PORT
from stop_and_wait import StopAndWaitSocket

if __name__ == '__main__':
    input('Enter any text to start sending file')

    with open('files/data_on_client.txt', 'rb') as file:
        data = file.read()

    socket = StopAndWaitSocket(ADDR, CLIENT_PORT)
    socket.set_timeout(1)
    socket.connect(ADDR, SERVER_PORT)
    socket.sendall(data)

    socket.set_timeout(1000)

    with open('files/data_on_client_received.txt', 'wb') as file:
        file.write(socket.recvall())
