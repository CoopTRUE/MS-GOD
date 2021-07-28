from PIL import Image
import numpy as np
from itertools import cycle

DEFAULT_COLORS = (
    (0, 0, 0),
    (255, 255, 255),
    (127, 127, 127),
    (195, 195, 195),
    (136, 0, 21),
    (185, 122, 87),
    (237, 28, 36),
    (255, 174, 201),
    (255, 127, 39),
    (255, 201, 14),
    (255, 242, 0),
    (239, 228, 176),
    (34, 177, 76),
    (181, 230, 29),
    (0, 162, 232),
    (153, 217, 234),
    (63, 72, 204),
    (112, 146, 190),
    (163, 73, 164),
    (200, 191, 231),
)

IMAGE_FILE_NAME = 'SF_Bridge.jpg'

image = Image.open(IMAGE_FILE_NAME)
data = np.asarray(image).copy()
# print(data)

def get_mouse_click():
    import win32api
    from time import sleep
    while True:
        state_left = win32api.GetKeyState(0x01)
        if state_left == -127 or state_left == -128:
            while win32api.GetKeyState(0x01) not in {0, 1}:
                sleep(0.1)
            return win32api.GetCursorPos()

def calibrate_colors():
    import win32api, win32gui

    print("Click the middle of the black square...")
    pos1 = get_mouse_click()

    print("Click the middle of the gray square...")
    pos2 = get_mouse_click()

    xdifference = pos2[0] - pos1[0]
    ydifference = pos2[1] - pos1[1]
    return {
        color: (pos1[0] + (xdifference * (index - index%2)//2), pos1[1] + (index%2 * ydifference))

        for
            index, color
        in
            enumerate(DEFAULT_COLORS)
    }

COLORS = calibrate_colors()