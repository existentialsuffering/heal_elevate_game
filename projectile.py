import pygame

class Projectile:
    def __init__(self, x, y, dx, dy, is_heal=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 9 if is_heal else 6.5
        self.life = 60
        self.is_heal = is_heal
        self.color = (120, 255, 255) if is_heal else (200, 60, 220)

    def update(self, walls):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.life -= 1
        for wall in walls:
            if wall.collidepoint(self.x, self.y):
                self.life = 0
                break
        return self.life > 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 8 if self.is_heal else 6)