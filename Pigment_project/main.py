import tkinter
from tkinter import *

def print_sentence():
    print('hello world')


# Main window of the Paint class
class MainWindow(tkinter.Tk):
    def __init__(self, XY, title):
        super().__init__()
        self.x, self.y = XY
        self.geometry(f"{self.x}x{self.y}")
        self.title(title)

        # Create all menu objects
        self.menu = Menu(self)
        self.file_menu = Menu(self)
        self.help_menu = Menu(self)
        self.setup_menus()

    def setup_menus(self):
        # Set up menus
        self.config(menu=self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)

        # Set up file_menu
        self.file_menu.add_command(label='New', command=print_sentence)
        self.file_menu.add_command(label='Open', command=self.open_load_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=print_sentence)
        self.file_menu.add_command(label='Save As', command=self.open_save_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.quit)

        # Set up help_menu
        self.help_menu.add_command(label='Help', command=print_sentence)

        test_label = Label(self, text="Hello World")
        test_label.pack()

    def open_load_window(self):
        # Check to keep only one extra window open at a time
        if not SecondaryWindow.open:
            self.load_window = SecondaryWindow((int(self.x/2), int(self.y/2)), "Load Image", print_sentence)

    def open_save_window(self):
        # Check to keep only one extra window open at a time
        if not SecondaryWindow.open:
            self.save_window = SecondaryWindow((int(self.x/2), int(self.y/2)), "Save Image", print_sentence)

    def run(self):
        # Execute tkinter
        self.mainloop()


# Secondary window class for loading/saving images
class SecondaryWindow(tkinter.Toplevel):
    # Value to keep track of whether this window is open or not
    open = False
    def __init__(self, XY ,title, func):
        super().__init__()
        self.config(width = XY[0], height = XY[1])
        self.title(title)
        self.func = func()
        self.file_path = ''
        self.__class__.alive = True

    def function(self):
        #Either load the image from the chosen self.filepath or save the current image to the current self.filepath
        pass


# Main Class
class Pigment:
    def __init__(self, XY):
        # Set dimensions of the main window
        self.x, self.y = XY

        # Create main window object
        self.root = MainWindow(XY, 'Pigment-PaintLite')




screen = (700,1000)

program = Pigment(screen)
program.root.run()

