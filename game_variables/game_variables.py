import pygame


class GameVariables:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 720
    SQUARE_SIZE = 32
    FPS = 60


    FONT_BIG = None
    FONT_MIDDLE = None
    FONT_SMALL = None

    @staticmethod
    def init():
        pygame.init()
        GameVariables.FONT_BIG = pygame.font.SysFont("orbitron", 48, bold=True)
        GameVariables.FONT_MIDDLE = pygame.font.SysFont("orbitron", 30, bold=False)
        GameVariables.FONT_SMALL = pygame.font.SysFont("orbitron", 14, bold=False)


class GameScreens:
    MAIN = "mainscreen"
    PLAY = "play"
    CONTROLS = "controls"
    EXIT = "exit"
    actual = MAIN