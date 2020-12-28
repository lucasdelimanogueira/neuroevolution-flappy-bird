import pygame
import os

class Ground:
    def __init__(self, y=365):
        self.IMG = pygame.image.load(os.path.join('images', 'ground.png'))
        self.VEL = 5
        self.WIDTH = self.IMG.get_width()

        self.y = y
        self.x1 = 0 # ground 1
        self.x2 = self.WIDTH # ground 2

    def move(self):

        # ground 1 and ground 2 in a row

        self.x1 -= self.VEL # move ground 1
        self.x2 -= self.VEL # move ground 2

        if self.x1 + self.WIDTH < 0: # when ground 1 leaves the screen, it goes behind ground 2
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0: # when ground 2 leaves the screen, it goes behind ground 1
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y)) # put ground 1 on the screen
        win.blit(self.IMG, (self.x2, self.y)) # put ground 2 on the screen
