import pygame
from math import sin, cos, degrees
from shot import Shot
from random import randrange


class Tank:
    def __init__(self, x, y, width, height, color):
        self.posX = x
        self.posY = y
        self.rot = 0
        self.width = width
        self.height = height
        self.color = color
        self.vel = 3
        self.rotVel = 0.05
        self.delay = 0
        self.points = 0
        self.is_hit = False

    def draw(self, win, image):
        rotated_image = pygame.transform.rotate(image, degrees(-self.rot))
        img_pos = (self.posX - rotated_image.get_width() / 2, self.posY - rotated_image.get_height() / 2)

        rotated_image.fill(self.color, special_flags=pygame.BLEND_ADD)

        win.blit(rotated_image, img_pos)

    def make_commands(self):
        keys = pygame.key.get_pressed()
        commands = []
        vel = 0
        rot = 0

        if self.delay <= 0:
            if keys[pygame.K_SPACE]:
                commands.append(("shoot", None))

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            rot = -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            rot = 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vel = 1

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vel = -1

        if vel != 0 or rot != 0:
            commands.append(("move_tank", (vel, rot)))

        return commands

    def move(self, vel, rot):
        if not self.is_hit:
            if abs(rot) == 1:
                self.rot += rot * self.rotVel

            if abs(vel) == 1:
                moveX = self.posX + vel * sin(self.rot) * self.vel
                moveY = self.posY - vel * cos(self.rot) * self.vel
                if 30 < moveX < 770:
                    self.posX = moveX
                if 30 < moveY < 570:
                    self.posY = moveY

    def shot(self, tank_id):
        if not self.is_hit:
            if self.delay <= 0:
                self.delay = 20
                return Shot(self.posX + sin(self.rot) * 30, self.posY + cos(self.rot) * -30, tank_id, self.rot)

    def hit(self):
        self.is_hit = True
        self.delay = 200

    def wait(self):
        if self.delay <= 0:
            self.is_hit = False
            self.posX = randrange(100, 400)
            self.posY = randrange(100, 400)

    def tank_loop(self):
        if self.delay > 0:
            self.delay -= 1
        if self.is_hit:
            self.wait()
