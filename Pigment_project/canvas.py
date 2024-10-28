import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk
import cv2
from file_manager import FileManager
from tools import *


# Function that handles mouse movements and draws on the canvas
class CustomCanvas:
    def __init__(self, root):
        self.file_manager = FileManager()
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack(fill='both', expand=True)
        self.display_image_on_canvas()

        # Attributes to track drawing
        self.start_x, self.start_y = None, None
        self.current_stroke = None
        self.drawing_color = "#000000"
        self.drawing_size = 5

        # Keep track of the drawing history (for undo)
        self.history = []
        # Bind mouse events
        #self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)  # Mouse click
        #self.canvas.bind("<B1-Motion>", self.on_mouse_move)  # Mouse drag
        #self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)  # Mouse release
        self.chose_tool(0)

    def chose_tool(self, numb):
        # Drawing tool
        if numb == 0:
            self.tool = DrawTool(self, self.canvas, self.drawing_color, self.drawing_size)
            self.tool.bind_events()
        # Eraser tool
        if numb == 1:
            self.tool = EraserTool(self, self.canvas, self.drawing_size)
            self.tool.bind_events()
        # Bucket tool
        if numb == 2:
            pass
        #  Color Picker tool
        if numb == 3:
            self.tool = ColorPickerTool(self, self.canvas, self.file_manager)
            self.tool.bind_events()
        # Rectangle Selection tool
        if numb == 4:
            pass
        # Polygon Selection tool
        if numb == 5:
            pass
        # Lasso selection tool
        if numb == 6:
            pass

    def change_color(self):
        color = colorchooser.askcolor(title = "choose color")
        if color is not None:
            self.drawing_color = color[1]
            self.tool.color = color[1]

    def change_drawing_size(self):
        pass

    def display_image_on_canvas(self):
        canvas = self.canvas
        if self.file_manager.current_image is not None:
            # Convert PIL Image to ImageTk.PhotoImage for Tkinter
            img_tk = ImageTk.PhotoImage(image=self.file_manager.current_image)

            # Create image on the Tkinter canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            # To prevent garbage collection of image in Tkinter
            canvas.img_tk = img_tk  # Save a reference to the image

    def undo(self):
        """Undo the last stroke"""
        if self.history:
            # Revert to the last saved state in the history
            self.file_manager.current_image = self.history.pop()
            self.display_image_on_canvas()

    def crop(self, crop_area):
        self.history.append(self.file_manager.current_image.copy())
        width,heigth = self.file_manager.current_image.size
        crop_area = (crop_area[0],crop_area[1],width-crop_area[2],heigth-crop_area[3])
        self.file_manager.current_image = self.file_manager.current_image.crop(crop_area)
        self.display_image_on_canvas()

    def rotate(self, opt):
        self.history.append(self.file_manager.current_image.copy())
        if opt == 1:
            self.file_manager.current_image = self.file_manager.current_image.rotate(90)
        elif opt == 2:
            self.file_manager.current_image = self.file_manager.current_image.rotate(270)
        self.display_image_on_canvas()

    def flip(self, opt):
        self.history.append(self.file_manager.current_image.copy())
        if opt == 3:
            self.file_manager.current_image = self.file_manager.current_image.transpose(Image.FLIP_TOP_BOTTOM)
        elif opt == 4:
            self.file_manager.current_image = self.file_manager.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image_on_canvas()