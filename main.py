from PIL import Image
import numpy as np

COLORS = (
    (255, 0, 0),
    (0, 0, 255)
)
IMAGE_FILE_NAME = 'SF_Bridge.jpg'

image = Image.open(IMAGE_FILE_NAME)
data = np.asarray(image).copy()
print(data)