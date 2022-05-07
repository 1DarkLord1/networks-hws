import tkinter as tk
from xmlrpc.client import ServerProxy

from constants import CANVAS_SIZE, SERVER_ADDR
from utils import canvas_sync


CLIENT_ADDR = ('127.0.0.1', 8080)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Client paint Application')
    root.geometry(f'{CANVAS_SIZE[0]}x{CANVAS_SIZE[1]}')

    canvas = tk.Canvas(root, width = CANVAS_SIZE[0], height = CANVAS_SIZE[1], bg = 'white')
    canvas.pack(fill = 'both', expand = True)

    with ServerProxy(f'http://localhost:{SERVER_ADDR[1]}/') as proxy:
        canvas.bind('<B1-Motion>', canvas_sync(canvas, proxy))

        while True:
            try:
                canvas.update()
                proxy.update()
            except (Exception, KeyboardInterrupt):
                proxy.delete('all')
                proxy.update()
                exit(0)
