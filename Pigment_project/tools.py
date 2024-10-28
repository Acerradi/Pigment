import tkinter

import numpy as np
from PIL import ImageDraw, ImageGrab

class Tool:
    def __init__(self, root, canvas, color):
        self.root = root
        self.canvas = canvas
        self.start_x = None
        self.start_y = None
        self.color = color
        self.bind_events()

    def mouse_down(self, event):
        # When pressing the mouse button on the canvas
        self.start_x = event.x
        self.start_y = event.y

    def mouse_move(self, event):
        # When moving the mouse over the canvas after pressing down
        raise NotImplementedError("This method should be overridden by subclasses")

    def mouse_up(self, event):
        # When releasing the mouse over the canvas
        raise NotImplementedError("This method should be overridden by subclasses")

    def bind_events(self):
        # Binds the mouse events onto the overlay canvas layer
        self.canvas.bind("<ButtonPress-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)


class RectangleSelection(Tool):
    def __init__(self, r_canvas, canvas):
        super().__init__(r_canvas, canvas, color=None)
        self.selection = None

    def mouse_down(self, event):
        #Start drawing the rectangle
        super().mouse_down(event)
        self.selection = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def mouse_move(self, event):
        # Update the rectangle while moving the mouse
        self.canvas.coords(self.selection, self.start_x, self.start_y, event.x, event.y)

    def mouse_up(self, event):
        # Finalize the rectangle selection
        raise "RectangleSelection"
        pass


class PolygonSelection(Tool):
    def __init__(self, r_canvas,  canvas):
        super().__init__(r_canvas, canvas, color=None)
        self.polygon_points = []

    def mouse_down(self, event):
        # Add coordinate points to the polygon
        self.polygon_points.append((event.x, event.y))
        if len(self.polygon_points) > 1:
            self.canvas.create_line(self.polygon_points[-2], self.polygon_points[-1], fill='red')
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill='blue')

    def mouse_move(self, event):
        # No need to add anything
        pass

    def mouse_up(self, event):
        if len(self.polygon_points) > 2:
            self.canvas.create_line(self.polygon_points[-1], self.polygon_points[0], fill='red')


class LassoSelection(Tool):
    def __init__(self, r_canvas, canvas):
        super().__init__(r_canvas, canvas, color=None)
        self.lasso_points = []

    def mouse_down(self, event):
        # Add a point to the lasso_points list
        self.lasso_points.append((event.x, event.y))

    def mouse_move(self, event):
        # Add points to the lasso path as the mouse moves
        self.lasso_points.append((event.x, event.y))
        self.canvas.create_line(self.lasso_points[-2], self.lasso_points[-1], fill='red')

    def mouse_up(self, event):
        #Finalize the lasso selection
        raise "LassoSelection"
        pass


class DrawTool(Tool):
    def __init__(self,r_canvas, canvas, color, size):
        super().__init__(r_canvas, canvas, color=color)
        self.size = size
        self.current_stroke = None

    def mouse_down(self, event):
        """Start drawing when mouse button is pressed"""
        if self.root.file_manager.current_image is not None:
            # Save the current image to history for undo
            self.root.history.append(self.root.file_manager.current_image.copy())
        self.start_x, self.start_y = event.x, event.y
        self.current_stroke = []

    def mouse_move(self, event):
        """Draw as the mouse is dragged"""
        if self.start_x is not None and self.start_y is not None:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y

            # Draw the line directly on the image
            draw = ImageDraw.Draw(self.root.file_manager.current_image)
            draw.line([x1, y1, x2, y2], fill=self.color, width=self.size)
            # Add line points to current stroke
            self.current_stroke.append(((x1, y1), (x2, y2)))
            # Display the updated image on the canvas
            self.root.display_image_on_canvas()

            # Update start point for next motion
            self.start_x, self.start_y = x2, y2

    def mouse_up(self, event):
        """Finalize drawing when mouse button is released"""
        if self.current_stroke:
            # Draw the entire stroke on the image
            if self.root.file_manager.current_image is not None:
                draw = ImageDraw.Draw(self.root.file_manager.current_image)
                for (x1, y1), (x2, y2) in self.current_stroke:
                    draw.line([x1, y1, x2, y2], fill=self.color, width=self.size)
                self.root.display_image_on_canvas()

        # Reset drawing state
        self.start_x, self.start_y = None, None
        self.current_stroke = []


class EraserTool(Tool):
    def __init__(self, root, canvas, size):
        super().__init__(root, canvas, color="#FFFFFF")
        self.size = size

    def mouse_drag(self, event):
        raise "EraserTool"

    def mouse_move(self, event):
        raise "EraserTool"

    def mouse_down(self, event):
        raise "EraserTool"


class BucketTool(Tool):
    def __init__(self, root, canvas, color):
        super().__init__(root, canvas, color=color)

    def mouse_down(self, event):
        raise "BucketTool"

    def mouse_middle(self, event):
        raise "BucketTool"

    def mouse_up(self, event):
        raise "BucketTool"


class ColorPickerTool(Tool):
    def __init__(self, root, canvas):
        super().__init__(root, canvas, color=None)

    def mouse_down(self, event):
        self.canvas.update_idletasks()
        x = self.canvas.winfo_rootx()+event.x
        y = self.canvas.winfo_rooty()+event.y
        image = ImageGrab.grab(bbox=(x,y,x+1,y+1))

        rgb_color = image.getpixel((0,0))
        self.color = rgb_color


    def mouse_move(self, event):
        raise "ColorPickerTool"

    def mouse_up(self, event):
        self.root.drawing_color = self.color
        raise "ColorPickerTool"
