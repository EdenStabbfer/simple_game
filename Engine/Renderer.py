import pygame as pg
from Settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, PLAYER_HEIGHT

half_width = WINDOW_WIDTH // 2
half_height = WINDOW_HEIGHT // 2 - PLAYER_HEIGHT


class Renderer:
    def __init__(self, surface: pg.Surface, camera_scroll):
        self.surface = surface
        self.camera_scroll = camera_scroll

        self.textures = {}
        self.unknown_texture_color = pg.Color(128, 0, 128)

    def load_static_texture(self, id, path):
        img = pg.image.load(path).convert_alpha()
        tile = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.textures[id] = tile

    def draw_map(self, rects, ids):
        for i in range(len(rects)):
            if ids[i] in self.textures:
                self.surface.blit(self.textures[ids[i]],
                                  (rects[i].x + half_width - self.camera_scroll[0],
                                   rects[i].y + half_height - self.camera_scroll[1]))
            else:
                pg.draw.rect(self.surface,
                             self.unknown_texture_color,
                             (rects[i].x + half_width - self.camera_scroll[0],
                              rects[i].y + half_height - self.camera_scroll[1],
                              rects[i].width, rects[i].height))
                pg.draw.rect(self.surface,
                             (255, 0, 0),
                             (rects[i].x + half_width - self.camera_scroll[0],
                              rects[i].y + half_height - self.camera_scroll[1],
                              rects[i].width, rects[i].height), 2)