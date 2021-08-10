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

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.DOUBLEBUF, 32)

player = Player(0, 0, TILE_SIZE, TILE_SIZE*2, 10)
game_map = Map(player, 'test', TILE_SIZE, 50)

camera_scroll = [player.x, player.y]
true_camera_scroll = camera_scroll

renderer = Renderer(screen, true_camera_scroll)

# ---texture-loading-------
renderer.load_static_texture(1, './Textures/blocks/dirt.bmp')
renderer.load_static_texture(2, './Textures/blocks/grass.bmp')


# ----------------------game-cycle------------------------------------------
while True:
    if ENABLE_CAMERA_SCROLL:
        camera_scroll[0] += (player.x - camera_scroll[0]) // 10
        camera_scroll[1] += (player.y - camera_scroll[1]) // 10
        true_camera_scroll[0] = int(camera_scroll[0])
        true_camera_scroll[1] = int(camera_scroll[1])
    else:
        true_camera_scroll[0] += player.x - true_camera_scroll[0]
        true_camera_scroll[1] += player.y - true_camera_scroll[1]

    mouse_pos = pg.mouse.get_pos()
    pointer_x = (true_camera_scroll[0] + mouse_pos[0]) // TILE_SIZE * TILE_SIZE
    pointer_y = (true_camera_scroll[1] + mouse_pos[1]) // TILE_SIZE * TILE_SIZE

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            player.key_down_event(event)
        if event.type == pg.KEYUP:
            player.key_up_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                game_map.remove_block(pointer_x, pointer_y)
            if event.button == 3:
                game_map.put_block(pointer_x, pointer_y, 1)

    screen.fill((35, 30, 70))

    map_rects, map_ids = game_map.get_tiles_within_display()
    renderer.draw_map(map_rects, map_ids)
    renderer.draw_highlighted_block(pointer_x, pointer_y)

    player.update(map_rects)

    player.draw(screen, camera_scroll)
    pg.display.update()
    clock.tick(30)
