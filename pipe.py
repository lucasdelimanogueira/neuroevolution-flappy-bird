import pygame
import os
import random

class Pipe:
    def __init__(self, x=250):

        self.PIPE_IMG = pygame.image.load(os.path.join('images', 'pipe.png'))
        self.GAP = 100 # gap entre cano superior e inferior
        self.VEL = 5

        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(25, 225)

        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top)) # coloca o cano superior na tela
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom)) # coloca o cano inferior na tela

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_pipe_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y)) # distancias (x,y) entre pássaro e top pipe
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) # distancias (x,y) entre pássaro e bottom pipe

        t_point = bird_mask.overlap(top_pipe_mask, top_offset) # ponto de colisão passáro-top_pipe
        b_point = bird_mask.overlap(bottom_pipe_mask, bottom_offset) # ponto de colisão pássario-bottom_pipe

        if t_point or b_point: # se existir um ponto de colisão
            return True

        return False