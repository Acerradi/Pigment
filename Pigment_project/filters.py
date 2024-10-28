from PIL import Image, ImageFilter
import numpy as np
import cv2
from canvas import CustomCanvas
def pillow_2_cv2(pillow_image:Image):
    # Convert the Pillow image to RGB (in case it's not)
    if pillow_image.mode != 'RGB':
        pillow_image = pillow_image.convert('RGB')

    # Convert the Pillow image to a NumPy array
    opencv_image = np.array(pillow_image)

    # Convert RGB to BGR format for OpenCV
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
    return opencv_image
def cv2_2_pillow(opencv_image):
    # Convert the image from BGR to RGB
    rgb_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

    # Convert the NumPy array to a Pillow image
    pillow_image = Image.fromarray(rgb_image)
    return pillow_image
def gaussian(root:CustomCanvas):
    image = root.file_manager.current_image
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=2))
    root.file_manager.current_image = blurred_image
    root.display_image_on_canvas()


def sobel(root: CustomCanvas):
    # Get the current image in Pillow format
    pillow_image = root.file_manager.current_image

    # Convert Pillow image to OpenCV format
    image = pillow_2_cv2(pillow_image)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply the Sobel filter
    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)  # Sobel in X direction
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)  # Sobel in Y direction

    # Calculate the magnitude of gradients
    sobel_magnitude = cv2.magnitude(sobel_x, sobel_y)

    # Normalize the magnitude to range 0-255 and convert to uint8 for display
    sobel_magnitude = np.uint8(cv2.normalize(sobel_magnitude, None, 0, 255, cv2.NORM_MINMAX))

    # Convert the processed image to a Pillow image and update the canvas
    root.file_manager.current_image = cv2_2_pillow(sobel_magnitude)
    root.display_image_on_canvas()


def apply_binary_filter(root:CustomCanvas, threshold=128):
    # Convert Pillow image to OpenCV format (BGR)
    pillow_image = root.file_manager.current_image
    cv2_image = cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    # Convert back to Pillow format
    root.file_manager.current_image = Image.fromarray(binary_image)
    root.display_image_on_canvas()