# player.py
import pygame
from game_variables.game_variables import GameVariables

class Player:
    def __init__(self, screen):
        self.screen = screen
        # Load sprite sheet (4 frames assumed)
        sheet = pygame.image.load("sprites/player/walk_cycle.png").convert_alpha()
        # scale to reasonable size (adjust if needed)
        sheet = pygame.transform.scale(sheet, (175, 75))

        frame_width = sheet.get_width() // 4
        frame_height = sheet.get_height()

        self.frames = [sheet.subsurface(pygame.Rect(i*frame_width,0,frame_width,frame_height)) for i in range(4)]
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames]

        self.image = self.frames[0]
        # initial rect; respawn will place player correctly
        self.rect = self.image.get_rect(topleft=(100, 600))

        # Movement
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

        # Invulnerability and dash disable timers
        self.invulnerable_until = 0
        self.dash_disabled_until = 0

    def move(self):
        keys = pygame.key.get_pressed()

        # Left / Right
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

        # Jump
        if keys[pygame.K_w] and self.on_ground:
            self.dy = -15
            self.on_ground = False

        # Dash input handling (space)
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

        # Reactivate dash if cooldown passed
        if not self.can_dash and now - self.last_dash_time >= self.dash_cooldown:
            self.can_dash = True

        # Reactivate dash if disabled by respawn invuln
        if getattr(self, "dash_disabled_until", 0) and now >= self.dash_disabled_until:
            self.can_dash = True
            self.dash_disabled_until = 0

    def start_dash(self):
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

    def animate_walk(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            # cycle through walking frames (1..3)
            self.animation_index = (self.animation_index + 1) % 3 + 1
            self.image = self.frames[self.animation_index] if self.facing_right else self.frames_left[self.animation_index]

    def physics(self, ground):
        # gravity
        self.dy += 1
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

        # dash movement
        self.do_dash()

        # Top platform Y (world coordinate)
        top_world_y = GameVariables.SCREEN_HEIGHT - 2 * GameVariables.SQUARE_SIZE

        # Determine which ground indices are under player's feet
        left_index = self.rect.left // GameVariables.SQUARE_SIZE
        right_index = (self.rect.right - 1) // GameVariables.SQUARE_SIZE

        supported = False
        n = len(ground)
        # check all indices under player's width for robustness
        for idx in range(left_index, right_index + 1):
            if 0 <= idx < n and ground[idx]:
                supported = True
                break

        if self.rect.bottom >= top_world_y:
            if supported:
                # snap to platform
                self.rect.bottom = top_world_y
                self.dy = 0
                self.on_ground = True
            else:
                # fall through if no support
                self.on_ground = False
                if self.dy < 1:
                    self.dy = 1
        else:
            self.on_ground = False

    def draw_with_camera(self, camera_x, camera_y):
        now = pygame.time.get_ticks()
        if now < getattr(self, "invulnerable_until", 0):
            # blink every 100 ms
            if (now // 100) % 2 == 0:
                self.screen.blit(self.image, (self.rect.x + camera_x, self.rect.y + camera_y))
        else:
            self.screen.blit(self.image, (self.rect.x + camera_x, self.rect.y + camera_y))

    def update_and_draw(self, camera_x, camera_y, ground):
        self.move()
        self.physics(ground)
        self.draw_with_camera(camera_x, camera_y)