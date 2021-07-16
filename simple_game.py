import pygame as pg

from settings import WNDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE
from map import map_loader
from texture_manager import texture_loader

pg.init()
pg.display.set_caption('Simple Game')

screen = pg.display.set_mode((WNDOW_WIDTH, WINDOW_HEIGHT))

map = map_loader('map.txt')
textures = texture_loader('textures.png')

FIELD_WIDTH = len(map[0]) * TILE_SIZE
FIELD_HEIGHT = len(map) * TILE_SIZE
game_surf = pg.Surface((FIELD_WIDTH, FIELD_HEIGHT))
dif = WNDOW_WIDTH // FIELD_WIDTH

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    screen.fill((0, 0, 0))

    i = 0
    for row in map:
        j = 0
        for tile in row:
            if tile != '-':
                game_surf.blit(textures[int(tile)], (j*TILE_SIZE, i*TILE_SIZE))
            j += 1
        i += 1

    screen.blit(pg.transform.scale(game_surf, (FIELD_WIDTH*dif, FIELD_HEIGHT*dif)), (0, 0))

    pg.display.update()
