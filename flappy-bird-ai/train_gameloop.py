import pygame
import neat
import math
import random
from base import Base
from bird import Bird
from pipe import Pipe
from os.path import join, dirname
from images import BG_IMG
import pickle

pygame.font.init()
pygame.display.set_caption("Flappy Bird NEAT")

WIN_WIDTH = 500
WIN_HEIGHT = 800
STAT_FONT_SCORE = pygame.font.SysFont("monospace", 40)
STAT_FONT_STATS = pygame.font.SysFont("monospace", 25)
DRAW_LINES = True


def draw_window(win, birds, pipes, base, score, gen, pipe_ind, birds_left):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT_SCORE.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT_STATS.render(f"Gen: {gen}", 1, (255, 255, 255))
    win.blit(text, (10, 10))
    text = STAT_FONT_STATS.render(f"Birds Left: {birds_left}", 1, (255, 255, 255))
    win.blit(text, (10, 50))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

        if DRAW_LINES:
            try:
                pygame.draw.line(
                    win,
                    (255, 0, 0),
                    (
                        bird.x + bird.img.get_width() / 2,
                        bird.y + bird.img.get_height() / 2,
                    ),
                    (
                        pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width() / 2,
                        pipes[pipe_ind].height,
                    ),
                    5,
                )
                pygame.draw.line(
                    win,
                    (255, 0, 0),
                    (
                        bird.x + bird.img.get_width() / 2,
                        bird.y + bird.img.get_height() / 2,
                    ),
                    (
                        pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                        pipes[pipe_ind].bottom,
                    ),
                    5,
                )
            except:
                pass

    pygame.display.update()


GEN = 0


def fitness_eval_genomes(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(130, 350))
        g.fitness = 0
        ge.append(g)

    score = 0

    base = Base(730)
    pipes = [Pipe(510)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # move the ground
        base.move()

        # need to establish which pipe is the upcoming one (also terminate the generation if there are no birds left)
        pipe_ind = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                pipe_ind = 1
        else:
            break

        # if the birds survived a frame give them some fitness and most importantly, determine if they should
        # jump or not
        for i, bird in enumerate(birds):
            bird.move()
            # encourage it to survive for another frame
            ge[i].fitness += 0.1

            # the inputs for the network are:
            # 1. bird y position (the bird is static in x only the screen moves)
            # 2. distance to the top pipe (pipe always refers to the "upcoming pipe")
            # 3. distance to bottom pipe
            # for the calculation of the distances the bird always has static x = 130
            top_pipe_pos = [
                pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                pipes[pipe_ind].height,
            ]
            bottom_pipe_pos = [
                pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                pipes[pipe_ind].bottom,
            ]
            bird_pos = [130, bird.y]

            output = nets[i].activate(
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
            for i, bird in enumerate(birds):
                # collision detection -> kill the bird, its network and genome
                if pipe.collide(bird):
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                # pipe passed by at least one bird -> should add a new pipe
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

        # add a pipe at a random location just off screen, this also implies that at least one bird has made it through
        # a pipe -> reward it with a big chunk of fitness
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            new_pipe_loc = random.randrange(501, 620)
            pipes.append(Pipe(new_pipe_loc))

        # if the birds hit the ground or fly through the ceiling they are removed
        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        # if a bird reaches score 100 it will probably go on forever
        if score > 50:
            # store the neural net associated with the best bird for the ai_gameloop 
            pickle.dump(nets[0], open("trained.pickle", "wb"))
            break

        draw_window(win, birds, pipes, base, score, GEN, pipe_ind, len(birds))


def train_gameloop():
    config_path = join(dirname(__file__), "config-feedforward.txt")
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    # run for up to 20 generations
    winner = p.run(fitness_eval_genomes, 20)
    print("winner")
    print(winner)
