import math

import pygame
from math import sin, cos, degrees


class Shot:
    def __init__(self, x, y, tank_id, rot):
        self.posX = x
        self.posY = y
        self.tank_id = tank_id
        self.rot = rot
        self.vel = 6

    def draw(self, win, image):
        rotated_image = pygame.transform.rotate(image, degrees(-self.rot))
        img_pos = (self.posX - rotated_image.get_width() / 2, self.posY - rotated_image.get_height() / 2)
        rotated_image.fill('red', special_flags=pygame.BLEND_ADD)
        win.blit(rotated_image, img_pos)

    def move(self):
        self.posX += sin(self.rot) * self.vel
        self.posY -= cos(self.rot) * self.vel
        return 0 < self.posX < 800 and 0 < self.posY < 600

    def did_hit_tank(self, tank):
        return math.sqrt((self.posX - tank.posX)**2 + (self.posY - tank.posY)**2) < 25
