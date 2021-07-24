import pygame as pg

from Settings import WINDOW_WIDTH, WINDOW_HEIGHT, G, PLAYER_HEIGHT
from functions import collision_detection

half_width = WINDOW_WIDTH // 2
half_height = WINDOW_HEIGHT // 2 - PLAYER_HEIGHT + 10


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.rect = pg.Rect(self.x, self.y, size_x, size_y)
        self.image = None

        self.move_right = False
        self.move_left = False
        self.falling = True

        self.vx = 0
        self.vy = 0

    def update(self, map_tiles):
        if self.vy <= self.speed:
            self.vy += G
        self.vx = 0
        if self.move_right:
            self.vx = self.speed
        if self.move_left:
            self.vx = -self.speed

        self.move(self.vx, self.vy, map_tiles)

    def draw(self, surface: pg.Surface, scroll):
        pg.draw.rect(surface, (255, 255, 255), (self.x + half_width - scroll[0],
                                                self.y + half_height - scroll[1],
                                                self.size_x,
                                                self.size_y))

    def move(self, dx, dy, rects):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        if dx != 0:
            self.x += dx
            self.rect.x = int(self.x)
            collided_obj = collision_detection(self.rect, rects)
            for obj in collided_obj:
                if dx > 0:
                    self.x = obj.left - self.size_x
                    self.rect.right = obj.left
                    collision_types['right'] = True
                elif dx < 0:
                    self.x = obj.right
                    self.rect.left = obj.right
                    collision_types['left'] = True
        if dy != 0:
            self.y += dy
            self.rect.y = int(self.y)
            collided_obj = collision_detection(self.rect, rects)
            for obj in collided_obj:
                self.vy = 0
                if dy > 0:
                    self.y = obj.top - self.size_y
                    self.rect.bottom = obj.top
                    collision_types['bottom'] = True
                elif dy < 0:
                    self.y = obj.bottom
                    self.rect.top = obj.bottom
                    collision_types['top'] = True

    def key_down_event(self, event):
        if event.key == pg.K_d:
            self.move_right = True
        if event.key == pg.K_a:
            self.move_left = True
        if event.key == pg.K_SPACE:
            self.vy = -self.speed*2.2

    def key_up_event(self, event):
        if event.key == pg.K_d:
            self.move_right = False
        if event.key == pg.K_a:
            self.move_left = False
