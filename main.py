import pygame
import sys
import math
from constants import *
from player import Player
from enemy import EnemySoul
from levels import get_level_data
from menu import draw_main_menu, draw_class_select, draw_pause_screen, draw_settings

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("monospace", 48, bold=True)
font_med = pygame.font.SysFont("monospace", 32)
font_small = pygame.font.SysFont("monospace", 20)

game_state = STATE_MAIN_MENU
current_level = 1
menu_cursor = 0
class_cursor = 0
pause_cursor = 0
settings_cursor = 0
anim_timer = 0
select_delay = 0
player = None
walls = []
enemies = []

def draw_end_screen(text, color, extra=""):
    screen.fill((12, 8, 35))
    msg = font_big.render(text, True, color)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 80))
    if extra:
        sub = font_med.render(extra, True, (220, 220, 220))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))

running = True
while running:
    current_time = pygame.time.get_ticks()
    mouse_click = False
    mouse_pos = pygame.mouse.get_pos()
    anim_timer += 0.085

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True

    keys = pygame.key.get_pressed()

    # Global ESC
    if keys[pygame.K_ESCAPE]:
        if game_state == STATE_GAME:
            game_state = STATE_PAUSED
            pause_cursor = 0
            pygame.time.wait(200)
        elif game_state == STATE_PAUSED:
            game_state = STATE_GAME
            pygame.time.wait(200)
        elif game_state != STATE_MAIN_MENU:
            game_state = STATE_MAIN_MENU
            select_delay = 0

    if game_state == STATE_MAIN_MENU:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            menu_cursor = (menu_cursor - 1) % 4
            pygame.time.wait(140)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            menu_cursor = (menu_cursor + 1) % 4
            pygame.time.wait(140)

        menu_cursor = draw_main_menu(screen, menu_cursor, anim_timer, mouse_pos, font_med, font_big)
        
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or mouse_click) and select_delay == 0:
            select_delay = 25
            if menu_cursor == 0:
                current_level = 1
                game_state = STATE_CLASS_SELECT
                class_cursor = 0
            elif menu_cursor == 1:
                game_state = STATE_SETTINGS
                settings_cursor = 0
            elif menu_cursor == 2:
                game_state = STATE_ABOUT
            elif menu_cursor == 3:
                running = False

    elif game_state == STATE_CLASS_SELECT:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            class_cursor = (class_cursor - 1) % 3
            pygame.time.wait(140)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            class_cursor = (class_cursor + 1) % 3
            pygame.time.wait(140)

        class_cursor = draw_class_select(screen, class_cursor, anim_timer, mouse_pos, font_med, font_big)
        
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or mouse_click) and select_delay == 0:
            select_delay = 25
            class_list = ["Monk", "Priest", "Exorcist"]
            player = Player(class_list[class_cursor])
            walls, enemy_pos = get_level_data(current_level)
            enemies = [EnemySoul(x, y) for x, y in enemy_pos]
            game_state = STATE_GAME

    elif game_state == STATE_GAME:
        player.update(keys, mouse_pos, mouse_click, current_time, walls, enemies)
        
        for e in enemies[:]:
            if player.class_type == "Monk" and player.invisible:
                e.projectiles = []
            e.update(player, current_time, walls)
            
            for p in player.projectiles[:]:
                if p.is_heal and math.hypot(p.x - e.x, p.y - e.y) < e.size + 9:
                    e.elevation += 28
                    if p in player.projectiles: player.projectiles.remove(p)
            for p in e.projectiles[:]:
                if not p.is_heal and math.hypot(p.x - player.x, p.y - player.y) < player.size + 7:
                    player.health -= 14
                    if p in e.projectiles: e.projectiles.remove(p)
            if e.saved:
                enemies.remove(e)
        
        player.projectiles = [p for p in player.projectiles if p.update(walls)]
        
        if player.health <= 0:
            game_state = STATE_LOSE
        elif len(enemies) == 0:
            if current_level < MAX_LEVELS:
                game_state = STATE_LEVEL_COMPLETE
            else:
                game_state = STATE_WIN

        screen.fill((12, 18, 38))
        for x in range(0, WIDTH, 50):
            for y in range(0, HEIGHT, 50):
                pygame.draw.rect(screen, (28, 32, 58), (x, y, 48, 48), 1)
        for wall in walls:
            pygame.draw.rect(screen, (90, 90, 120), wall)
        
        player.draw(screen)
        for e in enemies:
            e.draw(screen)
            for p in e.projectiles: p.draw(screen)
        for p in player.projectiles:
            p.draw(screen)
        
        hud = font_small.render(f"Level {current_level} | {player.class_type} | Health: {int(player.health)}", True, (0, 255, 200))
        screen.blit(hud, (20, 15))

    elif game_state == STATE_PAUSED:
        pause_cursor = draw_pause_screen(screen, pause_cursor, anim_timer, font_med, font_big)
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pause_cursor = (pause_cursor - 1) % 2
            pygame.time.wait(140)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pause_cursor = (pause_cursor + 1) % 2
            pygame.time.wait(140)
        
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or mouse_click) and select_delay == 0:
            select_delay = 25
            if pause_cursor == 0:
                game_state = STATE_GAME
            else:
                game_state = STATE_MAIN_MENU

    elif game_state == STATE_LEVEL_COMPLETE:
        draw_end_screen(f"LEVEL {current_level} COMPLETE!", (100, 255, 180), "SPACE → Next Level")
        if keys[pygame.K_SPACE]:
            current_level += 1
            walls, enemy_pos = get_level_data(current_level)
            enemies = [EnemySoul(x, y) for x, y in enemy_pos]
            player.reset()
            game_state = STATE_GAME

    elif game_state == STATE_WIN:
        draw_end_screen("YOU ELEVATED EVERY SOUL", (100, 255, 180), "ESC to Main Menu")
        if keys[pygame.K_ESCAPE]:
            game_state = STATE_MAIN_MENU
    elif game_state == STATE_LOSE:
        draw_end_screen("YOU GOT LOST...", (255, 80, 80), "ESC to Main Menu")
        if keys[pygame.K_ESCAPE]:
            game_state = STATE_MAIN_MENU

    elif game_state == STATE_SETTINGS:
        settings_cursor = draw_settings(screen, settings_cursor, anim_timer, font_med, font_big, (WIDTH, HEIGHT), bool(screen.get_flags() & pygame.FULLSCREEN))
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            settings_cursor = (settings_cursor - 1) % 3
            pygame.time.wait(140)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            settings_cursor = (settings_cursor + 1) % 3
            pygame.time.wait(140)
        
            if keys[pygame.K_LEFT]:
                if settings_cursor == 0:
                    idx = RESOLUTIONS.index((WIDTH, HEIGHT))
                    idx = (idx - 1) % len(RESOLUTIONS)
                    WIDTH, HEIGHT = RESOLUTIONS[idx]
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.time.wait(200)
                elif settings_cursor == 1:
                    flags = 0 if screen.get_flags() & pygame.FULLSCREEN else pygame.FULLSCREEN
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
                    pygame.time.wait(200)
        
        if keys[pygame.K_RIGHT]:
            if settings_cursor == 0:
                idx = RESOLUTIONS.index((WIDTH, HEIGHT))
                idx = (idx + 1) % len(RESOLUTIONS)
                WIDTH, HEIGHT = RESOLUTIONS[idx]
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.time.wait(200)
            elif settings_cursor == 1:
                flags = 0 if screen.get_flags() & pygame.FULLSCREEN else pygame.FULLSCREEN
                screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
                pygame.time.wait(200)
        
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or mouse_click) and select_delay == 0:
            select_delay = 25
            if settings_cursor == 2:  # OK
                game_state = STATE_MAIN_MENU

    elif game_state == STATE_ABOUT:
        screen.fill((8, 3, 25))
        title = font_big.render("ABOUT", True, (0, 255, 220))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        info = "Pixel healer • Elevate lost souls • Dodge corruption"
        t2 = font_med.render(info, True, (180, 180, 200))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 280))

    if select_delay > 0:
        select_delay -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()