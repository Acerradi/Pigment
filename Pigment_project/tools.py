
from PIL import ImageDraw, ImageColor, Image


class Tool:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.start_x = None
        self.start_y = None
        self.ids=[]

    def mouse_down(self, event):
        self.ids=[]
        # When pressing the mouse button on the canvas
        self.start_x = event.x
        self.start_y = event.y

    def mouse_move(self, event):
        # When moving the mouse over the canvas after pressing down
        raise NotImplementedError("This method should be overridden by subclasses")

    def mouse_up(self, event):
        # When releasing the mouse over the canvas
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_event_coords(self, event):
        x = self.canvas.canvasx(event.x) / self.root.imscale
        y = self.canvas.canvasy(event.y) / self.root.imscale
        return x, y

    def get_event_coords_2(self,event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        return x, y

    def get_event_coords_3(self,event):
        x = event.x / self.root.imscale
        y = event.y / self.root.imscale
        return x, y

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
    def __init__(self, root, canvas, overlay):
        super().__init__(root, canvas)
        self.overlay_canvas = overlay
        self.selection_points = []
        self.image = self.root.file_manager.current_image
        self.ids = []

    def extract_selected_Area(self):
        mask = Image.new('L', self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(self.selection_points, fill=255)

        image = self.image.copy()
        extracted_image = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
        extracted_image.paste(image, mask=mask)

        # Calculate the tight bounding box of the selected area
        bbox = mask.getbbox()  # Get the bounding box of non-zero (white) areas
        if bbox:
            cropped_image = extracted_image.crop(bbox)  # Crop tightly to the selected shape

            # Save the extracted area and display it as an overlay
            self.root.extracted_area = cropped_image
            overlay = cropped_image.copy()

            # Draw an outline on the overlay
            draw_overlay = ImageDraw.Draw(overlay)
            draw_overlay.polygon([(x - bbox[0], y - bbox[1]) for x, y in self.selection_points], outline="red")

            # Determine the top-left corner for placement
            self.root.extracted_position = (bbox[0], bbox[1])
            self.root.display_overlay_image_on_canvas(overlay, self.root.extracted_position)

    def in_range(self):
        x1, y1 = self.selection_points[0]
        x2, y2 = self.selection_points[-1]
        return True if x1+5 > x2 > x1-5 and y1+5 > y2 > y1-5 else False

#Finished
class RectangleSelection(SelectionTool):
    def __init__(self, r_canvas, canvas, overlay):
        super().__init__(r_canvas, canvas, overlay)
        self.selection_start_2 = None
        self.selection_end = None

    def mouse_down(self, event):
        # Record the initial point of the selection
        self.selection_start_1 = self.get_event_coords(event)
        self.selection_start_2 = self.get_event_coords_2(event)
        self.selection_start_3 = event.x, event.y

    def mouse_move(self, event):
        x1,y1 = self.selection_start_2
        x2,y2 = self.get_event_coords_2(event)
        # Draw a rectangle from the initial click to the current mouse position
        if self.selection_start_2:
            # Remove the previous rectangle
            if self.ids:
                self.canvas.delete(self.ids)
            # Draw the new rectangle
            self.ids = self.canvas.create_rectangle(x1, y1,
                                                    x2, y2, outline='red')

    def mouse_up(self, event):
        # Get the coordinates of the selection (top-left and bottom-right)
        start_x, start_y = self.selection_start_1
        stop_x, stop_y = self.get_event_coords(event)

        self.selection_points = [(start_x, start_y),(start_x, stop_y),(stop_x, stop_y), (stop_x, start_y)]

        # Delete the previous rectangle
        self.canvas.delete(self.ids)

        self.extract_selected_Area()

#Finished
class PolygonSelection(SelectionTool):
    def __init__(self, r_canvas, canvas, overlay):
        super().__init__(r_canvas, canvas, overlay)
        self.polygon_points = []
        self.points = []

    def mouse_down(self, event):
        x, y = self.get_event_coords_2(event)
        # Append each point as the user clicks
        self.selection_points.append((self.get_event_coords(event)))
        self.polygon_points.append((x, y))
        # Draw small circles for each vertex on the canvas
        self.points.append(self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red"))
        if len(self.selection_points) > 1:
            # Draw lines connecting points
            self.ids.append(self.canvas.create_line(self.polygon_points[-2], self.polygon_points[-1], fill="red"))

    def mouse_move(self, event):
        pass

    def mouse_up(self, event):
        if len(self.selection_points) > 2 and self.in_range():
            for id in self.ids:
                self.canvas.delete(id)
            for point in self.points:
                self.canvas.delete(point)
            self.extract_selected_Area()

#Finished
class LassoSelection(SelectionTool):
    def __init__(self, r_canvas, canvas, overlay):
        super().__init__(r_canvas, canvas, overlay)
        self.lasso_path = []

    def mouse_down(self, event):
        self.selection_points = [(self.get_event_coords(event))]  # Start new lasso path
        self.lasso_path = [(self.get_event_coords_2(event))]

    def mouse_move(self, event):
        # Append points as the user drags
        if self.selection_points:
            self.selection_points.append((self.get_event_coords(event)))
            self.lasso_path.append(self.get_event_coords_2(event))
            if self.ids:
                self.canvas.delete(self.ids)
            # Draw the current path
            self.ids = self.canvas.create_line(self.lasso_path, fill="red", smooth=True)

    def mouse_up(self, event):
        # Close the lasso path by connecting last point to the first
        if len(self.selection_points) > 2:
            self.selection_points.append(self.selection_points[0])  # Close the loop
            self.lasso_path.append(self.lasso_path[0])  # Close the loop
            if self.ids:
                self.canvas.delete(self.ids)  # Remove the path preview

            self.extract_selected_Area()

#Finished
class DrawTool(ColoredTool):
    def __init__(self,r_canvas, canvas, color, size):
        super().__init__(r_canvas, canvas, color=color)
        self.size = size
        self.current_stroke = None

    def mouse_down(self, event):
        """Start drawing when mouse button is pressed"""
        x, y = self.get_event_coords(event)
        if self.root.file_manager.current_image is not None:
            # Save the current image to history for undo
            self.root.add_to_history()
        self.start_x, self.start_y = x, y
        self.current_stroke = []

    def mouse_move(self, event):
        """Draw as the mouse is dragged"""
        if self.start_x is not None and self.start_y is not None:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = self.get_event_coords(event)

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
class EraserTool(DrawTool):
    def __init__(self, r_canvas, canvas, size):
        super().__init__(r_canvas, canvas, "#ffffff", size)

#Finished
class BucketTool(ColoredTool):
    def __init__(self, root, canvas, color):
        super().__init__(root, canvas, color=color)

    def mouse_down(self, event):
        self.root.add_to_history()
        # Get the starting coordinates
        x, y = self.get_event_coords(event)
        if type(self.color) != tuple:
            self.color = ImageColor.getrgb(self.color)

        # Get the image from the canvas (assuming canvas is associated with an image)
        self.image = self.root.file_manager.current_image
        target_color = self.image.getpixel((x, y))

        # Perform flood fill if target color is different from fill color
        if target_color != self.color:
            self.flood_fill(x, y, target_color, self.color)

        # Update the canvas with the modified image
        self.root.display_image_on_canvas()

    def mouse_move(self, event):
        pass

    def mouse_up(self, event):
        pass

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
        x, y = self.get_event_coords(event)
        pix = self.file_manager.current_image.getpixel((x, y))
        self.color = pix

    def mouse_move(self, event):
        pass

    def mouse_up(self, event):
        color = "#%02x%02x%02x" % self.color
        self.root.drawing_color = color
        self.root.chose_tool(0)

#Finished
class DrawShape(ColoredTool):
    def __init__(self, root, canvas, color, shape, size):
        super().__init__(root, canvas, color=color)
        self.ids = []
        self.shape = shape
        self.size = size
    def mouse_down(self, event):
        self.root.add_to_history()
        # Record the initial point of the selection
        #self.selection_start = (event.x/self.root.imscale, event.y/self.root.imscale)
        self.selection_start = self.get_event_coords_2(event)
    def mouse_move(self, event):
        # Draw the selected shape dynamically as the mouse moves
        if self.selection_start:
            if self.ids:
                self.canvas.delete(self.ids)

            x1, y1 = self.selection_start
            #x2, y2 = event.x/self.root.imscale, event.y/self.root.imscale
            x2,y2 = self.get_event_coords_2(event)

            if self.shape == "rectangle":
                self.ids = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.color, width=self.size)
            elif self.shape == "circle":
                self.ids = self.canvas.create_oval(x1, y1, x2, y2, outline=self.color, width=self.size)
            elif self.shape == "triangle":
                # Calculate the top vertex for an isosceles triangle
                top_x = (x1 + x2) / 2
                self.ids = self.canvas.create_polygon(x1, y2, x2, y2, top_x, y1, outline=self.color, fill="", width=self.size)
            elif self.shape == "line":
                self.ids = self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size)
    def mouse_up(self, event):
        x1, y1 = self.selection_start
        x1 = x1 / self.root.imscale
        y1 = y1 / self.root.imscale
        x2, y2 = self.get_event_coords(event)

        # Correct ordering for the top-left and bottom-right coordinates
        left, right = min(x1, x2), max(x1, x2)
        top, bottom = min(y1, y2), max(y1, y2)

        # Draw the shape directly on the current image
        draw = ImageDraw.Draw(self.root.file_manager.current_image)
        if self.shape == "rectangle":
            draw.rectangle([left, top, right, bottom], outline=self.color, width=self.size)
        elif self.shape == "circle":
            draw.ellipse([left, top, right, bottom], outline=self.color, width=self.size)
        elif self.shape == "triangle":
            top_x = (left + right) / 2
            draw.polygon([(left, y2), (right, y2), (top_x, y1)], outline=self.color, width=self.size)
        elif self.shape == "line":
            draw.line([x1, y1, x2, y2], fill=self.color, width=self.size)

        # Save the image
        self.root.file_manager.save()

        # Update the canvas to show the new image
        self.root.display_image_on_canvas()

        # Reset selection state
        self.selection_start = None
        self.ids = []


class PasteTool(Tool):
    def __init__(self, root,canvas):
        super().__init__(root, canvas)

    def mouse_down(self, event):
        paste_pos = self.get_event_coords(event)
        paste_pos = int(paste_pos[0]),int(paste_pos[1])
        if self.root.clipboard:
            if not self.root.cut:
                self.root.add_to_history()
            self.root.file_manager.current_image.paste(self.root.extracted_area, paste_pos, self.root.extracted_area)
            self.root.display_image_on_canvas()

        if self.root.cut:
            self.root.cut = False
            self.root.clipboard=False
            self.root.extracted_area = None
            self.root.extracted_position = None
            self.root.chose_tool(0)

