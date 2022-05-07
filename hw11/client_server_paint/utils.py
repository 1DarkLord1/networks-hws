import tkinter as tk
from xmlrpc.client import ServerProxy

from constants import DOT_RADIUS


def canvas_paint(canvas: tk.Canvas):
  def paint(x, y):
      x1, y1 = (x - DOT_RADIUS), (y - DOT_RADIUS)
      x2, y2 = (x + DOT_RADIUS), (y + DOT_RADIUS)
      color = "black"

      canvas.create_oval(x1, y1, x2, y2, fill = color, outline = color)

  return paint


def canvas_sync(canvas: tk.Canvas, proxy: ServerProxy):
  def paint(event):
      canvas_paint(canvas)(event.x, event.y)
      proxy.paint(event.x, event.y)

  return paint
 