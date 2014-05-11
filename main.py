import sys
import curses
import pygame
import signal
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()

# Create a low resolution camera object (assumed to be at /dev/video0)
CAM = pygame.camera.Camera("/dev/video0", (40, 30))
CAM.start()

def print_image(image):
    '''
    Convert the parm image RGB value into a black and white value (average of
    red, green, and blue) then assign a corresponding character to represent
    this shade of grey.
    '''
    string_image = ''
    for row in range(image.get_height()):
        for col in range(image.get_width()):
            val = reduce(lambda x, y: x+y, image.get_at((col, row))[:3]) / 3
            if val < 32:
                val = ' '
            elif val < 64:
                val = '.'
            elif val < 128:
                val = '*'
            else:
                val = '#'
            string_image += str(val)
        string_image += '\n'
    return string_image

def main():
    '''
    Initialize curses as a blank canvas. Continuously capture camera images,
    convert them into a string 2D array, and print them to the canvas.
    '''
    screen = curses.initscr()
    while True:
        img = print_image(CAM.get_image())
        try:
            screen.addstr(0, 0, img)
        except Exception:
            pass
        screen.refresh()

def shutdown(signal, frame):
    '''
    Capture SIGINT to ensure that curses is shut down appropriately (if this
    isn't done, the terminal will be all sorts of messed up once the program
    terminates).
    '''
    curses.endwin()
    sys.exit(0)
        
if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown)
    main()
