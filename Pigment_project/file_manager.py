import cv2
import tkinter as tk
from PIL import Image
class FileManager:
    def __init__(self):
        self.current_image=Image.new("RGB", (500,500), "white")
        self.current_path=None
    def import_image(self, path:str):
        self.current_image=Image.open(path)
        self.current_path=path
    def save(self):
        if self.current_path is not None:
            self.current_image.save(self.current_path)
