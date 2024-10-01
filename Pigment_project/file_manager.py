import cv2
import tkinter as tk
from PIL import Image
class FileManager:
    def __init__(self):
        self.current_image=Image.new("RGB", (500,500), "white")
    def import_image(self, path:str):
        self.current_image=Image.open(path)

