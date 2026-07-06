import pygame
import math
import random
from projectile import Projectile

class EnemySoul:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.elevation = 25
        self.size = 19
        self.shoot_timer = random.randint(800, 1600)
        self.saved = False
        self.projectiles = []

    def update(self, player, current_time, walls):
        if self.saved: return
        dist = math.hypot(self.x - player.x, self.y - player.y)
        if dist < 55 and player.class_type != "Exorcist":
            self.elevation += 1.4
            player.heal_charge = min(100, player.heal_charge + 0.6)
        if self.elevation >= 100:
            self.saved = True
            return

        # Do NOT shoot at invisible Monk
        if not (player.class_type == "Monk" and player.invisible):
            if current_time > self.shoot_timer:
                dx = player.x - self.x
                dy = player.y - self.y
                d = math.hypot(dx, dy)
                if d > 0:
                    self.projectiles.append(Projectile(self.x, self.y, dx/d, dy/d, is_heal=False))
                self.shoot_timer = current_time + random.randint(700, 1400)

        self.projectiles = [p for p in self.projectiles if p.update(walls)]

    def draw(self, surface):
        if self.saved:
            pygame.draw.circle(surface, (255, 245, 100), (int(self.x), int(self.y)), self.size + 8)
            return
        col = (180, 60, 220) if self.elevation < 65 else (80, 200, 255)
        pygame.draw.circle(surface, col, (int(self.x), int(self.y)), self.size)
        bar_w = 60
        pygame.draw.rect(surface, (80,0,80), (self.x - bar_w//2, self.y - 35, bar_w, 6))
        pygame.draw.rect(surface, (140, 255, 255), (self.x - bar_w//2, self.y - 35, bar_w * (self.elevation/100), 6))