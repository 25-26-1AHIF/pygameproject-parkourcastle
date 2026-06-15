import pygame
import pygame.time

from Game.highscore_manager import load_scores, save_scores, update_score
import random

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
    controls_text = GameVariables.FONT_MIDDLE.render("STEUERUNG", True, "white")
    highscores_text = GameVariables.FONT_MIDDLE.render("BESTENLISTE", True, "white")

    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 100))
    starten_text_rect  = starten_text.get_rect(center=(GameVariables.SCREEN_WIDTH/4, 250))
    highscores_text_rect = highscores_text.get_rect(center=(GameVariables.SCREEN_WIDTH/4, 325))
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
                    return GameScreens.NAME_INPUT
                elif controls_text_rect.collidepoint(event.pos):
                    print("Controls gedrückt!")
                    return GameScreens.CONTROLS
                elif highscores_text_rect.collidepoint(event.pos):
                    print("Leaderboard gedrückt!")
                    return GameScreens.HIGHSCORES

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=controls_text, dest=controls_text_rect)
        screen.blit(source=highscores_text, dest=highscores_text_rect)
        pygame.draw.rect(screen, (255, 0, 0), starten_text_rect, 1)
        pygame.draw.rect(screen, (255, 255, 0), controls_text_rect, 1)
        pygame.draw.rect(screen, (0, 255, 255), highscores_text_rect, 1)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()

import random

def generate_ground():
    ANZAHL_BLOECKE = 200

    ground = []
    i = 0

    while i < ANZAHL_BLOECKE:

        # 5% Chance auf eine Grube
        if random.random() < 0.05:

            # Grube mindestens 1 Block lang
            grubenlaenge = random.randint(1, 2)

            for _ in range(grubenlaenge):
                if i < ANZAHL_BLOECKE:
                    ground.append(False)
                    i += 1

        else:
            ground.append(True)
            i += 1

    return ground

def play_screen(screen, clock):
    GameVariables.SCORE = 0
    score_timer = pygame.time.get_ticks()
    pygame.display.set_caption("Play Screen")


    BACKGROUND = pygame.image.load("sprites/background/bricks-background.png")
    BACKGROUND = pygame.transform.scale(BACKGROUND, (int(GameVariables.SCREEN_WIDTH * 5),
                                                     int(GameVariables.SCREEN_HEIGHT * 2.5)))

    none_platform = pygame.image.load("sprites/ground/none_platform.png")
    none_platform = pygame.transform.scale(none_platform, (GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE))

    top_platform = pygame.image.load("sprites/ground/Top_platform.png")
    top_platform = pygame.transform.scale(top_platform, (GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE))

    player = Player(screen)
    ground = generate_ground()
    running = True

    # Die Main Loop (Game Loop)
    while running:
        if pygame.time.get_ticks() - score_timer >= 1000:
            GameVariables.SCORE += 1
            score_timer = pygame.time.get_ticks()
        # Jedes Ereignis (Event) durchgehen
        for event in pygame.event.get():
            # Das Spiel verlassen, falls der Benutzer das Fenster schließen möchte
            if event.type == pygame.QUIT:
                counting = False
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
                    counting = False
                    print("Escape gedrückt!")
                    return GameScreens.EXIT
        if player.rect.y >= GameVariables.SCREEN_HEIGHT:
            update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
            return GameScreens.DEATH


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
        score_text = GameVariables.FONT_BIG.render(f"Score: {GameVariables.SCORE}", True, "white")
        name_text = GameVariables.FONT_MIDDLE.render(f"{GameVariables.PLAYER_NAME}", True, "white")
        screen.blit(score_text, (GameVariables.SCREEN_WIDTH - 225, 50))
        screen.blit(name_text, (25, 25))

        ground_y = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE

        for i, block in enumerate(ground):

            if block:
                x = i * GameVariables.SQUARE_SIZE + camera_x

                screen.blit(
                    none_platform,
                    (x, ground_y)
                )

                screen.blit(
                    top_platform,
                    (x, ground_y - GameVariables.SQUARE_SIZE)
                )

        # Player mit Kamera zeichnen
        player.update_and_draw(camera_x, camera_y, ground)
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
        close_button = pygame.draw.rect(screen, (255, 0, 0), (900, 36, 50, 50), border_radius=10)
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

def name_input_screen(screen, clock):
    pygame.display.set_caption("Name eingeben")

    name = ""
    font = GameVariables.FONT_BIG

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GameVariables.PLAYER_NAME = name
                    return GameScreens.PLAY

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode
        screen.fill("black")
        text = font.render("Name: " + name, True, "white")
        screen.blit(text, (100, 200))

        pygame.display.flip()
        clock.tick(60)


def highscore_screen(screen, clock):
    pygame.display.set_caption("Highscores")


    scores = load_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    x_text = GameVariables.FONT_BIG.render("X", True, "white")
    x_text_rect = x_text.get_rect(center=(924, 63))
    titel_text = GameVariables.FONT_BIG.render("Bestenliste", True, "white")
    keine_spieler_text = pygame.font.SysFont("bahnschrift", 80, bold=True).render("! Keine Spieler gefunden !", True, "red")
    keine_spieler_text_rect = keine_spieler_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, GameVariables.SCREEN_HEIGHT/2))
    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 100))

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
        close_button = pygame.draw.rect(screen, (255, 0, 0), (900, 36, 50, 50), border_radius=10)
        screen.blit(source=x_text, dest=x_text_rect)
        screen.blit(source=titel_text, dest=titel_text_rect)
        if not scores:
            screen.blit(source=keine_spieler_text, dest=keine_spieler_text_rect)
        y = 150
        for name, score in sorted_scores:
            text = GameVariables.FONT_MIDDLE.render(f"{name}: {score}", True, "gold")
            screen.blit(text, (100, y))
            y += 50

        pygame.display.flip()
        clock.tick(60)

def death_screen(screen, clock):
    pygame.display.set_caption("Death")

    tod_text = pygame.font.SysFont("bahnschrift", 80, bold=True).render("Du bist gestorben...", True, "red")
    tod_text_rect = tod_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, GameVariables.SCREEN_HEIGHT/2))
    hauptmenu_text = GameVariables.FONT_MIDDLE.render("Hauptmenü", True, "white")
    hauptmenu_text_rect = hauptmenu_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, GameVariables.SCREEN_HEIGHT/2 + 100))
    screen.fill("black")
    pygame.draw.rect(screen, "brown", hauptmenu_text_rect, border_radius=10)
    screen.blit(source=tod_text, dest=tod_text_rect)
    screen.blit(source=hauptmenu_text, dest=hauptmenu_text_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hauptmenu_text_rect.collidepoint(event.pos):
                    print("Hauptmenü gedrückt!")
                    return GameScreens.EXIT

        pygame.display.flip()
        clock.tick(60)



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
        elif GameScreens.actual == GameScreens.NAME_INPUT:
            GameScreens.actual = name_input_screen(screen, clock)
        elif GameScreens.actual == GameScreens.HIGHSCORES:
            GameScreens.actual = highscore_screen(screen, clock)
        elif GameScreens.actual == GameScreens.DEATH:
            GameScreens.actual = death_screen(screen, clock)
pygame.quit()


if __name__ == '__main__':
    # pygame und fonts initialisieren
    main()
