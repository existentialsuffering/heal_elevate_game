import pygame

def get_level_data(level):
    if level == 1:
        walls = [pygame.Rect(200,100,400,20), pygame.Rect(200,400,400,20), pygame.Rect(150,150,20,300)]
        enemies = [(300,200), (500,300), (400,450)]
    elif level == 2:
        walls = [pygame.Rect(100,100,20,400), pygame.Rect(680,100,20,400), pygame.Rect(250,200,300,20), pygame.Rect(250,380,300,20)]
        enemies = [(200,150), (600,150), (200,450), (600,450)]
    else:
        walls = [pygame.Rect(150,150,500,20), pygame.Rect(150,430,500,20), pygame.Rect(150,150,20,300), pygame.Rect(630,150,20,300)]
        enemies = [(250,250), (400,200), (550,350), (300,420), (500,280)]
    return walls, enemies