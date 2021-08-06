from Engine.Tile import Tile, BlockType


class Dirt(Tile):
    def __init__(self, surf, wx, wy):
        super().__init__(surf, wx, wy)
        self.type = BlockType.NORMAL
        self.id = 0
        self.texture = 'dirt.png'