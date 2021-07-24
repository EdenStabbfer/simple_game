import pygame as pg

from Settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, ENABLE_CAMERA_SCROLL
from Map import Map
from Player import Player
from EventHandler import EventHandler

# --------------------------------------------------------------------------
pg.init()
pg.display.set_caption('Simple Game')
event_handler = EventHandler()
clock = pg.time.Clock()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map('map.txt', 'textures.png')

player = Player(TILE_SIZE*3, -TILE_SIZE, TILE_SIZE, TILE_SIZE*2, 10)
event_handler.bind(player.key_down_event, pg.KEYDOWN)
event_handler.bind(player.key_up_event, pg.KEYUP)

half_width = WINDOW_WIDTH // 2
half_height = WINDOW_HEIGHT // 2
camera_scroll = [0, 0]
true_camera_scroll = camera_scroll

# ----------------------game-cycle------------------------------------------
while True:
    event_handler.handle()

    if ENABLE_CAMERA_SCROLL:
        camera_scroll[0] += (player.x - camera_scroll[0]) / 20
        camera_scroll[1] += (player.y - camera_scroll[1]) / 20
        true_camera_scroll = [int(camera_scroll[0]), int(camera_scroll[1])]
    else:
        true_camera_scroll = [player.x - camera_scroll[0], player.y - camera_scroll[1]]

    screen.fill((0, 0, 0))

    player.update(map.tile_rects)

    player.draw(screen, true_camera_scroll)
    map.draw(screen, true_camera_scroll)
    pg.display.update()
    clock.tick(30)
