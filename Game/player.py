import time

import pygame
from game_variables.game_variables import GameVariables

class Player:
    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: wie lade ich eine png in frames?
    def __init__(self, screen):
        self.screen = screen
        sheet = pygame.image.load("sprites\player\walk_cycle.png").convert_alpha()
        sheet = pygame.transform.scale(sheet, (175, 75))

        frame_width = sheet.get_width() // 4
        frame_height = sheet.get_height()

        self.last_dash_time = 0
        self.dash_cooldown = 1000

        self.frames = []
        for i in range(4):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sheet.subsurface(rect)
            self.frames.append(frame)

        self.image = self.frames[0]


        self.frames_left = []
        for i in range(4):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sheet.subsurface(rect)
            frame_left = pygame.transform.flip(frame, True, False)
            self.frames_left.append(frame_left)

        self.image_left = self.frames_left[0]

        self.rect = self.image.get_rect(topleft=(100, 600))

        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.animation_index = 0
        self.animation_timer = 0
    # KI-Ende

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_SPACE]:
            self.dx = -5
            self.animate_walk()
            self.image = self.image_left
        elif keys[pygame.K_d] and not keys[pygame.K_SPACE]:
            self.dx = 5
            self.animate_walk()
            self.image_left = self.image
        elif keys[pygame.K_a] and keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_dash_time > self.dash_cooldown:
                self.dx = -20
                self.animate_walk()
                self.image = self.image_left
                self.last_dash_time = now
        elif keys[pygame.K_d] and keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_dash_time > self.dash_cooldown:
                self.dx = 20
                self.animate_walk()
                self.image_left = self.image
                self.last_dash_time = 0
        else:
            self.dx = 0
            if self.image:
                self.image_left = self.image
            else:
                self.image = self.image_left

        if keys[pygame.K_w] and self.on_ground and not keys[pygame.K_SPACE]:
            self.dy = -15
            self.on_ground = False
        elif keys[pygame.K_w] and self.on_ground and keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_dash_time > self.dash_cooldown:
                self.dy = -30
                self.on_ground = False
                self.last_dash_time = 0

    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: wie wechsel ich zwischen frames?
    def animate_walk(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % 3 + 1
            self.image = self.frames[self.animation_index]
            self.image_left = self.frames_left[self.animation_index]
    # KI-Ende

    def animate_dash(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % 3 + 1

    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: Wie kann ich Schwerkraft hinzufügen?
    def physics(self):
        self.dy += 1
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.bottom >= GameVariables.SCREEN_HEIGHT:
            self.rect.bottom = GameVariables.SCREEN_HEIGHT
            self.dy = 0
            self.on_ground = True
    # KI-Ende

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update_and_draw(self):
        self.move()
        self.physics()
        self.draw()
