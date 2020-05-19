import pygame
from bird import Bird
from base import Base
from pipe import Pipe
from population import Population
import time
import os
import random
import numpy as np

WIN_WIDTH = 250 # largura da tela
WIN_HEIGHT = 400 # altura da tela


def draw_window(win, population, pipes, base, max_score, score):
    win.blit(pygame.image.load(os.path.join('images', 'bg.png')), (0,0)) # coloca background

    for pipe in pipes:
        pipe.draw(win) # coloca pipes na tela

    base.draw(win) # coloca o chão

    for bird in population:
        bird.draw(win) # coloca o pássaro

    # configura txt score
    text = pygame.font.SysFont('comicsans', 25).render("Max Score: " + str(max_score)
                                                       + '          Score:' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10)) # coloca score

    pygame.display.update() # atualiza tela

def main():
    population = Population(25, 0.01)

    base = Base()
    pipes = [Pipe()]

    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.font.init()
    clock = pygame.time.Clock()
    max_score = 0
    score = 0

    while run:
        #clock.tick(30)
        base.move() # move chão

        # Canos
        removed_pipes = []
        flag_add_pipe = False
        for pipe in pipes:
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # se o cano sair da tela
                removed_pipes.append(pipe)

            pipe.move()  # move cano

            for bird in population.individuals:
                if pipe.collide(bird) and bird.is_alive: # checa colisão
                    bird.is_alive = False

                if not pipe.passed: # medir distancia entre pássaro e próximo pipe
                    bird.distance_x_next_pipe = (pipe.x - bird.x)
                    bird.distance_y_next_pipe = (pipe.height - bird.y)

                # checa se o cano foi ultrapassado
                if not pipe.passed and pipe.x + pipe.PIPE_BOTTOM.get_width()/2 < bird.x - bird.img.get_width()/2:
                    bird.fitness += 100
                    pipe.passed = True
                    flag_add_pipe = True
                    score += 1


        if flag_add_pipe:
            pipes.append(Pipe()) # adiciona cano

        for removed_pipe in removed_pipes:
            pipes.remove(removed_pipe) # remove cano


        for bird in population.individuals:
            bird.move()  # move pássaro
            if bird.y + bird.img.get_height() >= 350 and bird.is_alive: # se pássaro atingiu o chão
                bird.is_alive = False
                bird.y = 350

            if bird.y < 0: # se o pássaro atingir o teto
                bird.y = 0

            if bird.is_alive:
                bird.fitness += 1

        draw_window(win, population.individuals, pipes, base, max_score, score) # desenha modificação dos objetos na tela

        if population.is_all_dead():
            pipes = [Pipe()]
            population.reproduct()
            if score > max_score:
                max_score = score
            score = 0

        # Sair do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    quit()

main()
