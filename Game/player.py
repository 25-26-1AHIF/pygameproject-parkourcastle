import pygame
from game_variables.game_variables import GameVariables
from Game.platform import Platform

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x = 100
        self.y = 600
        self.width = 40
        self.height = 60
        self.color = (0, 255, 0)
        self.dx = 0
        self.dy = 0
        self.on_ground = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.dx = -5
        elif keys[pygame.K_d]:
            self.dx = 5
        else:
            self.dx = 0

        if keys[pygame.K_w] and self.on_ground:
            self.dy = -15
            self.on_ground = False

    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: Wie kann ich Schwerkraft hinzufügen?
    def physics(self):
        self.dy += 1
        self.y += self.dy
        self.x += self.dx

        if self.y + self.height >= GameVariables.SCREEN_HEIGHT:
            self.y = GameVariables.SCREEN_HEIGHT - self.height
            self.dy = 0
            self.on_ground = True
    # KI-Ende

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def update_and_draw(self):
        self.move()
        self.physics()
        self.draw()
