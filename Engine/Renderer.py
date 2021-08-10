import pygame as pg
from Settings import TILE_SIZE, HALF_WIDTH, HALF_HEIGHT


class Renderer:
    def __init__(self, surface: pg.Surface, camera_scroll):
        self.surface = surface
        self.camera_scroll = camera_scroll

        self.textures = {}
        self.unknown_texture_color = pg.Color(128, 0, 128)
        self.highlighted_block_color = pg.Color(255, 255, 30, 70)

    # TODO: Перенести всю отрисовку сюда

    def load_static_texture(self, id, path):
        img = pg.image.load(path).convert_alpha()
        tile = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.textures[id] = tile

    def draw_map(self, rects, ids):
        for i in range(len(rects)):
            if ids[i] in self.textures:
                self.surface.blit(self.textures[ids[i]],
                                  (rects[i].x + HALF_WIDTH - self.camera_scroll[0],
                                   rects[i].y + HALF_HEIGHT - self.camera_scroll[1]))
            else:
                pg.draw.rect(self.surface,
                             self.unknown_texture_color,
                             (rects[i].x + HALF_WIDTH - self.camera_scroll[0],
                              rects[i].y + HALF_HEIGHT - self.camera_scroll[1],
                              rects[i].width, rects[i].height))
                pg.draw.rect(self.surface,
                             (255, 0, 0),
                             (rects[i].x + HALF_WIDTH - self.camera_scroll[0],
                              rects[i].y + HALF_HEIGHT - self.camera_scroll[1],
                              rects[i].width, rects[i].height), 2)

    def draw_highlighted_block(self, x, y, border_width=2):
        x -= self.camera_scroll[0]
        y -= self.camera_scroll[1]
        s = pg.Surface((TILE_SIZE - 2*border_width, TILE_SIZE - 2*border_width), pg.SRCALPHA, 32)
        s.fill(self.highlighted_block_color)  # notice the alpha value in the color
        self.surface.blit(s, (x + border_width, y + border_width))
        pg.draw.rect(self.surface, self.highlighted_block_color, (x, y, TILE_SIZE, TILE_SIZE), border_width, 3)
