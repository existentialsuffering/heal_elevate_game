import pygame
import math


def _centered_positions(screen, rows, top_frac=0.4, spacing_frac=0.08):
    w, h = screen.get_size()
    center_x = w // 2
    start_y = int(h * top_frac)
    spacing = int(h * spacing_frac)
    return [start_y + i * spacing for i in range(rows)], center_x


def draw_main_menu(screen, cursor, anim, mouse_pos, font_med, font_big):
    screen.fill((8, 3, 25))
    w, h = screen.get_size()
    title = font_big.render("HEAL ELEVATE", True, (0, 255, 220))
    screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.15)))

    options = ["START THE GAME", "SETTINGS", "ABOUT", "EXIT"]
    ys, cx = _centered_positions(screen, len(options), top_frac=0.43, spacing_frac=0.1)
    for i, txt in enumerate(options):
        if ys[i] < mouse_pos[1] < ys[i] + int(h * 0.06):
            cursor = i
        color = (255, 240, 0) if i == cursor else (200, 200, 230)
        t = font_med.render(txt, True, color)
        offset = math.sin(anim * 8 + i) * 4 if i == cursor else 0
        screen.blit(t, (cx - t.get_width() // 2 + offset, ys[i]))
    return cursor


def draw_class_select(screen, cursor, anim, mouse_pos, font_med, font_big):
    screen.fill((8, 3, 25))
    w, h = screen.get_size()
    title = font_big.render("CHOOSE YOUR HEALER", True, (0, 255, 220))
    screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.15)))

    options = ["MONK - Close Assassin", "PRIEST - AoE Support", "EXORCIST - Ranged Purifier"]
    ys, cx = _centered_positions(screen, len(options), top_frac=0.38, spacing_frac=0.12)
    for i, txt in enumerate(options):
        if ys[i] < mouse_pos[1] < ys[i] + int(h * 0.06):
            cursor = i
        color = (255, 240, 0) if i == cursor else (200, 200, 230)
        t = font_med.render(txt, True, color)
        offset = math.sin(anim * 8 + i) * 5 if i == cursor else 0
        screen.blit(t, (cx - t.get_width() // 2 + offset, ys[i]))
    return cursor


def draw_pause_screen(screen, cursor, anim, font_med, font_big):
    w, h = screen.get_size()
    overlay = pygame.Surface((w, h))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    paused = font_big.render("PAUSED", True, (255, 255, 100))
    screen.blit(paused, (w // 2 - paused.get_width() // 2, int(h * 0.25)))

    options = ["RESUME", "MAIN MENU"]
    ys, cx = _centered_positions(screen, len(options), top_frac=0.48, spacing_frac=0.08)
    for i, txt in enumerate(options):
        color = (255, 240, 0) if i == cursor else (200, 200, 230)
        t = font_med.render(txt, True, color)
        offset = math.sin(anim * 8 + i) * 4 if i == cursor else 0
        screen.blit(t, (cx - t.get_width() // 2 + offset, ys[i]))
    return cursor


def draw_settings(screen, cursor, anim, font_med, font_big, current_res, is_fullscreen):
    screen.fill((8, 3, 25))
    w, h = screen.get_size()
    title = font_big.render("SETTINGS", True, (0, 255, 220))
    screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.12)))

    ys, cx = _centered_positions(screen, 3, top_frac=0.33, spacing_frac=0.12)

    res_color = (255, 240, 0) if cursor == 0 else (200, 200, 230)
    res_text = font_med.render(f"Resolution: {current_res[0]}x{current_res[1]}", True, res_color)
    screen.blit(res_text, (cx - res_text.get_width() // 2, ys[0]))

    fs_color = (255, 240, 0) if cursor == 1 else (200, 200, 230)
    fs_text = font_med.render("Fullscreen: " + ("ON" if is_fullscreen else "OFF"), True, fs_color)
    screen.blit(fs_text, (cx - fs_text.get_width() // 2, ys[1]))

    ok_color = (255, 240, 0) if cursor == 2 else (200, 200, 230)
    ok_text = font_med.render("OK", True, ok_color)
    screen.blit(ok_text, (cx - ok_text.get_width() // 2, ys[2]))

    instr = font_med.render("WASD/Arrows • Left/Right to change • Enter to select", True, (140, 160, 220))
    screen.blit(instr, (w // 2 - instr.get_width() // 2, int(h * 0.78)))
    return cursor