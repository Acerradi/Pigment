import tkinter
from tkinter import *
from tkinter import filedialog

from canvas import CustomCanvas
from file_manager import FileManager

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
        self.image_menu = Menu(self)
        self.help_menu = Menu(self)

    def setup_menus(self, canvas, program):
        # Set up menus
        self.config(menu=self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Image', menu=self.image_menu)
        self.menu.add_cascade(label='Undo', command=canvas.undo)
        self.menu.add_cascade(label='Help', menu=self.help_menu)


        # Set up file_menu
        self.file_menu.add_command(label='New', command=lambda:self.new_main_window(program))
        self.file_menu.add_command(label='Open', command=lambda:self.open_load_window(canvas))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=lambda:self.save(canvas))
        self.file_menu.add_command(label='Save As', command=lambda:self.open_save_window(canvas))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.quit)
        #Set up image menu
        self.image_menu.add_command(label="Crop",command=lambda:self.open_crop_window(canvas))
        self.image_menu.add_command(label="Resize")
        self.image_menu.add_command(label="Rotate left",command=lambda:self.image_edit(1,canvas))
        self.image_menu.add_command(label="Rotate right",command=lambda:self.image_edit(2,canvas))
        self.image_menu.add_command(label="Flip vertically",command=lambda:self.image_edit(3,canvas))
        self.image_menu.add_command(label="Flip horizontally",command=lambda:self.image_edit(4,canvas))

        # Set up help_menu
        self.help_menu.add_command(label='Help', command=print_sentence)

        test_label = Label(self, text="Hello World")
        test_label.pack()
    def new_main_window(self,program):
        program.root.destroy()
        program.create_main_window()
    def open_load_window(self, canvas):
        # Check to keep only one extra window open at a time
        if not SecondaryWindow.open:
            file_path = filedialog.askopenfilename(
                title="Select an Image",
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")],
            )
            canvas.file_manager.import_image(file_path)
            canvas.display_image_on_canvas()
    def save(self, canvas):
        if canvas.file_manager.current_path is None:
            self.open_save_window(canvas)
        elif canvas.file_manager.current_path is not None:
            canvas.file_manager.save()
    def open_save_window(self,canvas):
        # Check to keep only one extra window open at a time
        if not SecondaryWindow.open:
            file = filedialog.asksaveasfile(defaultextension="png",
                title="Save as",
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
            )
            if file:
                canvas.file_manager.current_image.save(file.name)
    def open_crop_window(self, canvas:CustomCanvas):
        crop_window = Toplevel(self)
        label_1_text = StringVar()
        label_1_text.set("Pixels cropped from left")
        label_1 = Label(crop_window, textvariable=label_1_text)
        label_1.pack()
        entry_1_text = StringVar()
        entry_1 = Entry(crop_window, textvariable=entry_1_text)
        entry_1.pack()
        label_2_text = StringVar()
        label_2_text.set("Pixels cropped from top")
        label_2 = Label(crop_window, textvariable=label_2_text)
        label_2.pack()
        entry_2_text = StringVar()
        entry_2 = Entry(crop_window, textvariable=entry_2_text)
        entry_2.pack()
        label_3_text = StringVar()
        label_3_text.set("Pixels cropped from right")
        label_3 = Label(crop_window, textvariable=label_3_text)
        label_3.pack()
        entry_3_text = StringVar()
        entry_3 = Entry(crop_window, textvariable=entry_3_text)
        entry_3.pack()
        label_4_text = StringVar()
        label_4_text.set("Pixels cropped from bottom")
        label_4 = Label(crop_window, textvariable=label_4_text)
        label_4.pack()
        entry_4_text = StringVar()
        entry_4 = Entry(crop_window, textvariable=entry_4_text)
        entry_4.pack()
        confirm_button = Button(crop_window, text="Confirm", command=lambda:canvas.crop((int(entry_1_text.get()),int(entry_2_text.get()),int(entry_3_text.get()),int(entry_4_text.get()))))
        confirm_button.pack()
    def image_edit(self,opt:int,canvas:CustomCanvas):
        if opt == 1:
            canvas.rotate_left()
        elif opt == 2:
            canvas.rotate_right()
        elif opt == 3:
            canvas.flip_vertically()
        elif opt == 4:
            canvas.flip_horizontally()

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


    def create_main_window(self):
        # Create main window object
        self.root = MainWindow((self.x,self.y), 'Pigment-PaintLite')
        self.canvas = CustomCanvas(self.root)
        self.root.setup_menus(self.canvas, self)
        self.root.run()
def run1():
    screen = (700, 1000)
    program = Pigment(screen)
    program.create_main_window()
if __name__ == '__main__':
    run1()


