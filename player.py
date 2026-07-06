import pygame
import math
from projectile import Projectile

class Player:
    def __init__(self, class_type):
        self.class_type = class_type
        self.size = 24
        self.speed = 5.8 if class_type == "Monk" else 4.8
        self.color = (0, 255, 150) if class_type == "Monk" else (255, 220, 100) if class_type == "Priest" else (200, 80, 255)
        self.reset()
        self.invisible = False
        self.invis_timer = 0
        self.invis_cooldown = 0
        self.last_smash = 0

    def reset(self):
        self.x = 400
        self.y = 300
        self.health = 100
        self.heal_charge = 100
        self.projectiles = []
        self.last_shot = 0

    def update(self, keys, mouse_pos, mouse_click, current_time, walls, enemies):
        # Movement
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
        
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            nx = self.x + (dx / length) * self.speed
            ny = self.y + (dy / length) * self.speed
            if not any(w.collidepoint(nx, self.y) for w in walls):
                self.x = nx
            if not any(w.collidepoint(self.x, ny) for w in walls):
                self.y = ny

        self.x = max(30, min(770, self.x))
        self.y = max(30, min(570, self.y))

        # Monk Invisibility
        if self.class_type == "Monk":
            if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and self.invis_cooldown <= 0:
                self.invisible = True
                self.invis_timer = current_time + 4000
                self.invis_cooldown = current_time + 8000

            if self.invisible and current_time > self.invis_timer:
                self.invisible = False
            if current_time > self.invis_cooldown and self.invis_cooldown > 0:
                self.invis_cooldown = 0

        # Close Range Smash
        if self.class_type == "Monk" and (keys[pygame.K_SPACE] or mouse_click) and current_time - self.last_smash > 300:
            for e in enemies:
                if not e.saved and math.hypot(self.x - e.x, self.y - e.y) < 65:
                    e.elevation += 45
            self.last_smash = current_time

        # Other classes projectiles
        elif self.class_type != "Monk":
            if (keys[pygame.K_SPACE] or mouse_click) and current_time - self.last_shot > 220:
                tx = mouse_pos[0]
                ty = mouse_pos[1]
                dx = tx - self.x
                dy = ty - self.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    self.projectiles.append(Projectile(self.x, self.y, dx/dist, dy/dist, is_heal=True))
                    self.last_shot = current_time

    def draw(self, surface):
        color = (*self.color, 90) if self.invisible else self.color
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)
        if not self.invisible:
            pygame.draw.circle(surface, (100, 255, 255), (int(self.x), int(self.y)), self.size + 22, 5)
        bar_w = 80
        pygame.draw.rect(surface, (80,0,0), (self.x - bar_w//2, self.y - 50, bar_w, 8))
        pygame.draw.rect(surface, (0, 255, 120), (self.x - bar_w//2, self.y - 50, bar_w * (self.health/100), 8))