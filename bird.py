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
        self.tick_count = 0 # auxiliary clock counting to manage the jumping movement
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
        self.y_vel = -10.5 # bird with upward speed (screen pixel reference 0,0 -> top left)
        self.tick_count = 0 # reset clock
        self.height = self.y # height the bird jumped

    def move(self):

        if self.is_alive:
            self.tick_count += 1 # clock counting since last jump

            if self.brain.feedforward([[self.distance_x_next_pipe], [self.distance_y_next_pipe]]) > 0.5:
                self.jump()

            d = self.y_vel * self.tick_count + 1.5 * self.tick_count**2 # s = voT + aT^2/2

            # limit to do not fall too fast
            if d >= 16:
                d = 16

            # simulate impulse during jump
            if d <= 0:
                d -= 2

            self.y = self.y + d # s = so + voT + aT^2/2

            if d < 0 or self.y < self.height + 50: # if already jumping or a little after the jump
                if self.tilt < self.MAX_ROTATION: # angles the bird
                    self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90: # max angle limit
                    self.tilt -= self.ROT_VEL # decreases the bird angle

        else:
            self.x -= 5

    def draw(self, win):
        self.img_count += 1

        # simulate a "GIF" to animate the bird flapping wings
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

        # if jumping (inclined) do not flap wings
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotate image according to inclination
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # change reference to rotate image around the center
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img) # collision edges


    def mutate(self, mutation_rate):
        for c, W in enumerate(self.brain.weights): # for each weight matrix
            for j, neuron_weights_connections in enumerate(W): # for each neuron j
                for k, weight in enumerate(neuron_weights_connections): # for each weight w_jk
                    if random.random() < mutation_rate:  # mutation with probability mutation_rate
                        new_weight = weight * 4*(random.random() - 0.5) # multiply weight with value between -2 and 2
                        self.brain.weights[c][j][k] = new_weight # replaces new gene (weight)

        for l, B in enumerate(self.brain.biases): # for each bias matrix
            for j, bias in enumerate(B): # for each neuron j
                if random.random() < mutation_rate: # mutation with probability mutation_rate
                    new_biases = bias[0] * 4*(random.random() - 0.5) # multiply bias with value between -2 and 2
                    self.brain.biases[l][j][0] = new_biases # replaces the new gene (bias)

    @staticmethod
    def cross_over(partner_a, partner_b):
        child = Bird()

        # weights crossover
        for c, W in enumerate(partner_a.brain.weights): # for each weights matrix
            for j, neuron_weights_connections in enumerate(W): # for each neuron j
                for k, weight in enumerate(neuron_weights_connections): # for each weight w_jk

                    #child = partner_a + rand(partner_b - partner_a)
                    child.brain.weights[c][j][k] = partner_a.brain.weights[c][j][k] \
                                                   + random.random()*(partner_b.brain.weights[c][j][k] - \
                                                           partner_a.brain.weights[c][j][k])

        # biases crossover
        for l, B in enumerate(partner_a.brain.biases): # for each bias matrix
            for j, bias in enumerate(B): # para cada neuronio j

                # child = partner_a + rand(partner_b - partner_a)
                child.brain.biases[l][j][0] = partner_a.brain.biases[l][j][0] \
                                               + random.random() * (partner_b.brain.weights[l][j][0] - \
                                                                    partner_a.brain.weights[l][j][0])

        return child
