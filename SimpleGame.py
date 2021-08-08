import pygame as pg

from Settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, ENABLE_CAMERA_SCROLL
from Engine.Map import Map
from Engine.Renderer import Renderer
from Player import Player
from EventHandler import EventHandler

# --------------------------------------------------------------------------
pg.init()
pg.display.set_caption('Simple Game')
event_handler = EventHandler()
clock = pg.time.Clock()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

player = Player(TILE_SIZE*30, 30*TILE_SIZE, TILE_SIZE, TILE_SIZE*2, 10)
game_map = Map(player, 'test', TILE_SIZE, 50)

event_handler.bind(player.key_down_event, pg.KEYDOWN)
event_handler.bind(player.key_up_event, pg.KEYUP)

half_width = WINDOW_WIDTH // 2
half_height = WINDOW_HEIGHT // 2
camera_scroll = [player.x, player.y]
true_camera_scroll = camera_scroll

renderer = Renderer(screen, true_camera_scroll)

# ---texture-loading-------
renderer.load_static_texture(1, './Textures/blocks/dirt.bmp')
renderer.load_static_texture(2, './Textures/blocks/grass.bmp')

# ----------------------game-cycle------------------------------------------
while True:
    event_handler.handle()

    if ENABLE_CAMERA_SCROLL:
        camera_scroll[0] += (player.x - camera_scroll[0]) // 10
        camera_scroll[1] += (player.y - camera_scroll[1]) // 10
        true_camera_scroll[0] = int(camera_scroll[0])
        true_camera_scroll[1] = int(camera_scroll[1])
    else:
        true_camera_scroll[0] += player.x - true_camera_scroll[0]
        true_camera_scroll[1] += player.y - true_camera_scroll[1]

    screen.fill((0, 0, 0))

    map_rects, map_ids = game_map.get_tiles_within_display()
    renderer.draw_map(map_rects, map_ids)

    player.update(map_rects)

    player.draw(screen, camera_scroll)
    pg.display.update()
    clock.tick(30)
