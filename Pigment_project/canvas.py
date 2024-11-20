import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import ImageTk
from typing import Tuple

from file_manager import FileManager
from tools import *
import time


class AutoScrollbar(ttk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed. """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)


# Function that handles mouse movements and draws on the canvas
class CustomCanvas:
    def __init__(self, root):
        self.file_manager = FileManager()
        self.extracted_area = None
        self.extracted_position = None
        self.clipboard = False
        self.cut = False
        self.root = root
        self.height, self.width = 500, 500
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, xscrollcommand=self.scroll_x, yscrollcommand=self.scroll_y)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Atributes for zoom and pan functionality
        self.imscale = 1.0
        self.delta = 1.3

        # Add scrollbar
        self.vbar = AutoScrollbar(root, orient='vertical', command=self.scroll_y)
        self.hbar = AutoScrollbar(root, orient='horizontal', command=self.scroll_x)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.vbar.grid(row=0, column=1, sticky='ns')
        self.hbar.grid(row=1, column=0, sticky='ew')

        # Attributes to track drawing
        self.start_x, self.start_y = None, None
        self.current_stroke = None
        self.drawing_color = "#000000"
        self.drawing_size = 5

        # Keep track of the drawing history (for undo)
        self.history = []
        self.chose_tool(0)

        # Bind zoom
        self.canvas.bind('<MouseWheel>', self.wheel)

        # Time tracking
        self.last_draw_time = time.time()

    def scroll_y(self, *args):
        self.canvas.yview(*args)
        self.display_image_on_canvas()

    def scroll_x(self, *args):
        self.canvas.xview(*args)
        self.display_image_on_canvas()

    def wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        scale = 1.0
        if event.delta > 0:  # Scroll up
            self.imscale *= self.delta
            scale *= self.delta
        elif event.delta < 0:  # Scroll down
            self.imscale /= self.delta
            scale /= self.delta
        self.canvas.scale('all', x, y, scale, scale)
        self.display_image_on_canvas()

    def chose_tool(self, numb):
        # Drawing tool
        if numb == 0:
            self.tool = DrawTool(self, self.canvas, self.drawing_color, self.drawing_size)
        # Eraser tool
        if numb == 1:
            self.tool = EraserTool(self, self.canvas, self.drawing_size)
        # Bucket tool
        if numb == 2:
            self.tool = BucketTool(self, self.canvas, self.drawing_color)
        #  Color Picker tool
        if numb == 3:
            self.tool = ColorPickerTool(self, self.canvas, self.file_manager)
        # Rectangle Selection tool
        if numb == 4:
            self.tool = RectangleSelection(self, self.canvas, self.canvas)
        # Polygon Selection tool
        if numb == 5:
            self.tool = PolygonSelection(self, self.canvas, self.canvas)
        # Lasso selection tool
        if numb == 6:
            self.tool = LassoSelection(self, self.canvas, self.canvas)
        # Line drawing tool
        if numb == 7:
            self.tool = DrawShape(self, self.canvas, self.drawing_color, "line")
        # Rectangle drawing tool
        if numb == 8:
            self.tool = DrawShape(self, self.canvas, self.drawing_color, "rectangle")
        # Circle drawing tool
        if numb == 9:
            self.tool = DrawShape(self, self.canvas, self.drawing_color, "circle")
        # Triangle drawing tool
        if numb == 10:
            self.tool = DrawShape(self, self.canvas, self.drawing_color, "triangle")
        if numb == 11:
            self.tool = PasteTool(self,self.canvas)
        self.tool.bind_events()

    def change_color(self):
        color = colorchooser.askcolor(title = "choose color")
        if color is not None:
            self.drawing_color = color[1]
            self.tool.color = color[1]

    def change_drawing_size(self):
        pass

    """
    def display_image_on_canvas(self):
        canvas = self.canvas
        if self.file_manager.current_image is not None:
            # Convert PIL Image to ImageTk.PhotoImage for Tkinter
            img_tk = ImageTk.PhotoImage(image=self.file_manager.current_image)

            # Create image on the Tkinter canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            # To prevent garbage collection of image in Tkinter
            canvas.img_tk = img_tk  # Save a reference to the image
    """

    def display_image_on_canvas(self):
        """ Display the current image on the canvas with scaling """
        current_time = time.time()
        if current_time - self.last_draw_time < 0.05:
            return
        self.last_draw_time = current_time
        if self.file_manager.current_image:

            # Adjust visible portion of the image based on zoom
            width, height = self.file_manager.current_image.size
            scaled_width = int(width * self.imscale)
            scaled_height = int(height * self.imscale)
            self.canvas.config(scrollregion=(0, 0, scaled_width, scaled_height))

            # Crop and resize for visible area
            visible_region = (self.canvas.canvasx(0), self.canvas.canvasy(0),
                              self.canvas.canvasx(self.canvas.winfo_width()),
                              self.canvas.canvasy(self.canvas.winfo_height()))

            crop_box = (int(visible_region[0] / self.imscale), int(visible_region[1] / self.imscale),
                        int(visible_region[2] / self.imscale), int(visible_region[3] / self.imscale))

            cropped_image = self.file_manager.current_image.crop(crop_box)
            display_image = cropped_image.resize((int(visible_region[2] - visible_region[0]),
                                                  int(visible_region[3] - visible_region[1])),
                                                 Image.Resampling.LANCZOS)

            self.tk_image = ImageTk.PhotoImage(display_image)
            self.canvas.create_image(visible_region[0], visible_region[1], anchor='nw', image=self.tk_image)

    def display_overlay_image_on_canvas(self, overlay:Image, pos: Tuple[int,int]=(0,0)):
        """ Display the current image on the canvas with scaling """
        background = self.file_manager.current_image.copy()

        if overlay.mode == "RGBA":
            background.paste(overlay, pos, mask=overlay.split()[3])
        else:
            background.paste(overlay, pos)

        current_time = time.time()
        if current_time - self.last_draw_time < 0.05:
            return
        self.last_draw_time = current_time

        if background:

            # Adjust visible portion of the image based on zoom
            width, height = background.size
            scaled_width = int(width * self.imscale)
            scaled_height = int(height * self.imscale)
            self.canvas.config(scrollregion=(0, 0, scaled_width, scaled_height))

            # Crop and resize for visible area
            visible_region = (self.canvas.canvasx(0), self.canvas.canvasy(0),
                              self.canvas.canvasx(self.canvas.winfo_width()),
                              self.canvas.canvasy(self.canvas.winfo_height()))

            crop_box = (int(visible_region[0] / self.imscale), int(visible_region[1] / self.imscale),
                        int(visible_region[2] / self.imscale), int(visible_region[3] / self.imscale))

            cropped_image = background.crop(crop_box)
            display_image = cropped_image.resize((int(visible_region[2] - visible_region[0]),
                                                  int(visible_region[3] - visible_region[1])),
                                                 Image.Resampling.LANCZOS)

            self.tk_image = ImageTk.PhotoImage(display_image)
            self.canvas.create_image(visible_region[0], visible_region[1], anchor='nw', image=self.tk_image)

    def add_to_history(self):
        if len(self.history) >= 30:
            self.history.pop(0)
        self.history.append(self.file_manager.current_image.copy())

    def undo(self):
        """Undo the last stroke"""
        if self.history:
            # Revert to the last saved state in the history
            self.file_manager.current_image = self.history.pop()
            self.display_image_on_canvas()

    def crop(self, crop_area):
        self.add_to_history()
        width,heigth = self.file_manager.current_image.size
        crop_area = (crop_area[0],crop_area[1],width-crop_area[2],heigth-crop_area[3])
        self.file_manager.current_image = self.file_manager.current_image.crop(crop_area)
        self.display_image_on_canvas()

    def resize(self, new_width, new_height):
        self.add_to_history()

        # Get the current image and its size
        current_image = self.file_manager.current_image

        # Create a new blank image with the desired size, filled with white
        new_image = Image.new("RGB", (new_width, new_height), "white")

        # Paste the current image onto the new canvas
        new_image.paste(current_image, (0, 0))

        # Update the current image and redisplay
        self.file_manager.current_image = new_image
        self.display_image_on_canvas()

    def rotate(self, opt):
        self.add_to_history()
        if opt == 1:
            self.file_manager.current_image = self.file_manager.current_image.rotate(90)
        elif opt == 2:
            self.file_manager.current_image = self.file_manager.current_image.rotate(270)
        self.display_image_on_canvas()

    def flip(self, opt):
        self.add_to_history()
        if opt == 3:
            self.file_manager.current_image = self.file_manager.current_image.transpose(Image.FLIP_TOP_BOTTOM)
        elif opt == 4:
            self.file_manager.current_image = self.file_manager.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image_on_canvas()