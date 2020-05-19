import pygame
import os

class Base:
    def __init__(self, y=365):
        self.IMG = pygame.image.load(os.path.join('images', 'base.png'))
        self.VEL = 5
        self.WIDTH = self.IMG.get_width()

        self.y = y
        self.x1 = 0 # base 1
        self.x2 = self.WIDTH # base 2

    def move(self):

        # base 1 e base 2 enfileirados

        self.x1 -= self.VEL # move base 1
        self.x2 -= self.VEL # move base 2

        if self.x1 + self.WIDTH < 0: # quando base 1 sair da tela, vai para trás d1 base 2
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0: # quando base 2 sair da tela, vai para trás de base 1
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y)) # coloca base 1 na tela
        win.blit(self.IMG, (self.x2, self.y)) # coloca base 2 na tela