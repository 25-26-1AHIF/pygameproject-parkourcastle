import pygame
from game_variables.game_variables import GameVariables

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x = 100
        self.y = 600
        self.width = 40
        self.height = 60
        self.image = pygame.image.load("sprites/walk_cycle.png")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
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
        self.screen.blit(self.image, self.rect)

    def update_and_draw(self):
        self.move()
        self.physics()
        self.draw()
