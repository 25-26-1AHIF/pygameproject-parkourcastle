import pygame
from game_variables.game_variables import GameVariables

class Player:
    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: wie erstelle ich ein png in frames und wie mache ich den dash und cooldown?
    def __init__(self, screen):
        self.screen = screen
        sheet = pygame.image.load("sprites/player/walk_cycle.png").convert_alpha()
        sheet = pygame.transform.scale(sheet, (175, 75))

        frame_width = sheet.get_width() // 4
        frame_height = sheet.get_height()

        self.frames = [sheet.subsurface(pygame.Rect(i*frame_width,0,frame_width,frame_height)) for i in range(4)]
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(100, 600))

        # Bewegung
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.facing_right = True

        # Animation
        self.animation_index = 0
        self.animation_timer = 0

        # Dash
        self.can_dash = True
        self.dash_cooldown = 1000
        self.last_dash_time = 0
        self.space_was_pressed = False
        self.dash_active = False
        self.dash_frames_left = 0
        self.dash_step = 0

    def move(self):
        keys = pygame.key.get_pressed()

        # Links / Rechts laufen
        if keys[pygame.K_a]:
            self.dx = -5
            self.facing_right = False
            self.animate_walk()
        elif keys[pygame.K_d]:
            self.dx = 5
            self.facing_right = True
            self.animate_walk()
        else:
            self.dx = 0
            self.image = self.frames[0] if self.facing_right else self.frames_left[0]

        # Springen
        if keys[pygame.K_w] and self.on_ground:
            self.dy = -15
            self.on_ground = False

        # Dash
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if not self.space_was_pressed:
                if self.can_dash and now - self.last_dash_time >= self.dash_cooldown:
                    self.start_dash()
                    self.can_dash = False
                    self.last_dash_time = now
            self.space_was_pressed = True
        else:
            self.space_was_pressed = False

        # Cooldown reset
        if not self.can_dash and now - self.last_dash_time >= self.dash_cooldown:
            self.can_dash = True

    def start_dash(self):
        # 20 Pixel über 5 Frames = 4 Pixel pro Frame
        self.dash_active = True
        self.dash_frames_left = 15
        self.dash_step = 12.5

    def do_dash(self):
        if self.dash_active:
            if self.facing_right and self.on_ground:
                self.rect.x += self.dash_step
            elif not self.facing_right and self.on_ground:
                self.rect.x -= self.dash_step
            elif self.facing_right and not self.on_ground:
                self.rect.y -= self.dash_step
                self.rect.x += self.dash_step
            elif not self.facing_right and not self.on_ground:
                self.rect.y -= self.dash_step
                self.rect.x -= self.dash_step
            self.dash_frames_left -= 1
            if self.dash_frames_left <= 0:
                self.dash_active = False
    # KI-Ende

    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: wie kann ich die frames tauschen beim Laufen?
    def animate_walk(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % 3 + 1
            self.image = self.frames[self.animation_index] if self.facing_right else self.frames_left[self.animation_index]
    # KI-Ende

    # KI-Anfang
    # KI: Microsoft Copilot
    # prompt: wie erstelle ich Schwerkraft?
    def physics(self):
        self.dy += 1
        self.rect.x += self.dx
        self.rect.y += self.dy

        self.do_dash()

        if self.rect.bottom >= GameVariables.SCREEN_HEIGHT:
            self.rect.bottom = GameVariables.SCREEN_HEIGHT
            self.dy = 0
            self.on_ground = True
    # KI-Ende

    def draw_with_camera(self, camera_x, camera_y):
        self.screen.blit(self.image, (self.rect.x + camera_x,
                                      self.rect.y + camera_y - GameVariables.SQUARE_SIZE * 0.875))

    def update_and_draw(self, camera_x, camera_y):
        self.move()
        self.physics()
        self.draw_with_camera(camera_x, camera_y)


