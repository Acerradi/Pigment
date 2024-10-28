import tkinter

import numpy as np
from PIL import ImageDraw, ImageColor, ImageTk, Image

from Pigment_project import canvas


class Tool:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.start_x = None
        self.start_y = None
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

class ColoredTool(Tool):
    def __init__(self, root, canvas, color):
        super().__init__(root, canvas)
        self.color = color

class SelectionTool(Tool):
    def __init__(self, root, canvas):
        super().__init__(root, canvas)
        self.selection_points = []
        self.image = self.root.file_manager.current_image

    def extract_selected_Area(self):
        mask = Image.new('L', self.image.size, 0)
        draw = ImageDraw.Draw(mask)

        draw.polygon(self.selection_points, fill=255)

        selected_Area = Image.composite(self.image, Image.new("RGBA", self.image.size), mask)

        self.display_on_overlay(selected_Area)

    def display_on_overlay(self, area):
        # Convert to PhotoImage for tkinter
        overlay_image = ImageTk.PhotoImage(area)

        # Display on overlay canvas at (0,0)
        self.overlay_canvas.delete("all")
        self.overlay_canvas.create_image(0, 0, anchor="nw", image=overlay_image)
        self.overlay_canvas.image = overlay_image  # Keep a reference to avoid garbage collection
        self.overlay_canvas.lift()  # Bring overlay to front

class RectangleSelection(SelectionTool):
    def __init__(self, r_canvas, canvas):
        super().__init__(r_canvas, canvas)
        self.selection_start = None
        self.selection_end = None
        self.rectangle_id = None

    def mouse_down(self, event):
        # Record the initial point of the selection
        self.selection_start = (event.x, event.y)

    def mouse_move(self, event):
        # Draw a rectangle from the initial click to the current mouse position
        if self.selection_start:
            # Remove the previous rectangle
            if self.rectangle_id:
                self.canvas.delete(self.rectangle_id)
            # Draw the new rectangle
            self.rectangle_id = self.canvas.create_rectangle(self.selection_start[0], self.selection_start[1],
                                                             event.x, event.y, outline='red')

    def mouse_up(self, event):
        # Record the final point of the selection
        self.selection_end = (event.x, event.y)
        # Ensure both points are defined for further processing
        if self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            self.selection_points.append((x1, y1))
            self.selection_points.append((x2, y1))
            self.selection_points.append((x1, y2))
            self.selection_points.append((x2, y2))
            self.extract_selected_Area()


class PolygonSelection(SelectionTool):
    def __init__(self, r_canvas,  canvas):
        super().__init__(r_canvas, canvas)
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


class LassoSelection(SelectionTool):
    def __init__(self, r_canvas, canvas):
        super().__init__(r_canvas, canvas)
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

#Finished
class DrawTool(ColoredTool):
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

#Finished
class EraserTool(ColoredTool):
    def __init__(self, r_canvas, canvas, size):
        super().__init__(r_canvas, canvas, color="#ffffff")
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

#Finished
class BucketTool(ColoredTool):
    def __init__(self, root, canvas, color):
        super().__init__(root, canvas, color=color)

    def mouse_down(self, event):
        # Get the starting coordinates
        x, y = event.x, event.y
        self.color = ImageColor.getrgb(self.color)

        # Get the image from the canvas (assuming canvas is associated with an image)
        self.image = self.root.file_manager.current_image
        target_color = self.image.getpixel((x, y))

        # Perform flood fill if target color is different from fill color
        if target_color != self.color:
            self.flood_fill(x, y, target_color, self.color)

        # Update the canvas with the modified image
        self.root.display_image_on_canvas()

    def mouse_middle(self, event):
        raise "BucketTool"

    def mouse_up(self, event):
        raise "BucketTool"

    def flood_fill(self, x, y, target_color, fill_color):
        width, height = self.image.size
        pixels = self.image.load()  # Direct access to image pixels

        # Stack-based flood fill to avoid recursion depth issues
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()

            # Skip if out of bounds or already filled with fill_color
            if not (0 <= x < width and 0 <= y < height) or pixels[x, y] != target_color:
                continue

            # Fill the current pixel
            pixels[x, y] = fill_color

            # Add neighboring pixels (4-way connectivity)
            stack.append((x + 1, y))  # Right
            stack.append((x - 1, y))  # Left
            stack.append((x, y + 1))  # Down
            stack.append((x, y - 1))  # Up

#Finished
class ColorPickerTool(ColoredTool):
    def __init__(self, root, canvas, file_manager):
        super().__init__(root, canvas, color=None)
        self.file_manager = file_manager

    def mouse_down(self, event):
        self.canvas.update_idletasks()
        x = event.x
        y = event.y
        pix = self.file_manager.current_image.getpixel((x, y))
        self.color = pix

    def mouse_move(self, event):
        pass

    def mouse_up(self, event):
        self.root.drawing_color = self.color
        self.root.chose_tool(0)
