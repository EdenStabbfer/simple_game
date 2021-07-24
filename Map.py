import pygame as pg
from Settings import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_HEIGHT, ORIGINAL_TILE_SIZE

half_width = WINDOW_WIDTH // 2
half_height = WINDOW_HEIGHT // 2 - PLAYER_HEIGHT


class Map:
    def __init__(self, map_fn, textures_fn):
        self.map = self.load(map_fn)
        self.tile_rects = self.get_tiles_rects()
        self.textures = self.texture_loader(textures_fn)
        self.width = len(self.map[0])
        self.height = len(self.map)

    @staticmethod
    def load(file_name):
        map_mass = []
        file = open(file_name, 'r')
        for row in file.read().split('\n'):
            map_mass.append(row)
        return map_mass

    def draw(self, surface, scroll):
        y = 0
        for row in self.map:
            x = 0
            for tile in row:
                if tile != '-':
                    surface.blit(self.textures[int(tile)], (x * TILE_SIZE + half_width - scroll[0],
                                                      y * TILE_SIZE + half_height - scroll[1]))
                x += 1
            y += 1

    def get_tiles_rects(self):
        rects = []
        y = 0
        for row in self.map:
            x = 0
            for tile in row:
                if tile != '-':
                    rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1
        return rects
        # wx = int(object.x // TILE_SIZE)
        # wy = int(object.y // TILE_SIZE)
        # start_x = wx - 1 if wx - 1 >= 0 else 0
        # end_x = wx + 1 if wx + 1 <= self.width else self.width
        # start_y = wy - 1 if wy - 1 >= 0 else 0
        # end_y = wy + 1 if wy + 1 <= self.height else self.height
        # for i in range(start_y, end_y + 1):
        #     for j in range(start_x, end_x + 1):
        #         if self.map[i][j] != '-' and object.rect.colliderect((j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)):
        #             return j, i

    @staticmethod
    def texture_loader(file_name):
        img = pg.image.load(file_name).convert_alpha()
        textures = []
        for i in range(9):
            for j in range(3):
                tile = pg.Surface((ORIGINAL_TILE_SIZE, ORIGINAL_TILE_SIZE), pg.SRCALPHA)
                tile.blit(img, (-j * ORIGINAL_TILE_SIZE - 2 * j, -i * ORIGINAL_TILE_SIZE - 2 * i))
                tile = pg.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                textures.append(tile)
        return textures