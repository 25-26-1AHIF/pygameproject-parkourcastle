import pygame
from Game.player import Player
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens

def main_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> GameScreens:
    pygame.display.set_caption("Main Screen")

    # statische texte erstellen
    titel_text = GameVariables.FONT_BIG.render("WeltraumShooter", True, "white")
    starten_text = GameVariables.FONT_MIDDLE.render("Starten", True, "white")
    controls_text = GameVariables.FONT_MIDDLE.render("Steuerung", True, "white")

    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 100))
    starten_text_rect  = starten_text.get_rect(center=(GameVariables.SCREEN_WIDTH/2, 250))
    controls_text_rect = controls_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 400))

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
                    print("Starten gedrückt!")
                    return GameScreens.PLAY
                elif controls_text_rect.collidepoint(event.pos):
                    print("Controls gedrückt!")
                    return GameScreens.CONTROLS

        screen.fill("black")
        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        pygame.draw.rect(screen, (255, 0, 0), starten_text_rect, 1)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()

def play_screen(screen, clock):
    pygame.display.set_caption("Play Screen")
    player = Player(screen)
    running = True
    # Die Main Loop (Game Loop)
    while running:
        shoot = False
        # Jedes Ereignis (Event) durchgehen
        for event in pygame.event.get():
            # Das Spiel verlassen, falls der Benutzer das Fenster schließen möchte
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape gedrückt!")
                    return GameScreens.EXIT
        screen.fill("black")
        player.update_and_draw()
        # Das Display updaten
        pygame.display.flip()
        # FPS überwachen
        clock.tick(GameVariables.FPS)
    pygame.quit()

def controls_screen(screen, clock):
    pygame.display.set_caption("Controls Screen")



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