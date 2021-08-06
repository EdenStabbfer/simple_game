from pygame.sprite import Sprite
from pygame import Rect
from enum import Enum

from Settings import TILE_SIZE


class Tile:
    def __init__(self, wx, wy, id=0):
        super().__init__()
        self.rect = Rect(wx*TILE_SIZE, wy*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.id = id
        self.wx = wx
        self.wy = wy


class BlockType(Enum):
    NORMAL = 0
    HOVERED = 1
    SMOOTHED = 2
