import cv2
class FileManager:
    def __init__(self):
        self.current_image=None
        self.previous_image=None
    def import_image(self, path:str):
        self.current_image=cv2.imread(path)
