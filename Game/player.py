import pygame
from game_variables.game_variables import GameVariables

class Player:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.xpos = GameVariables.SCREEN_WIDTH // 2 - GameVariables.SQUARE_SIZE // 2 - 1
        self.ypos = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE - 1

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.xpos -= 5
        if keys[pygame.K_d]:
            self.xpos += 5

    def update_and_draw(self):
        self.move()