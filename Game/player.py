import pygame
from game_variables.game_variables import GameVariables

class Player:
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

        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.facing_right = True

        self.animation_index = 0
        self.animation_timer = 0

        self.can_dash = True
        self.dash_cooldown = 1000
        self.last_dash_time = 0
        self.space_was_pressed = False
        self.dash_active = False
        self.dash_frames_left = 0
        self.dash_step = 0

        self.invulnerable_until = 0
        self.dash_disabled_until = 0

        self.speed_multiplier = 1.0
        self.can_doublejump = False
        self.doublejump_used = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.dx = -5 * self.speed_multiplier
            self.facing_right = False
            self.animate_walk()
        elif keys[pygame.K_d]:
            self.dx = 5 * self.speed_multiplier
            self.facing_right = True
            self.animate_walk()
        else:
            self.dx = 0
            self.image = self.frames[0] if self.facing_right else self.frames_left[0]

        if keys[pygame.K_w]:
            if self.on_ground:
                self.dy = -20
                self.on_ground = False
                self.doublejump_used = False
            elif self.can_doublejump and not self.doublejump_used:
                self.dy = -20
                self.doublejump_used = True

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

        if not self.can_dash and now - self.last_dash_time >= self.dash_cooldown:
            self.can_dash = True

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
            self.animation_index = (self.animation_index + 1) % 3 + 1
            self.image = self.frames[self.animation_index] if self.facing_right else self.frames_left[self.animation_index]

    def physics(self, ground):
        self.dy += 1
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        self.do_dash()

        top_world_y = GameVariables.SCREEN_HEIGHT - 2 * GameVariables.SQUARE_SIZE
        left_index = self.rect.left // GameVariables.SQUARE_SIZE
        right_index = (self.rect.right - 1) // GameVariables.SQUARE_SIZE

        supported = False
        n = len(ground)
        for idx in range(left_index, right_index + 1):
            if 0 <= idx < n and ground[idx]:
                supported = True
                break

        if self.rect.bottom >= top_world_y:
            if supported:
                self.rect.bottom = top_world_y
                self.dy = 0
                self.on_ground = True
            else:
                self.on_ground = False
                if self.dy < 1:
                    self.dy = 1
        else:
            self.on_ground = False

    def draw_with_camera(self, camera_x, camera_y):
        now = pygame.time.get_ticks()
        # Schild aktiv → blauer Kreis
        if GameVariables.HAS_SHIELD and now < GameVariables.SHIELD_ACTIVE_UNTIL:
            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (self.rect.x + camera_x + self.rect.width // 2,
                 self.rect.y + camera_y + self.rect.height // 2),
                max(self.rect.width, self.rect.height),
                3
            )
        # Blink-Effekt bei Invulnerability
        if now < getattr(self, "invulnerable_until", 0):
            if (now // 100) % 2 == 0:
                self.screen.blit(self.image, (self.rect.x + camera_x, self.rect.y + camera_y))
        else:
            self.screen.blit(self.image, (self.rect.x + camera_x, self.rect.y + camera_y))

    def update_and_draw(self, camera_x, camera_y, ground):
        self.move()
        self.physics(ground)
        self.draw_with_camera(camera_x, camera_y)
