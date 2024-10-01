import tkinter as tk
# Function that handles mouse movements and draws on the canvas
class CustomCanvas:
    def paint(self,event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_line(x1, y1, x2, y2, fill="black", width=5)
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
