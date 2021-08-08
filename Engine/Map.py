import pygame as pg
from pickle import dump, load
from math import ceil
import os

from Settings import WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_HEIGHT

"""
Карта делится на регионы, которые храняться в отдельных бинарных файлах 'reg.x.y'.bin

В самой игре одновременно храняться не более 4-х регионов 'NW': [], 'SW': [], 'NE': [], 'SE': []
Когда мы пересекаем границу следующего региона, регионы с противоположной стороны выгружаются, а с текущей загружаются
Изначально подгружается 4 региона и игрок появляется в 0, 0 (NW):
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
    def __init__(self, player, name, tile_size, region_size):
        self.name = name
        self.player = player
        self.tile_size = tile_size  # In pixels
        self.region_size = region_size  # In tiles

        if not os.path.isdir(f'Saves/{name}/region/'):
            os.makedirs(f'Saves/{name}/region/')

        self.cur_reg = (0, 0)  # В пределах мира
        self.cur_reg_mark = 'NW'
        self.regions = {'NW': [], 'SW': [], 'NE': [], 'SE': []}
        self.load_region(*self.cur_reg, 'NW')
        self.load_region(self.cur_reg[0], self.cur_reg[1] + 1, 'SW')
        self.load_region(self.cur_reg[0] + 1, self.cur_reg[1], 'NE')
        self.load_region(self.cur_reg[0] + 1, self.cur_reg[1] + 1, 'SE')

        self.wx_offset = ceil(WINDOW_WIDTH / tile_size) // 2  # Chunks visibility zone to left and right
        self.wy_offset = ceil(WINDOW_HEIGHT / tile_size) // 2  # Chunks visibility zone to up and down

    def update(self):
        # Изменять текущие позиции на карте
        pass

    def load_region(self, rx, ry, reg: str):
        try:
            reg_file = open(f'Saves/{self.name}/region/reg.{rx}.{ry}.bin', 'rb')
            self.regions[reg] = load(reg_file)
            reg_file.close()
        except FileNotFoundError:
            self.generate_region(rx, ry, reg)
            self.save_region(rx, ry, reg)

    def generate_region(self, rx, ry, reg: str):
        grass_level = 32
        region = [[0] * self.region_size for i in range(self.region_size)]
        for wy in range(self.region_size):
            for wx in range(self.region_size):
                # world generation here
                if wy + ry * self.region_size == grass_level:
                    region[wy][wx] = 2
                elif wy + ry * self.region_size >= grass_level:
                    region[wy][wx] = 1
        self.regions[reg] = region

    def get_tiles_within_display(self):
        w_coords = self.player.get_world_coords()
        new_reg = w_coords[0] // self.region_size, w_coords[1] // self.region_size

        if new_reg[0] > self.cur_reg[0]:
            self.cur_reg_mark = self.cur_reg_mark[0] + 'E'
        elif new_reg[0] < self.cur_reg[0]:
            self.cur_reg_mark = self.cur_reg_mark[0] + 'W'
        if new_reg[1] > self.cur_reg[1]:
            self.cur_reg_mark = 'S' + self.cur_reg_mark[1]
        elif new_reg[1] < self.cur_reg[1]:
            self.cur_reg_mark = 'N' + self.cur_reg_mark[1]

        self.cur_reg = new_reg

        left = w_coords[0] % self.region_size - self.wx_offset - 5
        right = w_coords[0] % self.region_size + self.wx_offset + 1 + 2
        top = w_coords[1] % self.region_size - self.wy_offset - 5
        bottom = w_coords[1] % self.region_size + self.wy_offset + 1 + 5

        is_crossed_left = left < 0
        is_crossed_right = right > self.region_size
        is_crossed_top = top < 0
        is_crossed_bottom = bottom > self.region_size

        if not (is_crossed_left or is_crossed_right or is_crossed_top or is_crossed_bottom):
            rects, ids = self.get_tiles(left, right, top, bottom, self.cur_reg_mark)
        else:  # Если пересекаемся с другими
            if self.cur_reg_mark == 'NW':
                if is_crossed_right and is_crossed_bottom:
                    rects, ids = self.get_tiles(left, self.region_size, top, self.region_size, self.cur_reg_mark)
                    rects_ne, ids_ne = self.get_tiles(0, right - self.region_size, top, bottom - self.region_size, 'NE', rx_offset=1)
                    rects_sw, ids_sw = self.get_tiles(left, self.region_size, 0, bottom - self.region_size, 'SW', ry_offset=1)
                    rects_se, ids_se = self.get_tiles(0, right - self.region_size, 0, bottom - self.region_size, 'SE', rx_offset=1, ry_offset=1)
                    rects.extend(rects_ne)
                    rects.extend(rects_sw)
                    rects.extend(rects_se)
                    ids.extend(ids_ne)
                    ids.extend(ids_sw)
                    ids.extend(ids_se)
                elif is_crossed_left and is_crossed_top:
                    self.regions['SE'] = self.regions['NW']
                    self.cur_reg_mark = 'SE'
                    self.load_region(self.cur_reg[0] - 1, self.cur_reg[1], 'SW')
                    self.load_region(self.cur_reg[0], self.cur_reg[1] - 1, 'NE')
                    self.load_region(self.cur_reg[0] - 1, self.cur_reg[1] - 1, 'NW')
                    rects, ids = self.get_tiles(0, right, 0, bottom, self.cur_reg_mark)
                elif is_crossed_left:
                    self.regions['NE'] = self.regions['NW']
                    self.regions['SE'] = self.regions['SW']
                    self.cur_reg_mark = 'NE'
                    self.load_region(self.cur_reg[0] - 1, self.cur_reg[1], 'NW')
                    self.load_region(self.cur_reg[0] - 1, self.cur_reg[1] + 1, 'SW')
                    rects, ids = self.get_tiles(0, right, top, bottom, self.cur_reg_mark)
                elif is_crossed_top:
                    self.regions['SW'] = self.regions['NW']
                    self.regions['SE'] = self.regions['NE']
                    self.cur_reg_mark = 'SW'
                    self.load_region(self.cur_reg[0], self.cur_reg[1] - 1, 'NW')
                    self.load_region(self.cur_reg[0] + 1, self.cur_reg[1] - 1, 'NE')
                    rects, ids = self.get_tiles(left, right, 0, bottom, self.cur_reg_mark)
                elif is_crossed_right:
                    rects, ids = self.get_tiles(left, self.region_size, top, bottom, self.cur_reg_mark)
                    rects_ne, ids_ne = self.get_tiles(0, right - self.region_size, top, bottom, 'NE', rx_offset=1)
                    rects.extend(rects_ne)
                    ids.extend(ids_ne)
                else:
                    rects, ids = self.get_tiles(left, right, top, self.region_size, self.cur_reg_mark)
                    rects_sw, ids_sw = self.get_tiles(left, right, 0, bottom - self.region_size, 'SW', ry_offset=1)
                    rects.extend(rects_sw)
                    ids.extend(ids_sw)
            elif self.cur_reg_mark == 'NE':
                if is_crossed_left and is_crossed_bottom:
                    rects, ids = self.get_tiles(0, right, top, self.region_size, self.cur_reg_mark)
                    rects_nw, ids_nw = self.get_tiles(self.region_size + left, self.region_size, top, 0, 'NW', rx_offset=-1)
                    rects_sw, ids_sw = self.get_tiles(self.region_size + left, self.region_size, 0, bottom - self.region_size, 'SW', rx_offset=-1, ry_offset=1)
                    rects_se, ids_se = self.get_tiles(0, right, 0, bottom - self.region_size, 'SE', ry_offset=1)
                    rects.extend(rects_nw)
                    rects.extend(rects_sw)
                    rects.extend(rects_se)
                    ids.extend(ids_nw)
                    ids.extend(ids_sw)
                    ids.extend(ids_se)
                elif is_crossed_right and is_crossed_top:
                    self.regions['SW'] = self.regions['NE']
                    self.cur_reg_mark = 'SW'
                    self.load_region(self.cur_reg[0], self.cur_reg[1] - 1, 'NW')
                    self.load_region(self.cur_reg[0] + 1, self.cur_reg[1] - 1, 'NE')
                    self.load_region(self.cur_reg[0] + 1, self.cur_reg[1], 'SE')
                    rects, ids = self.get_tiles(left, self.region_size, 0, bottom, self.cur_reg_mark)
                elif is_crossed_right:
                    self.regions['NW'] = self.regions['NE']
                    self.regions['SW'] = self.regions['SE']
                    self.cur_reg_mark = 'NW'
                    self.load_region(self.cur_reg[0] + 1, self.cur_reg[1], 'NE')
                    self.load_region(self.cur_reg[0] + 1, self.cur_reg[1] + 1, 'SE')
                    rects, ids = self.get_tiles(left, self.region_size, top, bottom, self.cur_reg_mark)
                elif is_crossed_top:
                    self.regions['SE'] = self.regions['NE']
                    self.regions['SW'] = self.regions['NW']
                    self.cur_reg_mark = 'SE'
                    self.load_region(self.cur_reg[0] - 1, self.cur_reg[1] - 1, 'NW')
                    self.load_region(self.cur_reg[0], self.cur_reg[1] - 1, 'NE')
                    rects, ids = self.get_tiles(left, right, 0, bottom, self.cur_reg_mark)
                elif is_crossed_left:
                    rects, ids = self.get_tiles(0, right, top, bottom, self.cur_reg_mark)
                    rects_nw, ids_nw = self.get_tiles(self.region_size + left, self.region_size, top, bottom, 'NW', rx_offset=-1)
                    rects.extend(rects_nw)
                    ids.extend(ids_nw)
                else:
                    rects, ids = self.get_tiles(left, right, top, self.region_size, self.cur_reg_mark)
                    rects_sw, ids_sw = self.get_tiles(left, right, 0, bottom - self.region_size, 'SE', ry_offset=1)
                    rects.extend(rects_sw)
                    ids.extend(ids_sw)
        return rects, ids

    def get_tiles(self, left, right, top, bottom, reg_name, rx_offset=0, ry_offset=0):
        rects = []
        ids = []
        for wy in range(top, bottom):
            for wx in range(left, right):
                if self.regions[reg_name][wy][wx] != 0:
                    real_wx = wx + (self.cur_reg[0] + rx_offset) * self.region_size
                    real_wy = wy + (self.cur_reg[1] + ry_offset) * self.region_size
                    rects.append(pg.Rect(real_wx * self.tile_size,
                                         real_wy * self.tile_size,
                                         self.tile_size,
                                         self.tile_size))
                    ids.append(self.regions[reg_name][wy][wx])
        return rects, ids

    def save_region(self, rx, ry, reg: str):
        reg_file = open(f'Saves/{self.name}/region/reg.{rx}.{ry}.bin', 'wb')
        dump(self.regions[reg], reg_file)
        reg_file.close()
