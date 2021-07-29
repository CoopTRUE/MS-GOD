from PIL import Image
import numpy as np
from win32api import GetKeyState
from time import sleep
from pynput.mouse import Button, Controller

def rgb2lab ( inputColor ) :

   num = 0
   RGB = [0, 0, 0]

   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
   Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
   Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
   XYZ[ 0 ] = round( X, 4 )
   XYZ[ 1 ] = round( Y, 4 )
   XYZ[ 2 ] = round( Z, 4 )

   XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
   XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
   XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :

       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]

   L = ( 116 * XYZ[ 1 ] ) - 16
   a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
   b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

   Lab [ 0 ] = round( L, 4 )
   Lab [ 1 ] = round( a, 4 )
   Lab [ 2 ] = round( b, 4 )
   return Lab

mouse = Controller()

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
# print(data)

def get_mouse_click(message):

    print(message)
    while True:
        state_left = GetKeyState(0x01)
        if state_left == -127 or state_left == -128:
            while GetKeyState(0x01) not in {0, 1}:
                sleep(0.1)
            return mouse.position

def calibrate_colors():
    pos1 = get_mouse_click("Click the middle of the black square...")

    pos2 = get_mouse_click("Click the middle of the pink square...")

    xdifference = (pos2[0] - pos1[0]) / 10
    ydifference = xdifference
    return {
        color: (pos1[0] + (xdifference * (index - index%2)//2), pos1[1] + (index%2 * ydifference))

        for
            index, color
        in
            enumerate(DEFAULT_COLORS)
    }

def calibrate_position():
    pos1 = get_mouse_click("Click the top left of your canvas...")
    pos2 = get_mouse_click("Click the bottom right of your canvas...")
    width = pos2[0] - pos1[0]
    height = pos2[1] - pos1[1]

    return pos1, pos2, width, height

PALETTE_POS = calibrate_colors()
IMAGE_POS = calibrate_position()
print((IMAGE_POS[2], IMAGE_POS[3]))
image = image.resize((IMAGE_POS[2], IMAGE_POS[3]))
# image = image.convert('P', palette=[item for sublist in DEFAULT_COLORS for item in sublist], matrix=None)
data = np.asarray(image).copy()

from math import sqrt
def color_diff(color1, color2) -> float:
    color1 = rgb2lab(color1)
    color2 = rgb2lab(color2)
    a = (color2[0] - color1[0])**2
    b = (color2[1] - color1[1])**2
    c = (color2[2] - color1[2])**2
    return sqrt(a+b+c)

def convert_rgb(rgb, palette):
    return sorted(palette,
                key=lambda _color: color_diff(_color, rgb))[0]

new_data = []
for index, row in enumerate(data):
    new_data.append([])
    for rgb in row:
        new_data[-1].append(convert_rgb(rgb, DEFAULT_COLORS))
    print(f"LINE {index} DONE")

mouse.position = IMAGE_POS[0]
x, y = 0, 0
# last_rgb = None
for row in new_data:
    for rgb in row:
        # if rgb != last_rgb:
        # last_rgb = rgb
        mouse.position = PALETTE_POS[rgb]
        print(mouse.position)
        mouse.press(Button.left)
        mouse.release(Button.left)
        sleep(0.01)
        mouse.position = (IMAGE_POS[0][0] + x, IMAGE_POS[0][1] + y)
        mouse.press(Button.left)
        mouse.release(Button.left)
        x += 1
    y += 1
    x = 0
mouse.release(Button.left)