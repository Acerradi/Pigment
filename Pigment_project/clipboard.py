from PIL import Image

from Pigment_project.canvas import CustomCanvas


def cut(canvas:CustomCanvas):
    overlay = canvas.extracted_area
    start_pos = canvas.extracted_position
    if overlay and start_pos:
        canvas.history.append(canvas.file_manager.current_image.copy())
        blank = Image.new("RGB", overlay.size, "white")
        canvas.file_manager.current_image.paste(blank, start_pos)
        canvas.display_image_on_canvas()
        canvas.clipboard = True
        canvas.cut = True
def copy_clipboard(canvas:CustomCanvas):
    overlay = canvas.extracted_area
    start_pos = canvas.extracted_position
    if overlay and start_pos:
        canvas.clipboard = True