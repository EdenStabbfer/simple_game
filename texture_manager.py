import pygame as pg

from settings import TILE_SIZE


def texture_loader(file_name):
    img = pg.image.load(file_name).convert_alpha()
    textures = []
    for i in range(9):
        for j in range(3):
            tile = pg.Surface((TILE_SIZE, TILE_SIZE))
            tile.blit(img, (-j*TILE_SIZE - 2*j, -i*TILE_SIZE - 2*i))
            textures.append(tile)
    return textures
