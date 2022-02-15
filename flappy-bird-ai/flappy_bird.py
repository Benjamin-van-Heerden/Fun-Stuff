import pygame
import pygame_menu
from train_gameloop import train_gameloop
from normal_gameloop import normal_gameloop
from ai_gameloop import ai_gameloop

WIN_WIDTH = 500
WIN_HEIGHT = 800


def quit_game():
    pygame.quit()
    quit()


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    menu = pygame_menu.Menu(
        "Flappy Bird NEAT",
        WIN_WIDTH - 50,
        WIN_HEIGHT - 50,
        theme=pygame_menu.themes.THEME_DARK,
    )
    menu.add.button("Play Normal", normal_gameloop)
    menu.add.button("AI Train", train_gameloop)
    menu.add.button("AI Play", ai_gameloop)
    menu.add.button("Quit", quit_game)

    menu.mainloop(surface)
