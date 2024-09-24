
from tkinter import *

def print_sentence():
    print('hello world')


class Pigment:
    def __init__(self, dimensions):
        # Set dimensions of the main window
        self.x, self.y = dimensions

        # Create main window object
        self.root = Tk()
        self.root.title('Pigment-PaintLite')

        # Create save window
        self.save_window = Tk()
        self.save_window.title('Save')

        # Create load window
        self.load_window = Tk()
        self.load_window.title('Load')

        # Create all menus
        self.menu = Menu(self.root)
        self.file_menu = Menu(self.menu)
        self.help_menu = Menu(self.menu)

    def setup_menus(self):
        # Set up menus
        self.root.config(menu=self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)

        # Set up file_menu
        self.file_menu.add_command(label='New', command=print_sentence)
        self.file_menu.add_command(label='Open', command=self.load_img)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=print_sentence)
        self.file_menu.add_command(label='Save As', command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.quit)

        # Set up help_menu
        self.help_menu.add_command(label='Help', command=print_sentence)

        test_label = Label(self.root, text="Hello World")
        test_label.pack()

        # Set size
        self.root.geometry(f"{self.y}x{self.x}")

    def save_as(self):
        self.save_window.mainloop()

    def load_img(self):
        self.load_window.mainloop()

    def run(self):
        # Execute tkinter
        self.root.mainloop()


screen = (700,1000)
program = Pigment(screen)
program.setup_menus()
program.run()

