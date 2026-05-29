import pygame

#Ki Anfang - Gemeni
#Promt bitte mach mir eine klasse die spikes heißt bitte programmiere die grafiken richtig ein die datei ist im sprites und dann Spikes und heißt spies bitte.
#Promt 2 bitte füge noch nen scale factor ein weil da wie du im screenshot sehen kannst die textur in ein felck gedrückt wird und nicht 3 schöne spikes sind wie es sein sollte und bitte programmiere noch was das ich die höhe elicht änderen kann
class Spikes:
    def __init__(self, x: float, player_rect: pygame.Rect):
        self.image = pygame.image.load("sprites/Spikes/Spikes.png").convert_alpha()


        scale_factor = 2.3

        new_width = int(self.image.get_width() * scale_factor)
        new_height = int(self.image.get_height() * scale_factor)

        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        y_offset = 44
        y = player_rect.bottom - new_height + y_offset

        self.rect = pygame.Rect(x, y, new_width, new_height)
        # KI ENDE

    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        screen.blit(self.image, (self.rect.x + camera_x, self.rect.y + camera_y))

    def check_collision(self, player_rect: pygame.Rect) -> bool:
        return self.rect.colliderect(player_rect)