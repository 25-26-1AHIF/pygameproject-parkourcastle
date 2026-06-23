import pygame


class GameVariables:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 720
    SQUARE_SIZE = 64
    CLOSE_SIZE = 50
    FPS = 60
    HAS_SHIELD = False
    HAS_SPEED = False
    HAS_DOUBLEJUMP = False
    HAS_MULTIPLIER = False
    HAS_EXTRA_LIFE = False

    PLAYER_NAME = ""
    SCORE = 0
    HIGHSCORE_FILE = "highscores.json"


    FONT_BIG = None
    FONT_MIDDLE = None
    FONT_SMALL = None

    @staticmethod
    def init():
        pygame.init()
        pygame.display.set_mode((GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))
        GameVariables.FONT_BIG = pygame.font.SysFont("bahnschrift", 48, bold=True)
        GameVariables.FONT_MIDDLE = pygame.font.SysFont("bahnschrift", 30, bold=False)
        GameVariables.FONT_SMALL = pygame.font.SysFont("bahnschrift", 14, bold=False)


class GameScreens:
    MAIN = "mainscreen"
    PLAY = "play"
    CONTROLS = "controls"
    EXIT = "exit"
    NAME_INPUT = "name_input"
    NAME_INPUT_SHOP = "name_input_shop"
    HIGHSCORES = "highscores"
    DEATH = "death"
    CREDITS = "credits"
    SHOP = "shop"
    actual = MAIN