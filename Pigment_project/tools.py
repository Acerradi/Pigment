import tkinter


class Tool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x = None
        self.start_y = None

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
    def __init__(self, canvas):
        super().__init__(canvas)
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
        pass


class PolygonSelection(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
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
    def __init__(self, canvas):
        super().__init__(canvas)
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
        pass