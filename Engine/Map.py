import pygame as pg
from pickle import dump, load
from math import ceil
import os

from Settings import WINDOW_WIDTH, WINDOW_HEIGHT

"""
Карта делится на регионы, которые храняться в отдельных бинарных файлах 'reg.x.y'.bin

В самой игре одновременно храняться не более 4-х регионов 'NW': [], 'SW': [], 'NE': [], 'SE': []
Когда мы пересекаем границу следующего региона, регионы с противоположной стороны выгружаются, а с текущей загружаются
Изначально подгружается 4 региона и игрок появляется в середине (NW):
+--------+--------+--
|p       |        |
|        |        |
+--------+--------+--
|        |        |
|        |        |
+--------+--------+--
|        |        |

"""


class Map:
    def __init__(self, name, tile_size, chunk_size, region_size):
        self.name = name
        self.tile_size = tile_size  # In pixels
        self.chunk_size = chunk_size  # In tiles
        self.region_size = region_size  # In chunks

        if not os.path.isdir(f'Saves/{name}/region/'):
            os.makedirs(f'Saves/{name}/region/')

        self.n_tiles_in_region = self.chunk_size * self.region_size
        self.real_reg_size = self.n_tiles_in_region * self.tile_size

        self.cur_chunk = (0, 0)  # В пределах одного региона
        self.cur_reg = (0, 0)  # В пределах мира
        self.cur_reg_mark = 'NW'
        self.regions = {'NW': self.load_region(*self.cur_reg),
                        'SW': self.load_region(self.cur_reg[0], self.cur_reg[1] + 1),
                        'NE': self.load_region(self.cur_reg[0] + 1, self.cur_reg[1]),
                        'SE': self.load_region(self.cur_reg[0] + 1, self.cur_reg[1] + 1)}

        self.wx_chunk_offset = ceil(
            WINDOW_WIDTH / (tile_size * chunk_size)) // 2  # Chunks visibility zone to left and right
        self.wy_chunk_offset = ceil(
            WINDOW_HEIGHT / (tile_size * chunk_size)) // 2  # Chunks visibility zone to up and down

    def update(self, player):
        # Изменять текущие позиции на карте
        w_coords = player.get_world_coords()
        self.cur_chunk = (w_coords[0] // self.chunk_size) % self.region_size, \
                         (w_coords[1] // self.chunk_size) % self.region_size
        self.cur_reg = w_coords[0] // self.n_tiles_in_region, \
                       w_coords[1] // self.n_tiles_in_region

    def load_region(self, rx, ry):
        region = []
        try:
            reg_file = open(f'Saves/{self.name}/region/reg.{rx}.{ry}.bin', 'rb')
            region = load(reg_file)
            reg_file.close()
        except FileNotFoundError:
            region = self.generate_region(rx, ry)
            self.save_region(region, rx, ry)
        return region

    def generate_region(self, rx, ry):
        grass_level = 40
        region = [[0] * self.n_tiles_in_region for i in range(self.n_tiles_in_region)]
        for wy in range(self.n_tiles_in_region):
            for wx in range(self.n_tiles_in_region):
                # world generation here
                if wy + ry * self.n_tiles_in_region == grass_level:
                    region[wy][wx] = 2
                elif wy + ry * self.n_tiles_in_region >= grass_level:
                    region[wy][wx] = 1
        return region

    def get_tiles(self):
        left = (self.cur_chunk[0] - self.wx_chunk_offset) * self.chunk_size
        right = (self.cur_chunk[0] + self.wx_chunk_offset + 1) * self.chunk_size
        top = (self.cur_chunk[1] - self.wy_chunk_offset) * self.chunk_size
        bottom = (self.cur_chunk[1] + self.wy_chunk_offset + 1) * self.chunk_size

        is_crossed_left = left < 0
        is_crossed_right = right > self.n_tiles_in_region
        is_crossed_top = top < 0
        is_crossed_bottom = bottom > self.n_tiles_in_region

        rects = []
        ids = []
        if not(is_crossed_left or is_crossed_right or is_crossed_top or is_crossed_bottom):
            for wy in range(top, bottom):
                for wx in range(left, right):
                    if self.regions[self.cur_reg_mark][wy][wx] != 0:
                        real_wx = wx + self.cur_reg[0] * self.n_tiles_in_region
                        real_wy = wy + self.cur_reg[1] * self.n_tiles_in_region
                        rects.append(pg.Rect(real_wx*self.tile_size, real_wy*self.tile_size, self.tile_size, self.tile_size))
                        ids.append(self.regions[self.cur_reg_mark][wy][wx])
        else:
            # TODO: Прописать пограничные моменты
            pass
        return rects, ids

    def save_region(self, region, rx, ry):
        reg_file = open(f'Saves/{self.name}/region/reg.{rx}.{ry}.bin', 'wb')
        dump(region, reg_file)
        reg_file.close()
