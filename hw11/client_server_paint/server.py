import asyncio as aio
import tkinter as tk
from xmlrpc.server import SimpleXMLRPCServer

from constants import CANVAS_SIZE, SERVER_ADDR
from utils import canvas_paint


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Server paint Application')
    root.geometry(f'{CANVAS_SIZE[0]}x{CANVAS_SIZE[1]}')

    canvas = tk.Canvas(root, width = CANVAS_SIZE[0], height = CANVAS_SIZE[1], bg = 'white')
    canvas.pack(fill = 'both', expand = True)

    server = SimpleXMLRPCServer(SERVER_ADDR, allow_none=True)

    print(f'Listening on port {SERVER_ADDR[0]}...')

    server.register_function(canvas_paint(canvas), 'paint')
    server.register_function(root.update, 'update')
    server.register_function(canvas.delete, 'delete')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
