import pygame
import random
from base import Base
from bird import Bird
from pipe import Pipe
from os.path import join, dirname
from images import BG_IMG
import pickle
import math

pygame.font.init()
pygame.display.set_caption("Flappy Bird NEAT")

WIN_WIDTH = 500
WIN_HEIGHT = 800
STAT_FONT_SCORE = pygame.font.SysFont("monospace", 40)
STAT_FONT_STATS = pygame.font.SysFont("monospace", 25)


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT_SCORE.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT_STATS.render(f"'q' to quit", 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)
    bird.draw(win)

    pygame.display.update()


def ai_gameloop():
    bird = Bird(130, 350)

    # load the neural net that governs the bird
    with open(join(dirname(__file__), "best.pickle"), "rb") as n:
        net = pickle.load(n)

    score = 0
    base = Base(730)
    pipes = [Pipe(510)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    break
        # move the ground
        base.move()

        # need to establish which pipe is the upcoming one (also terminate the generation if there are no birds left)
        pipe_ind = 0
        if (
            len(pipes) > 1
            and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
        ):
            pipe_ind = 1

        # make the bird jump or not based on its neural network output
        top_pipe_pos = [
                pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                pipes[pipe_ind].height,
            ]
        bottom_pipe_pos = [
            pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
            pipes[pipe_ind].bottom,
        ]
        bird_pos = [130, bird.y]

        output = net.activate(
            (
                bird.y,
                math.dist(bird_pos, top_pipe_pos),
                math.dist(bird_pos, bottom_pipe_pos),
            )
        )

        # the output uses tanh activation so the value is in [-1, 1]. Using 0 as the trigger to jump also works
        # but I found 0.5 to be a bit better
        if output[0] >= 0.5:
            bird.jump()


        # pipe logic
        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                run = False

            if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < bird.x:
                pipe.passed = True
                add_pipe = True

            # remove a pipe if it is off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            # move the pipe to the left
            pipe.move()

        # remove off-screen pipes
        for r in rem:
            pipes.remove(r)

        # add a pipe at a random location just off screen
        if add_pipe:
            score += 1
            new_pipe_loc = random.randrange(501, 620)
            pipes.append(Pipe(new_pipe_loc))

        # if the bird hit the ground or fly through the ceiling the game ends
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False

        # move the bird
        bird.move()

        draw_window(win, bird, pipes, base, score)