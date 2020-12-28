import pygame
from bird import Bird
from ground import Ground
from pipe import Pipe
from population import Population
import time
import os
import random
import numpy as np

WIN_WIDTH = 250 # screen width
WIN_HEIGHT = 400 # screen height


def draw_window(win, population, pipes, ground, max_score, score):
    win.blit(pygame.image.load(os.path.join('images', 'bg.png')), (0,0)) # draws background

    for pipe in pipes:
        pipe.draw(win) # draws pipe on screen

    ground.draw(win) # draws ground

    for bird in population:
        bird.draw(win) # draws bird

    # sets up txt score
    text = pygame.font.SysFont('comicsans', 25).render("Max Score: " + str(max_score)
                                                       + '          Score:' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10)) # draws score

    pygame.display.update() # updates screen

def main():
    population = Population(25, 0.01)

    ground = Ground()
    pipes = [Pipe()]

    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.font.init()
    clock = pygame.time.Clock()
    max_score = 0
    score = 0

    while run:
        #clock.tick(30)
        ground.move() # moves ground

        # Pipes
        removed_pipes = []
        flag_add_pipe = False
        for pipe in pipes:
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # if pipe leaves screen
                removed_pipes.append(pipe)

            pipe.move()  # moves pipe

            for bird in population.individuals:
                if pipe.collide(bird) and bird.is_alive: # checks collision
                    bird.is_alive = False

                if not pipe.passed: # measures distance between bird and next pipe
                    bird.distance_x_next_pipe = (pipe.x - bird.x)
                    bird.distance_y_next_pipe = (pipe.height - bird.y)

                # checks if pipe has already been crossed
                if not pipe.passed and pipe.x + pipe.PIPE_BOTTOM.get_width()/2 < bird.x - bird.img.get_width()/2:
                    bird.fitness += 100
                    pipe.passed = True
                    flag_add_pipe = True
                    score += 1


        if flag_add_pipe:
            pipes.append(Pipe()) # adds pipe

        for removed_pipe in removed_pipes:
            pipes.remove(removed_pipe) # removes pipe


        for bird in population.individuals:
            bird.move()  # move pássaro
            if bird.y + bird.img.get_height() >= 350 and bird.is_alive: # if bird hits the ground
                bird.is_alive = False
                bird.y = 350

            if bird.y < 0: # if bird hits the ceiling
                bird.y = 0

            if bird.is_alive:
                bird.fitness += 1

        draw_window(win, population.individuals, pipes, ground, max_score, score) # draws objects modifications on screen

        if population.is_all_dead():
            pipes = [Pipe()]
            population.reproduct()
            if score > max_score:
                max_score = score
            score = 0

        # Exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    quit()

main()
