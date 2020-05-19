import pygame
from neural_network import MLP
import random
import os

class Bird:
    def __init__(self, x=115, y=175):
        self.MAX_ROTATION = 25
        self.ROT_VEL = 20
        self.ANIMATION_TIME = 5
        self.IMGS = [pygame.image.load(os.path.join('images', 'bird1.png')),
             pygame.image.load(os.path.join('images', 'bird2.png')),
             pygame.image.load(os.path.join('images', 'bird3.png'))]

        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0 # contagem de clock auxiliar para calcular movimento de pulo
        self.y_vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.is_alive = True

        self.distance_x_next_pipe = 0
        self.distance_y_next_pipe = 0
        self.brain = MLP([2, 2, 1])

        self.fitness = 0.1

    def jump(self):
        self.y_vel = -10.5 # pássaro com velocidade para cima (ref 0,0 -> top left)
        self.tick_count = 0 # zera contagem de tempo
        self.height = self.y # altura em que o pássaro pulou

    def move(self):

        if self.is_alive:
            self.tick_count += 1 # quantos clocks desde o último pulo

            if self.brain.feedforward([[self.distance_x_next_pipe], [self.distance_y_next_pipe]]) > 0.5:
                self.jump()

            d = self.y_vel * self.tick_count + 1.5 * self.tick_count**2 # d = voT + aT^2/2

            # limitar para nao cair muito rápido
            if d >= 16:
                d = 16

            # simular um impulso de pulo
            if d <= 0:
                d -= 2

            self.y = self.y + d # s = so + voT + aT^2/2

            if d < 0 or self.y < self.height + 50: # se estiver pulando ou até um pouco depois do pulo
                if self.tilt < self.MAX_ROTATION: # angula o pássaro
                    self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90: # limita angulação máxima
                    self.tilt -= self.ROT_VEL # vai diminuindo angulação do pássaro

        else:
            self.x -= 5

    def draw(self, win):
        self.img_count += 1

        # simular um "GIF" para animação do pássaro batendo asas
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # se estiver pulando (inclinado) não bater asas
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotacionar imagem de acordo com self.inclinação
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # alterar referencia para rotacionar imagem em torno do centro
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img) # bordas de colisão


    def mutate(self, mutation_rate):
        for c, W in enumerate(self.brain.weights): # para cada matrix de conexões
            for j, neuron_weights_connections in enumerate(W): # para cada neuronio j
                for k, weight in enumerate(neuron_weights_connections): # para cada peso wjk
                    if random.random() < mutation_rate:  # mutação com probabilidade mutation_rate
                        new_weight = weight * 4*(random.random() - 0.5) # soma weight por valor entre -2 e 2
                        self.brain.weights[c][j][k] = new_weight # substitui o novo gene (weight)

        for l, B in enumerate(self.brain.biases): # para cada layer
            for j, bias in enumerate(B): # para cada neuronio j
                if random.random() < mutation_rate: #mutação com probabilidade mutation_rate
                    new_biases = bias[0] * 4*(random.random() - 0.5) # multiplica bias por valor entre -2 e 2
                    self.brain.biases[l][j][0] = new_biases # substitui o novo gene (bias)

    @staticmethod
    def cross_over(partner_a, partner_b):
        child = Bird()

        #cross over weights
        for c, W in enumerate(partner_a.brain.weights): # para cada matrix de conexões
            for j, neuron_weights_connections in enumerate(W): # para cada neuronio j
                for k, weight in enumerate(neuron_weights_connections): # para cada peso wjk

                    #child = partner_a + rand(partner_b - partner_a)
                    child.brain.weights[c][j][k] = partner_a.brain.weights[c][j][k] \
                                                   + random.random()*(partner_b.brain.weights[c][j][k] - \
                                                           partner_a.brain.weights[c][j][k])

        #cross over biases
        for l, B in enumerate(partner_a.brain.biases): # para cada layer
            for j, bias in enumerate(B): # para cada neuronio j

                # child = partner_a + rand(partner_b - partner_a)
                child.brain.biases[l][j][0] = partner_a.brain.biases[l][j][0] \
                                               + random.random() * (partner_b.brain.weights[l][j][0] - \
                                                                    partner_a.brain.weights[l][j][0])

        return child