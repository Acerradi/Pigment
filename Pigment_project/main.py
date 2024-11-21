import tkinter
from tkinter import *
from tkinter import filedialog

from Pigment_project.clipboard import cut, copy_clipboard
from filters import *

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
        self.filter_menu = Menu(self)
        self.edit_menu = Menu(self)

        # Create all window objects
        self.top_frame = None
        self.left_frame = None
        self.right_frame = None
        self.canvas_frame = None
        self.setup_windows()

    def setup_windows(self):
        # Configure the grid layout of the window
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Initialize the top frame, stretch it out across three columns and make it stretch horizontally when the window expands
        self.top_frame = tkinter.Frame(self, height=150, borderwidth= 5, relief=tkinter.RIDGE)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky=tkinter.EW)
        # Initialize the left frame in (row 1, column 0), and make it stretch vertically when the window expands
        self.left_frame = tkinter.Frame(self, width=150, borderwidth= 5, relief=tkinter.RIDGE)
        self.left_frame.grid(row=1, column=0, sticky=tkinter.NS)
        # Initialize the right frame in (row 1, column 2), and make it stretch vertically when the window expands
        self.right_frame = tkinter.Frame(self, width=150, borderwidth= 5, relief=tkinter.RIDGE)
        self.right_frame.grid(row=1, column=2, sticky=tkinter.NS)
        # Initialize the canvas frame in (row 1, column 1), and make it expand in all directions when the window expands
        self.canvas_frame = tkinter.Frame(self, bg='gray')
        self.canvas_frame.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

    def setup_main_frames(self, canvas):
        change_color_button = tkinter.Button(self.right_frame, text = "Select color", command=canvas.change_color)
        change_color_button.grid(row=0, column=0)

        def get_value(button):
            return int(button.get())
        draw_size_button = tkinter.Spinbox(self.right_frame, from_=1, to=30, command=lambda:canvas.set_Drawing_size(get_value(draw_size_button)))
        draw_size_button.grid(row=1, column=0)
        draw_size_button.delete(0, tkinter.END)
        draw_size_button.insert(0, "5")

        draw_tool_button = tkinter.Button(self.left_frame, text = "Draw", command=lambda:canvas.chose_tool(numb=0))
        draw_tool_button.grid(row=0, column=0)

        erase_tool_button = tkinter.Button(self.left_frame, text = "Erase", command=lambda:canvas.chose_tool(numb=1))
        erase_tool_button.grid(row=0, column=1)

        color_picker_button = tkinter.Button(self.left_frame, text = "Pick", command=lambda:canvas.chose_tool(numb=3))
        color_picker_button.grid(row=1, column=0)

        bucket_tool_button = tkinter.Button(self.left_frame, text = "Bucket", command=lambda:canvas.chose_tool(numb=2))
        bucket_tool_button.grid(row=1, column=1)

        select_rectangle_button = tkinter.Button(self.left_frame, text = "rectangle_select", command=lambda:canvas.chose_tool(4))
        select_rectangle_button.grid(row=2, column=0)

        select_polygon_button = tkinter.Button(self.left_frame, text = "select_polygon", command=lambda:canvas.chose_tool(5))
        select_polygon_button.grid(row=3, column=0)

        select_lasso_button = tkinter.Button(self.left_frame, text="select_lasso", command=lambda: canvas.chose_tool(6))
        select_lasso_button.grid(row=4, column=0)

        draw_line_button = tkinter.Button(self.top_frame, text="Draw line",command=lambda: canvas.chose_tool(7))
        draw_line_button.grid(row=0, column=0)

        draw_rectangle_button = tkinter.Button(self.top_frame, text="Draw rectangle", command=lambda: canvas.chose_tool(8))
        draw_rectangle_button.grid(row=0, column=1)

        draw_circle_button = tkinter.Button(self.top_frame, text="Draw circle",command=lambda: canvas.chose_tool(9))
        draw_circle_button.grid(row=0, column=2)
        draw_triangle_button = tkinter.Button(self.top_frame, text="Draw triangle",
                                            command=lambda: canvas.chose_tool(10))
        draw_triangle_button.grid(row=0, column=3)

    def setup_menus(self, canvas, program):
        # Set up menus
        self.config(menu=self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Image', menu=self.image_menu)
        self.menu.add_cascade(label='Undo', command=canvas.undo)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.menu.add_cascade(label="Filters", menu=self.filter_menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)


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
        self.image_menu.add_command(label="Resize", command=lambda:self.open_resize_window(canvas))
        self.image_menu.add_command(label="Rotate left",command=lambda:self.image_edit(1,canvas))
        self.image_menu.add_command(label="Rotate right",command=lambda:self.image_edit(2,canvas))
        self.image_menu.add_command(label="Flip vertically",command=lambda:self.image_edit(3,canvas))
        self.image_menu.add_command(label="Flip horizontally",command=lambda:self.image_edit(4,canvas))

        # Set up help_menu
        self.help_menu.add_command(label='Help', command=print_sentence)

        self.filter_menu.add_command(label="Gaussian", command=lambda:self.gaussian(canvas))
        self.filter_menu.add_command(label="Sobel", command=lambda: self.sobel(canvas))
        self.filter_menu.add_command(label="Binary", command=lambda: self.binary(canvas))

        self.edit_menu.add_command(label="Cut", command=lambda: cut(canvas))
        self.edit_menu.add_command(label="Copy", command=lambda: copy_clipboard(canvas))
        self.edit_menu.add_command(label="Paste",command=lambda:canvas.chose_tool(11))

    def new_main_window(self,program):
        program.root.destroy()
        program.create_main_window()

    def open_load_window(self, canvas):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if file_path:
            canvas.file_manager.import_image(file_path)
            canvas.display_image_on_canvas()

    def save(self, canvas):
        if canvas.file_manager.current_path is None:
            self.open_save_window(canvas)
        elif canvas.file_manager.current_path is not None:
            canvas.file_manager.save()

    def open_save_window(self,canvas):
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
        entry_1_text = StringVar(value="0")
        entry_1 = Entry(crop_window, textvariable=entry_1_text)
        entry_1.pack()

        label_2_text = StringVar()
        label_2_text.set("Pixels cropped from top")
        label_2 = Label(crop_window, textvariable=label_2_text)
        label_2.pack()
        entry_2_text = StringVar(value="0")
        entry_2 = Entry(crop_window, textvariable=entry_2_text)
        entry_2.pack()

        label_3_text = StringVar()
        label_3_text.set("Pixels cropped from right")
        label_3 = Label(crop_window, textvariable=label_3_text)
        label_3.pack()
        entry_3_text = StringVar(value="0")
        entry_3 = Entry(crop_window, textvariable=entry_3_text)
        entry_3.pack()

        label_4_text = StringVar()
        label_4_text.set("Pixels cropped from bottom")
        label_4 = Label(crop_window, textvariable=label_4_text)
        label_4.pack()
        entry_4_text = StringVar(value="0")
        entry_4 = Entry(crop_window, textvariable=entry_4_text)
        entry_4.pack()

        confirm_button = Button(crop_window, text="Confirm", command=lambda:canvas.crop((int(entry_1_text.get()),int(entry_2_text.get()),int(entry_3_text.get()),int(entry_4_text.get()))))
        confirm_button.pack()

    def open_resize_window(self, canvas:CustomCanvas):
        resize_window = Toplevel(self)
        label_1_text = StringVar()
        label_1_text.set("Height")
        label_1 = Label(resize_window, textvariable=label_1_text)
        label_1.pack()
        entry_1_text = StringVar(value=f"{canvas.height}")
        entry_1 = Entry(resize_window, textvariable=entry_1_text)
        entry_1.pack()

        label_2_text = StringVar()
        label_2_text.set("Width")
        label_2 = Label(resize_window, textvariable=label_2_text)
        label_2.pack()
        entry_2_text = StringVar(value=f"{canvas.width}")
        entry_2 = Entry(resize_window, textvariable=entry_2_text)
        entry_2.pack()

        confirm_button = Button(resize_window, text="Confirm", command=lambda: canvas.resize(new_width = int(entry_2_text.get()), new_height = int(entry_1_text.get())))
        confirm_button.pack()

    def image_edit(self,opt:int,canvas:CustomCanvas):
        if opt <= 2:
            canvas.rotate(opt)
        elif opt <= 4:
            canvas.flip(opt)

    def gaussian(self, canvas):
        gaussian(canvas)

    def sobel(self, canvas):
        sobel(canvas)

    def binary(self,canvas):
        apply_binary_filter(canvas)

    def run(self):
        # Execute tkinter
        self.mainloop()



# Main Class
class Pigment:
    def __init__(self, XY):
        # Set dimensions of the main window
        self.canvas = None
        self.root = None
        self.x, self.y = XY

    def create_main_window(self):
        # Create main window object
        self.root = MainWindow((self.x,self.y), 'Pigment-PaintLite')
        self.canvas = CustomCanvas(self.root.canvas_frame)
        self.root.setup_menus(self.canvas, self)
        self.root.setup_main_frames(self.canvas)
        self.canvas.chose_tool(0)
        self.root.run()

def run1():
    screen = (700, 1000)
    program = Pigment(screen)
    program.create_main_window()

if __name__ == '__main__':
    run1()


