import os
import pygame
import sys

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, color_key=None):
    fullname = os.path.join('Assets', 'Graphics', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image
