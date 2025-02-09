import os
import pygame
import pytmx
import sys
import json

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

def get_enemies():
    with open("enemies.json", 'r') as file:
        return(json.load(file))

def get_collision_rects(tmx_map, layer_index):
    collision_rects = []
    layers = list(tmx_map.visible_layers)
    layer = layers[layer_index]
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_map.get_tile_image_by_gid(gid)
            if tile:
                rect = pygame.Rect(x * 16, y * 16, 16, 16)  # Используем 16x16 для коллизий
                collision_rects.append(rect)
    return collision_rects


