import pygame
import pygame.time

from Game.player import Player
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens

def main_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> GameScreens:
    pygame.display.set_caption("Main Screen")
    BACKGROUND = pygame.image.load("sprites/background/Start_screen.png")
    BACKGROUND = pygame.transform.scale(BACKGROUND, (GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))

    # statische texte erstellen
    titel_text = GameVariables.FONT_BIG.render("ParkourCastle", True, "white")
    starten_text = GameVariables.FONT_MIDDLE.render("START", True, "white")
    controls_text = GameVariables.FONT_MIDDLE.render("CONTROLS", True, "white")

    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 100))
    starten_text_rect  = starten_text.get_rect(center=(GameVariables.SCREEN_WIDTH/4, 250))
    controls_text_rect = controls_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 400))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                # klickposition event.pos (x, y)
                if starten_text_rect.collidepoint(event.pos):
                    counting = True
                    print("Starten gedrückt!")
                    return GameScreens.PLAY
                elif controls_text_rect.collidepoint(event.pos):
                    print("Controls gedrückt!")
                    return GameScreens.CONTROLS

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=controls_text, dest=controls_text_rect)
        pygame.draw.rect(screen, (255, 0, 0), starten_text_rect, 1)
        pygame.draw.rect(screen, (255, 255, 0), controls_text_rect, 1)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()

def play_screen(screen, clock):
    pygame.display.set_caption("Play Screen")
    score = 0

    highscore_text = GameVariables.FONT_MIDDLE.render(f"Score: {score}", True, "white")
    highscore_text_rect = highscore_text.get_rect(center=(GameVariables.SCREEN_WIDTH - 100, 20))

    BACKGROUND = pygame.image.load("sprites/background/bricks-background.png")
    BACKGROUND = pygame.transform.scale(BACKGROUND, (int(GameVariables.SCREEN_WIDTH * 5),
                                                     int(GameVariables.SCREEN_HEIGHT * 2.5)))

    top_platform = pygame.image.load("sprites/ground/Top_platform.png")
    top_platform = pygame.transform.scale(top_platform, (GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE))

    player = Player(screen)
    running = True

    # Die Main Loop (Game Loop)
    while running:
        # Jedes Ereignis (Event) durchgehen
        for event in pygame.event.get():
            # Das Spiel verlassen, falls der Benutzer das Fenster schließen möchte
            if event.type == pygame.QUIT:
                counting = False
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    counting = False
                    print("Escape gedrückt!")
                    return GameScreens.EXIT

        camera_x = -player.rect.x + GameVariables.SCREEN_WIDTH // 2
        camera_y = 0  # Kamera bleibt vertikal fixiert
        target_y = -player.rect.y + GameVariables.SCREEN_HEIGHT * 0.7
        camera_y += (target_y - camera_y) * 0.05

        # Parallax berechnen (10% der Kamerabewegung)
        parallax_x = camera_x * 0.1
        parallax_y = camera_y * 0.1

        # Hintergrund darf nicht aus dem Bild rutschen
        max_x = 0
        min_x = GameVariables.SCREEN_WIDTH - BACKGROUND.get_width()
        max_y = 0
        min_y = GameVariables.SCREEN_HEIGHT - BACKGROUND.get_height()

        parallax_x = max(min(parallax_x, max_x), min_x)
        parallax_y = max(min(parallax_y, max_y), min_y)



        # Hintergrund zeichnen
        screen.blit(BACKGROUND, (parallax_x, parallax_y))


        in_screen = True
        screen.blit(top_platform,
                    (parallax_x, 1.4 * GameVariables.SQUARE_SIZE * parallax_y + GameVariables.SCREEN_HEIGHT))
        while in_screen:
            parallax_x_new = parallax_x + GameVariables.SQUARE_SIZE
            if parallax_x_new >= GameVariables.SCREEN_WIDTH:
                in_screen = False
            else:
                screen.blit(top_platform,
                            (parallax_x_new, 1.4 * GameVariables.SQUARE_SIZE * parallax_y + GameVariables.SCREEN_HEIGHT))
                parallax_x = parallax_x_new



        # Player mit Kamera zeichnen
        player.update_and_draw(camera_x, camera_y)
        # Das Display updaten
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()

def controls_screen(screen, clock):
    BACKGROUND = pygame.image.load("sprites/background/bricks-background.png")
    BACKGROUND = pygame.transform.scale(BACKGROUND, (GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))
    steuerung_text = GameVariables.FONT_BIG.render("Steuerung", True, "white")
    springen_text = GameVariables.FONT_MIDDLE.render("W - Springen", True, "white")
    links_text = GameVariables.FONT_MIDDLE.render("A - Links", True, "white")
    rechts_text = GameVariables.FONT_MIDDLE.render("D - Rechts", True, "white")
    escape_text = GameVariables.FONT_MIDDLE.render("Escape - Menü/Pause", True, "white")
    sprung_dash_text = GameVariables.FONT_MIDDLE.render("Leertaste+W - Sprungdash", True, "white")
    links_dash_text = GameVariables.FONT_MIDDLE.render("Leertaste+A - Linksdash", True, "white")
    rechts_dash_text = GameVariables.FONT_MIDDLE.render("Leertaste+D - Rechtsdash", True, "white")
    dash_erklaert_text = GameVariables.FONT_SMALL.render("DASH: Boostet dich kurz in die jeweilige ausgewählte Richtung nach vorne!", True, "red")
    x_text = GameVariables.FONT_BIG.render("X", True, "white")

    steuerung_text_rect = steuerung_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 50))
    springen_text_rect = springen_text.get_rect(center=(GameVariables.SCREEN_WIDTH/4, 200))
    links_text_rect = links_text.get_rect(center=(GameVariables.SCREEN_WIDTH*0.75, 200))
    rechts_text_rect = rechts_text.get_rect(center=(GameVariables.SCREEN_WIDTH/4, 300))
    escape_text_rect = escape_text.get_rect(center=(GameVariables.SCREEN_WIDTH*0.75, 300))
    links_dash_text_rect = links_dash_text.get_rect(center=(GameVariables.SCREEN_WIDTH/4, 400))
    rechts_dash_text_rect = rechts_dash_text.get_rect(center=(GameVariables.SCREEN_WIDTH*0.75, 400))
    sprung_dash_text_rect = sprung_dash_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 500))
    dash_erklaert_text_rect = dash_erklaert_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 700))
    x_text_rect = x_text.get_rect(center=(924, 63))



    pygame.display.set_caption("Controls Screen")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape gedrückt!")
                    return GameScreens.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    print("Close-Button gedrückt!")
                    return GameScreens.EXIT

        screen.fill("black")
        screen.blit(source=steuerung_text, dest=steuerung_text_rect)
        screen.blit(source=springen_text, dest=springen_text_rect)
        screen.blit(source=links_text, dest=links_text_rect)
        screen.blit(source=rechts_text, dest=rechts_text_rect)
        screen.blit(source=escape_text, dest=escape_text_rect)
        screen.blit(source=links_dash_text, dest=links_dash_text_rect)
        screen.blit(source=rechts_dash_text, dest=rechts_dash_text_rect)
        screen.blit(source=sprung_dash_text, dest=sprung_dash_text_rect)
        screen.blit(source=dash_erklaert_text, dest=dash_erklaert_text_rect)
        close_button = pygame.draw.rect(screen, (255, 0, 0), (900, 36, 50, 50), border_radius=10)
        screen.blit(source=x_text, dest=x_text_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()




def main():
    GameVariables.init()
    screen = pygame.display.set_mode((GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))
    # Clock für die FPS Überwachung erstellen
    clock = pygame.time.Clock()

    while True:
        if GameScreens.actual == GameScreens.MAIN:
            GameScreens.actual = main_screen(screen, clock)
        elif GameScreens.actual == GameScreens.PLAY:
            GameScreens.actual = play_screen(screen, clock)
        elif GameScreens.actual == GameScreens.EXIT:
            GameScreens.actual = main_screen(screen, clock)
        elif GameScreens.actual == GameScreens.CONTROLS:
            GameScreens.actual = controls_screen(screen, clock)
    pygame.quit()

if __name__ == '__main__':
    # pygame und fonts initialisieren
    main()
