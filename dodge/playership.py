import pygame
    
class Bullet:
    def __init__(self):
        self.bullet_surf = pygame.image.load(r"bullet.png")
        self.bullet_surf = pygame.transform.scale(self.bullet_surf, (85, 85))
        self.bullet_rect = self.bullet_surf.get_rect()
        