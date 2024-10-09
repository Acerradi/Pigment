import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import cv2
from file_manager import FileManager


# Function that handles mouse movements and draws on the canvas
class CustomCanvas:
    def __init__(self, root):
        self.file_manager = FileManager()
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack(fill='both', expand=True)
        self.display_image_on_canvas()
        # Attributes to track drawing
        self.start_x, self.start_y = None, None
        self.current_stroke = None
        # Keep track of the drawing history (for undo)
        self.history = []
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)  # Mouse click
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)  # Mouse drag
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)  # Mouse release

    def on_mouse_down(self, event):
        """Start drawing when mouse button is pressed"""
        if self.file_manager.current_image is not None:
            # Save the current image to history for undo
            self.history.append(self.file_manager.current_image.copy())
        self.start_x, self.start_y = event.x, event.y
        self.current_stroke = []

    def on_mouse_move(self, event):
        """Draw as the mouse is dragged"""
        if self.start_x is not None and self.start_y is not None:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y

            # Draw the line directly on the image
            draw = ImageDraw.Draw(self.file_manager.current_image)
            draw.line([x1, y1, x2, y2], fill="black", width=5)
            # Add line points to current stroke
            self.current_stroke.append(((x1, y1), (x2, y2)))
            # Display the updated image on the canvas
            self.display_image_on_canvas()

            # Update start point for next motion
            self.start_x, self.start_y = x2, y2

    def on_mouse_up(self, event):
        """Finalize drawing when mouse button is released"""
        if self.current_stroke:
            # Draw the entire stroke on the image
            if self.file_manager.current_image is not None:
                draw = ImageDraw.Draw(self.file_manager.current_image)
                for (x1, y1), (x2, y2) in self.current_stroke:
                    draw.line([x1, y1, x2, y2], fill="black", width=5)
                self.display_image_on_canvas()

        # Reset drawing state
        self.start_x, self.start_y = None, None
        self.current_stroke = []

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
    def rotate_left(self):
        self.history.append(self.file_manager.current_image.copy())
        self.file_manager.current_image = self.file_manager.current_image.rotate(90)
        self.display_image_on_canvas()
    def rotate_right(self):
        self.history.append(self.file_manager.current_image.copy())
        self.file_manager.current_image = self.file_manager.current_image.rotate(270)
        self.display_image_on_canvas()
    def flip_vertically(self):
        self.history.append(self.file_manager.current_image.copy())
        self.file_manager.current_image = self.file_manager.current_image.transpose(Image.FLIP_TOP_BOTTOM)
        self.display_image_on_canvas()
    def flip_horizontally(self):
        self.history.append(self.file_manager.current_image.copy())
        self.file_manager.current_image = self.file_manager.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image_on_canvas()