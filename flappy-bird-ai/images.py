import pygame
from os.path import join, dirname

# load up images
BIRD_IMGS = [
    pygame.transform.scale2x(
        pygame.image.load(join(dirname(__file__), "imgs/bird1.png"))
    ),
    pygame.transform.scale2x(
        pygame.image.load(join(dirname(__file__), "imgs/bird2.png"))
    ),
    pygame.transform.scale2x(
        pygame.image.load(join(dirname(__file__), "imgs/bird3.png"))
    ),
]

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(join(dirname(__file__), "imgs/pipe.png"))
)

BG_IMG = pygame.transform.scale2x(
    pygame.image.load(join(dirname(__file__), "imgs/bg.png"))
)

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(join(dirname(__file__), "imgs/base.png"))
)