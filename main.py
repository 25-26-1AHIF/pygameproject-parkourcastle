import pygame
import pygame.time
from Game import player
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
    credits_text = GameVariables.FONT_MIDDLE.render("CREDITS", True, "white")
    shop_text = GameVariables.FONT_MIDDLE.render("SHOP", True, "white")

    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 100))
    starten_text_rect = starten_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 250))
    highscores_text_rect = highscores_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 325))
    controls_text_rect = controls_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 400))
    credits_text_rect = credits_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 475))
    shop_text_rect = shop_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 550))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.EXIT
                if event.key == pygame.K_q:
                    # Code-Eingabe bevor Admin-Panel
                    code = ""
                    entering = True
                    while entering:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit();
                                exit(0)
                            if e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_RETURN:
                                    if code == "2684":
                                        return GameScreens.ADMIN_PANEL
                                    else:
                                        entering = False
                                elif e.key == pygame.K_ESCAPE:
                                    entering = False
                                elif e.key == pygame.K_BACKSPACE:
                                    code = code[:-1]
                                else:
                                    if len(code) < 4 and e.unicode.isdigit():
                                        code += e.unicode
                        screen.fill("black")
                        txt = GameVariables.FONT_BIG.render("Admin-Code: " + code, True, "yellow")
                        screen.blit(txt, (200, 300))
                        pygame.display.flip()
                        clock.tick(30)

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
                elif credits_text_rect.collidepoint(event.pos):
                    print("Credits gedrückt!")
                    return GameScreens.CREDITS
                elif shop_text_rect.collidepoint(event.pos):
                    print("Shop gedrückt!")
                    return GameScreens.NAME_INPUT_SHOP

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=controls_text, dest=controls_text_rect)
        screen.blit(source=highscores_text, dest=highscores_text_rect)
        screen.blit(source=credits_text, dest=credits_text_rect)
        screen.blit(source=shop_text, dest=shop_text_rect)

        pygame.draw.rect(screen, (255, 0, 0), starten_text_rect, 1)
        pygame.draw.rect(screen, (255, 255, 0), controls_text_rect, 1)
        pygame.draw.rect(screen, (0, 255, 255), highscores_text_rect, 1)
        pygame.draw.rect(screen, (255, 0, 255), credits_text_rect, 1)
        pygame.draw.rect(screen, (0, 0, 255), shop_text_rect, 1)
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

    spike_img = pygame.image.load("sprites/Spikes/Spikes.png")
    spike_img = pygame.transform.scale(spike_img, (GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE))

    player = Player(screen)

    # Powerups nur wenn gekauft
    if GameVariables.HAS_SPEED:
        player.speed_multiplier = 1.5
    if GameVariables.HAS_DOUBLEJUMP:
        player.can_doublejump = True

    ground = generate_ground()
    spikes = [i for i, block in enumerate(ground) if block and random.random() < 0.1]
    spikes = clear_spikes_around(spikes, center=0, radius=3)

    player.rect.x = 0
    player.rect.bottom = GameVariables.SCREEN_HEIGHT - 2 * GameVariables.SQUARE_SIZE
    player.dx = 0
    player.dy = 0
    player.on_ground = True

    running = True
    while running:
        now = pygame.time.get_ticks()

        # Score mit Multiplikator
        if now - score_timer >= 1000:
            if player.dx > 0:
                GameVariables.SCORE += 2 if GameVariables.HAS_MULTIPLIER else 1
            score_timer = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
                return GameScreens.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and GameVariables.HAS_SHIELD:
                icon_rect = pygame.Rect(GameVariables.SCREEN_WIDTH - 80, GameVariables.SCREEN_HEIGHT - 80, 64, 64)
                if icon_rect.collidepoint(event.pos):
                    if now >= GameVariables.SHIELD_LAST_USED + GameVariables.SHIELD_COOLDOWN:
                        GameVariables.SHIELD_LAST_USED = now
                        GameVariables.SHIELD_ACTIVE_UNTIL = now + GameVariables.SHIELD_DURATION
                        player.invulnerable_until = GameVariables.SHIELD_ACTIVE_UNTIL

        # Tod durch Fallen
        if player.rect.top > GameVariables.SCREEN_HEIGHT:
            # Reset Schild-Cooldown beim Tod
            GameVariables.SHIELD_LAST_USED = 0
            GameVariables.SHIELD_ACTIVE_UNTIL = 0
            update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
            return GameScreens.DEATH

        # Kamera berechnen
        camera_x = -player.rect.x + GameVariables.SCREEN_WIDTH // 2
        camera_y = 0
        target_y = -player.rect.y + GameVariables.SCREEN_HEIGHT * 0.7
        camera_y += (target_y - camera_y) * 0.05

        # Parallax berechnen
        parallax_x = camera_x * 0.1
        parallax_y = camera_y * 0.1

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

        spike_rects = []

        for i, block in enumerate(ground):
            if block:
                world_x = i * GameVariables.SQUARE_SIZE
                world_ground_y = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE
                top_world_y = world_ground_y - GameVariables.SQUARE_SIZE

                # Zeichnen in Kamerakoordinaten
                screen.blit(none_platform, (world_x + camera_x, world_ground_y + camera_y))
                screen.blit(top_platform, (world_x + camera_x, top_world_y + camera_y))

                # Spike zeichnen und Rect speichern
                if i in spikes:
                    spike_world_x = world_x
                    spike_top_y = top_world_y

                    spike_img_w = spike_img.get_width()
                    spike_img_h = spike_img.get_height()

                    draw_y = spike_top_y - spike_img_h
                    screen.blit(spike_img, (spike_world_x + camera_x, draw_y + camera_y))

                    spike_rect = pygame.Rect(spike_world_x, draw_y, spike_img_w, spike_img_h)
                    spike_rects.append(spike_rect)

                    # Debug-Hitbox zeichnen
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (spike_rect.x + camera_x, spike_rect.y + camera_y, spike_rect.width,
                                      spike_rect.height), 1)


        # Player updaten und zeichnen
        player.update_and_draw(camera_x, camera_y, ground)
        if now < GameVariables.SHIELD_ACTIVE_UNTIL:
            pygame.draw.circle(
                screen,
                (0, 0, 255),
                (player.rect.x + camera_x + player.rect.width // 2,
                 player.rect.y + camera_y + player.rect.height // 2),
                max(player.rect.width, player.rect.height),
                3
            )
        pygame.draw.rect(screen, (0, 255, 0),
                         (player.rect.x + camera_x, player.rect.y + camera_y, player.rect.width,
                          player.rect.height), 1)

        # Spike-Kollision prüfen
        for spike in spike_rects:
            if player.rect.colliderect(spike):
                if GameVariables.HAS_SHIELD and now < GameVariables.SHIELD_ACTIVE_UNTIL:
                    # Schild aktiv → ignorieren
                    continue
                elif GameVariables.HAS_EXTRA_LIFE:
                    GameVariables.HAS_EXTRA_LIFE = False
                    player.invulnerable_until = now + 2000
                    player.rect.x = 0
                    player.rect.y = GameVariables.SCREEN_HEIGHT - 3 * GameVariables.SQUARE_SIZE
                else:
                    # Reset Schild-Cooldown beim Tod
                    GameVariables.SHIELD_LAST_USED = 0
                    GameVariables.SHIELD_ACTIVE_UNTIL = 0
                    update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
                    return GameScreens.DEATH

        # Schild-Icon zeichnen nur, wenn gekauft
        if GameVariables.HAS_SHIELD:
            icon_x, icon_y = GameVariables.SCREEN_WIDTH - 80, GameVariables.SCREEN_HEIGHT - 80
            cooldown_remaining = max(0, (
                        GameVariables.SHIELD_LAST_USED + GameVariables.SHIELD_COOLDOWN - now) // 1000)
            icon = GameVariables.SHIELD_ICON.copy()
            icon.set_alpha(100 if cooldown_remaining > 0 else 255)
            screen.blit(icon, (icon_x, icon_y))
            if cooldown_remaining > 0:
                cd_text = GameVariables.FONT_SMALL.render(str(cooldown_remaining), True, "white")
                screen.blit(cd_text, (icon_x + 20, icon_y - 20))
            if now < GameVariables.SHIELD_ACTIVE_UNTIL:
                pygame.draw.circle(screen, (0, 0, 255),
                                   (player.rect.x + camera_x + player.rect.width // 2,
                                    player.rect.y + camera_y + player.rect.height // 2),
                                   max(player.rect.width, player.rect.height), 3)

        # Statusanzeige unten links (leicht nach oben versetzt)
        speed_value = int(5 * player.speed_multiplier)  # Basisgeschwindigkeit 5, multipliziert
        jump_value = 20 if player.can_doublejump else 10
        multiplier_value = "x2" if GameVariables.HAS_MULTIPLIER else "x1"
        extra_life_value = "AKTIV" if GameVariables.HAS_EXTRA_LIFE else "INAKTIV"

        status_lines = [
            f"Speed: {speed_value}",
            f"Sprungkraft: {jump_value}",
            f"Multiplikator: {multiplier_value}",
            f"Extra-Leben: {extra_life_value}"
        ]

        # Position: unten links, aber ca. 100 Pixel über dem unteren Rand
        y_offset = GameVariables.SCREEN_HEIGHT - 100
        for line in status_lines:
            txt = GameVariables.FONT_SMALL.render(line, True, "white")
            screen.blit(txt, (40, y_offset))  # 40 Pixel vom linken Rand
            y_offset += 20

        pygame.display.flip()
        clock.tick(GameVariables.FPS)

    # Closure, die respawn_player die Kamera sofort setzen lässt
    def set_camera(x, y):
        nonlocal camera_x, camera_y
        camera_x = x
        camera_y = y
    # --- Left wall (chaser) setup ---
    # Start at world x = 0 (left edge of background/world)
    wall_width = GameVariables.SCREEN_WIDTH // 3
    wall_height = GameVariables.SCREEN_HEIGHT * 3
    wall_x = GameVariables.SCREEN_WIDTH - GameVariables.SCREEN_WIDTH  # starts at the very left of the world/background
    wall_y = 0
    # Wall speed slightly slower than player max horizontal speed (player ~5 px/frame)
    wall_speed = 2  # adjust 1-3 for difficulty

    # Sofort sicheren Spawn erzwingen (bereinigt spikes in Spawn-Umgebung)
    spikes = respawn_player(player, ground, spikes, set_camera, clear_radius=2, spike_clear_radius=2, invuln_ms=1500)

    running = True

    # Precompute world length (end of background)
    world_length = len(ground) * GameVariables.SQUARE_SIZE

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
        if player.rect.top > GameVariables.SCREEN_HEIGHT:
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

        spike_rects = []

        for i, block in enumerate(ground):
            if block:
                # Weltkoordinaten (keine Kamera hier)
                world_x = i * GameVariables.SQUARE_SIZE
                world_ground_y = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE
                top_world_y = world_ground_y - GameVariables.SQUARE_SIZE

                # Rects in Weltkoordinaten (nur für Logik / Debug)
                rect1 = pygame.Rect(world_x, world_ground_y, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)
                rect2 = pygame.Rect(world_x, top_world_y, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)

                # Zeichnen in Kamerakoordinaten (ADD camera offset)
                screen.blit(none_platform, (world_x + camera_x, world_ground_y + camera_y))
                screen.blit(top_platform, (world_x + camera_x, top_world_y + camera_y))

                # Spike zeichnen und Rect in Weltkoordinaten speichern (robust gegen Sprite-Höhe)
                # Spike zeichnen und Rect in Weltkoordinaten speichern (korrekte Y-Ausrichtung)
                if i in spikes:
                    spike_world_x = world_x
                    spike_top_y = top_world_y  # die Y-Position der Oberkante der Plattform

                    spike_img_w = spike_img.get_width()
                    spike_img_h = spike_img.get_height()

                    # Zeichnen: Unterkante des Spike-Sprites auf spike_top_y setzen
                    draw_y = spike_top_y - spike_img_h
                    screen.blit(spike_img, (spike_world_x + camera_x, draw_y + camera_y))

                    # Rect für Kollision: passt zur sichtbaren Sprite
                    spike_rect = pygame.Rect(spike_world_x, draw_y, spike_img_w, spike_img_h)
                    spike_rects.append(spike_rect)

                    # --- Update wall position (world coordinates) ---
                    # Wall moves right at wall_speed each frame (so player can outrun it if faster)
                    wall_x += wall_speed

                    # Clamp wall to world end so it doesn't run past the level
                    if wall_x + wall_width > world_length:
                        wall_x = max(0, world_length - wall_width)

                    # Draw wall in camera coordinates (solid black rectangle)
                    wall_rect_world = pygame.Rect(wall_x, wall_y, wall_width, wall_height)
                    pygame.draw.rect(screen, (0, 0, 0), (wall_rect_world.x + camera_x, wall_rect_world.y + camera_y,
                                                         wall_rect_world.width, wall_rect_world.height))

                    # If wall collides with player, push player to the right of the wall
                    if wall_rect_world.colliderect(player.rect):
                        # place player's left edge at wall's right edge (world coords)
                        player.rect.left = wall_rect_world.right
                        player.dx = 0
                        # small extra push to avoid sticking
                        player.rect.x += 2

        # Player updaten und zeichnen (player.rect bleibt in Weltkoordinaten)
        player.update_and_draw(camera_x, camera_y, ground)
        # Debug: Spieler-Hitbox in Grün zeichnen (1px Rahmen)
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (player.rect.x + camera_x, player.rect.y + camera_y, player.rect.width, player.rect.height),
            1
        )
        # Spike-Kollision prüfen (Weltkoordinaten)
        now = pygame.time.get_ticks()
        for spike in spike_rects:
            if player.rect.colliderect(spike) and now >= getattr(player, "invulnerable_until", 0):
                update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
                return GameScreens.DEATH

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
    dash_erklaert_text = GameVariables.FONT_SMALL.render(
        "DASH: Boostet dich kurz in die jeweilige ausgewählte Richtung nach vorne!", True, "red")
    x_text = GameVariables.FONT_BIG.render("X", True, "white")

    steuerung_text_rect = steuerung_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 50))
    springen_text_rect = springen_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 200))
    links_text_rect = links_text.get_rect(center=(GameVariables.SCREEN_WIDTH * 0.75, 200))
    rechts_text_rect = rechts_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 300))
    escape_text_rect = escape_text.get_rect(center=(GameVariables.SCREEN_WIDTH * 0.75, 300))
    links_dash_text_rect = links_dash_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 4, 400))
    rechts_dash_text_rect = rechts_dash_text.get_rect(center=(GameVariables.SCREEN_WIDTH * 0.75, 400))
    sprung_dash_text_rect = sprung_dash_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 500))
    dash_erklaert_text_rect = dash_erklaert_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 700))
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
                elif event.key == pygame.K_ESCAPE:
                    return GameScreens.EXIT

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
    keine_spieler_text = pygame.font.SysFont("bahnschrift", 80, bold=True).render("! Keine Spieler gefunden !", True,
                                                                                  "red")
    keine_spieler_text_rect = keine_spieler_text.get_rect(
        center=(GameVariables.SCREEN_WIDTH / 2, GameVariables.SCREEN_HEIGHT / 2))
    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 100))

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
        for idx, (name, entry) in enumerate(sorted_scores):
            # Falls alter Eintrag nur Zahl ist
            score_value = entry if isinstance(entry, int) else entry.get("score", 0)

            if idx == 0:
                text = GameVariables.FONT_MIDDLE.render(f"1. {name} - {score_value}s", True, "gold")
                screen.blit(text, (100, y))
                y += 75
            elif idx == 1:
                text = GameVariables.FONT_MIDDLE.render(f"2. {name} - {score_value}s", True, "silver")
                screen.blit(text, (100, y))
                y += 75
            elif idx == 2:
                text = GameVariables.FONT_MIDDLE.render(f"3. {name} - {score_value}s", True, "brown")
                screen.blit(text, (100, y))
                y += 75
            else:
                text = GameVariables.FONT_MIDDLE.render(f"{idx + 1}. {name} - {score_value}s", True, "white")
                screen.blit(text, (100, y))
                y += 75

        pygame.display.flip()
        clock.tick(60)


def death_screen(screen, clock):
    pygame.display.set_caption("Death")

    tod_text = pygame.font.SysFont("bahnschrift", 80, bold=True).render("Du bist gestorben...", True, "red")
    tod_text_rect = tod_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, GameVariables.SCREEN_HEIGHT / 2))
    hauptmenu_text = GameVariables.FONT_MIDDLE.render("Hauptmenü", True, "white")
    hauptmenu_text_rect = hauptmenu_text.get_rect(
        center=(GameVariables.SCREEN_WIDTH / 2, GameVariables.SCREEN_HEIGHT / 2 + 100))
    screen.fill("black")
    pygame.draw.rect(screen, "brown", hauptmenu_text_rect, border_radius=10)
    screen.blit(source=tod_text, dest=tod_text_rect)
    screen.blit(source=hauptmenu_text, dest=hauptmenu_text_rect)
    score_timer = pygame.time.get_ticks()

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


def credits_screen(screen, clock):
    pygame.display.set_caption("Credits")

    BACKGROUND = pygame.image.load("sprites/background/bricks-background.png")
    BACKGROUND = pygame.transform.scale(BACKGROUND, (GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))

    titel_text = GameVariables.FONT_BIG.render("Credits", True, "white")
    titel_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 100))

    # Beispiel-Credits
    dev_text = GameVariables.FONT_MIDDLE.render("Entwickler: Vincent Raven Schwindsackl und Levin Hagen", True, "gold")
    dev_rect = dev_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 250))

    art_text = GameVariables.FONT_MIDDLE.render("Grafiken: Levin Hagen - Eigene Assets", True, "white")
    art_rect = art_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 325))

    music_text = GameVariables.FONT_MIDDLE.render("Musik/SFX: Levin Hagen - Eigene Sounds", True, "white")
    music_rect = music_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 400))

    first_thanks_text = GameVariables.FONT_MIDDLE.render("Spezielles Dankeschön an: Die Lehrer für das beibringen",
                                                         True, "white")
    second_thanks_text = GameVariables.FONT_MIDDLE.render("Levin Hagen für die Sounds und Grafiken und", True, "white")
    third_thanks_text = GameVariables.FONT_MIDDLE.render("Vincent Raven Schwindsackl für den Code!", True, "white")

    first_thanks_rect = first_thanks_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 475))
    second_thanks_rect = second_thanks_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 525))
    third_thanks_rect = third_thanks_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 575))

    x_text = GameVariables.FONT_BIG.render("X", True, "white")
    x_rect = x_text.get_rect(center=(924, 63))
    close_button = pygame.Rect(900, 36, 50, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    return GameScreens.EXIT

        screen.blit(BACKGROUND, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), close_button, border_radius=10)
        screen.blit(x_text, x_rect)

        screen.blit(titel_text, titel_rect)
        screen.blit(dev_text, dev_rect)
        screen.blit(art_text, art_rect)
        screen.blit(music_text, music_rect)
        screen.blit(first_thanks_text, first_thanks_rect)
        screen.blit(second_thanks_text, second_thanks_rect)
        screen.blit(third_thanks_text, third_thanks_rect)

        pygame.display.flip()
        clock.tick(GameVariables.FPS)


import random
import pygame


def find_safe_spawn_index(ground, spikes, clear_radius=2, tries=200):
    n = len(ground)
    for _ in range(tries):
        i = random.randrange(n)
        left = max(0, i - clear_radius)
        right = min(n - 1, i + clear_radius)
        if all(ground[left:right + 1]) and i not in spikes:
            return i
    # Fallback: lineare Suche
    for i in range(n):
        left = max(0, i - clear_radius)
        right = min(n - 1, i + clear_radius)
        if all(ground[left:right + 1]) and i not in spikes:
            return i
    return None


def clear_spikes_around(spikes, center, radius=2):
    return [s for s in spikes if abs(s - center) > radius]


def respawn_player(player, ground, spikes, camera_setter=None, clear_radius=2, spike_clear_radius=2, invuln_ms=1000):
    # finde sicheren Index
    idx = find_safe_spawn_index(ground, spikes, clear_radius)
    if idx is None:
        idx = 0
        while idx < len(ground) and not ground[idx]:
            idx += 1
        if idx >= len(ground):
            idx = 0

    # entferne Spikes in der Nähe (synchron, bevor wir Spike-Rects bauen)
    spikes = clear_spikes_around(spikes, idx, spike_clear_radius)

    # Weltkoordinaten für Spawn
    world_x = idx * GameVariables.SQUARE_SIZE
    top_world_y = GameVariables.SCREEN_HEIGHT - 2 * GameVariables.SQUARE_SIZE

    # setze Spieler sauber (1px Puffer nach oben), reset Bewegung
    player.rect.x = world_x
    player.rect.bottom = top_world_y - 1
    player.dx = 0
    player.dy = 0
    player.on_ground = True

    # Invulnerabilität setzen
    # nach player.rect setzen
    now = pygame.time.get_ticks()
    player.invulnerable_until = now + 1000  # 1000 ms = 1 Sekunde Schutz
    # optional: disable dash during invuln
    player.can_dash = False
    player.dash_disabled_until = now + 1000

    # Kamera sofort zentrieren (falls gewünscht)
    if camera_setter:
        camera_x = -player.rect.x + GameVariables.SCREEN_WIDTH // 2
        camera_y = 0
        camera_setter(camera_x, camera_y)

    # Rückgabe: aktualisierte spikes-Liste
    return spikes


def shop_screen(screen, clock):
    pygame.display.set_caption("Shop")
    scores = load_scores()
    # Prüfen ob Spieler existiert
    if GameVariables.PLAYER_NAME not in scores:
        # Spieler hat noch nie gespielt → zurück zum Main-Screen
        return GameScreens.MAIN

    # Spieler existiert → Daten laden
    entry = scores[GameVariables.PLAYER_NAME]
    if isinstance(entry, int):
        GameVariables.SCORE = entry
    else:
        GameVariables.SCORE = entry.get("score", 0)
        upgrades = entry.get("upgrades", {})
        GameVariables.HAS_SHIELD = upgrades.get("HAS_SHIELD", False)
        GameVariables.HAS_SPEED = upgrades.get("HAS_SPEED", False)
        GameVariables.HAS_DOUBLEJUMP = upgrades.get("HAS_DOUBLEJUMP", False)
        GameVariables.HAS_MULTIPLIER = upgrades.get("HAS_MULTIPLIER", False)
        GameVariables.HAS_EXTRA_LIFE = upgrades.get("HAS_EXTRA_LIFE", False)

    titel_text = GameVariables.FONT_BIG.render("Shop & Upgrades", True, "white")
    titel_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, 100))

    items = [
        ("Schild", 50, "HAS_SHIELD"),
        ("Speed", 100, "HAS_SPEED"),
        ("Double-Jump", 150, "HAS_DOUBLEJUMP"),
        ("Multiplikator", 200, "HAS_MULTIPLIER"),
        ("Extra-Leben", 250, "HAS_EXTRA_LIFE"),
    ]

    button_rects = []
    y = 250
    for name, preis, flag in items:
        rect = pygame.Rect(GameVariables.SCREEN_WIDTH / 2 - 150, y, 300, 50)
        button_rects.append((rect, name, preis, flag))
        y += 75

    feedback_text = None
    feedback_color = None
    feedback_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Score nach Shop speichern
                update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE)
                return GameScreens.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, name, preis, flag in button_rects:
                    if rect.collidepoint(event.pos):
                        if getattr(GameVariables, flag, False):
                            feedback_text = f"{name} bereits gekauft!"
                            feedback_color = (200, 200, 200)
                            feedback_timer = pygame.time.get_ticks()
                        elif GameVariables.SCORE >= preis:
                            GameVariables.SCORE -= preis
                            setattr(GameVariables, flag, True)
                            scores = load_scores()
                            if GameVariables.PLAYER_NAME in scores:
                                update_score(GameVariables.PLAYER_NAME, GameVariables.SCORE, force_save=True)
                            feedback_text = f"{name} gekauft!"
                            feedback_color = (0, 200, 0)
                            feedback_timer = pygame.time.get_ticks()
                        else:
                            feedback_text = "Nicht genug Punkte!"
                            feedback_color = (200, 0, 0)
                            feedback_timer = pygame.time.get_ticks()


        screen.fill("black")
        screen.blit(titel_text, titel_rect)

        score_text = GameVariables.FONT_MIDDLE.render(
            f"Score: {GameVariables.SCORE}", True, "yellow"
        )
        screen.blit(score_text, (50, 50))

        for rect, name, preis, flag in button_rects:
            if getattr(GameVariables, flag, False):
                pygame.draw.rect(screen, (128, 128, 128), rect, border_radius=10)
                text = GameVariables.FONT_MIDDLE.render(f"{name} - gekauft", True, "white")
            else:
                pygame.draw.rect(screen, (0, 255, 0), rect, border_radius=10)
                text = pygame.font.SysFont("bahnschrift", 24, bold=True).render(f"{name} - {preis} Punkte", True, "black")
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if feedback_text and pygame.time.get_ticks() - feedback_timer < 1000:
            fb = GameVariables.FONT_MIDDLE.render(feedback_text, True, feedback_color)
            fb_rect = fb.get_rect(center=(GameVariables.SCREEN_WIDTH / 2, GameVariables.SCREEN_HEIGHT - 100))
            screen.blit(fb, fb_rect)

        pygame.display.flip()
        clock.tick(GameVariables.FPS)

def admin_panel_screen(screen, clock):
    pygame.display.set_caption("Admin-Panel")
    running = True
    input_name = ""
    input_score = ""
    scores = load_scores()
    focus = 0  # 0 = Spieler, 1 = Score

    # Feedback
    feedback_text = ""
    feedback_color = None
    feedback_until = 0

    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.EXIT
                elif event.key == pygame.K_TAB:
                    focus = 1 - focus
                elif event.key == pygame.K_BACKSPACE:
                    if focus == 1 and input_score:
                        input_score = input_score[:-1]
                    elif focus == 0 and input_name:
                        input_name = input_name[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        if input_name in scores:
                            new_score = int(input_score)
                            scores[input_name]["score"] = new_score
                            save_scores(scores)
                            feedback_text = "Gespeichert"
                            feedback_color = (0, 200, 0)  # grün
                            feedback_until = now + 2000
                        else:
                            feedback_text = f"Fehler: Spieler '{input_name}' nicht gefunden"
                            feedback_color = (200, 0, 0)  # rot
                            feedback_until = now + 4000
                    except ValueError:
                        feedback_text = "Fehler: Score muss Zahl sein"
                        feedback_color = (200, 0, 0)
                        feedback_until = now + 4000
                else:
                    if focus == 1 and event.unicode.isdigit():
                        input_score += event.unicode
                    elif focus == 0:
                        input_name += event.unicode

        # Hintergrund
        screen.fill("yellow")
        title = GameVariables.FONT_BIG.render("Admin-Panel", True, "black")
        screen.blit(title, (GameVariables.SCREEN_WIDTH//2 - 150, 50))

        # Textfelder mit Rand
        name_rect = pygame.Rect(100, 200, 400, 40)
        score_rect = pygame.Rect(100, 260, 400, 40)
        pygame.draw.rect(screen, (0,0,0), name_rect, 2 if focus == 0 else 1)
        pygame.draw.rect(screen, (0,0,0), score_rect, 2 if focus == 1 else 1)

        # Texte
        name_txt = GameVariables.FONT_MIDDLE.render("Spieler: " + input_name, True, "black")
        score_txt = GameVariables.FONT_MIDDLE.render("Neuer Score: " + input_score, True, "black")
        screen.blit(name_txt, (name_rect.x+5, name_rect.y+5))
        screen.blit(score_txt, (score_rect.x+5, score_rect.y+5))

        # Caret (blinkender Strich)
        caret_height = GameVariables.FONT_MIDDLE.get_height()
        if focus == 0:
            caret_x = name_rect.x + 5 + GameVariables.FONT_MIDDLE.size("Spieler: " + input_name)[0]
            caret_y = name_rect.y + 5
        else:
            caret_x = score_rect.x + 5 + GameVariables.FONT_MIDDLE.size("Neuer Score: " + input_score)[0]
            caret_y = score_rect.y + 5
        if (now // 500) % 2 == 0:
            pygame.draw.line(screen, (0,0,0), (caret_x, caret_y), (caret_x, caret_y+caret_height), 2)

        # Feedback anzeigen
        if feedback_text and now < feedback_until:
            fb_txt = GameVariables.FONT_MIDDLE.render(feedback_text, True, feedback_color)
            screen.blit(fb_txt, (100, 350))

        info_txt = GameVariables.FONT_SMALL.render("TAB = wechseln, Enter = speichern, ESC = schließen", True, "black")
        screen.blit(info_txt, (100, 400))

        pygame.display.flip()
        clock.tick(GameVariables.FPS)


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
        elif GameScreens.actual == GameScreens.CREDITS:
            GameScreens.actual = credits_screen(screen, clock)
        elif GameScreens.actual == GameScreens.ADMIN_PANEL:
            GameScreens.actual = admin_panel_screen(screen, clock)
        elif GameScreens.actual == GameScreens.NAME_INPUT_SHOP:
            result = name_input_screen(screen, clock)
            if result == GameScreens.PLAY:
                scores = load_scores()
                if GameVariables.PLAYER_NAME in scores:
                    entry = scores[GameVariables.PLAYER_NAME]
                    if isinstance(entry, int):
                        GameVariables.SCORE = entry
                    else:
                        GameVariables.SCORE = entry.get("score", 0)
                        upgrades = entry.get("upgrades", {})
                        GameVariables.HAS_SHIELD = upgrades.get("HAS_SHIELD", False)
                        GameVariables.HAS_SPEED = upgrades.get("HAS_SPEED", False)
                        GameVariables.HAS_DOUBLEJUMP = upgrades.get("HAS_DOUBLEJUMP", False)
                        GameVariables.HAS_MULTIPLIER = upgrades.get("HAS_MULTIPLIER", False)
                        GameVariables.HAS_EXTRA_LIFE = upgrades.get("HAS_EXTRA_LIFE", False)
                else:
                    # Spieler nicht in der Liste → Shop mit 0 Score öffnen
                    GameVariables.SCORE = 0
                    GameVariables.HAS_SHIELD = False
                    GameVariables.HAS_SPEED = False
                    GameVariables.HAS_DOUBLEJUMP = False
                    GameVariables.HAS_MULTIPLIER = False
                    GameVariables.HAS_EXTRA_LIFE = False
                    # WICHTIG: NICHT speichern → kein Eintrag in JSON

                GameScreens.actual = shop_screen(screen, clock)
            else:
                GameScreens.actual = result


pygame.quit()

if __name__ == '__main__':
    # pygame und fonts initialisieren
    main()