import pygame
import random
from random import randint

class Enemy:
    def __init__(self, tier):
        self.tier = tier
        self.enemyimg = pygame.image.load(r"enemy.png")
        self.enemy = pygame.transform.scale(self.enemyimg, (65, 65))
        self.enemyrect = self.enemy.get_rect(center=(0, 100))
    def enspawn(self):
        if self.tier == 1:
            self.speed = 3
            self.health = 10
        elif self.tier == 2:
            self.speed = 2.5
            self.health = 20
        elif self.tier == 3:
            self.speed = 2
            self.health = 3
        elif self.tier == 4:
            self.speed = 1.5
            self.health = 4
        elif self.tier == 5:
            self.speed = 1
            self.health = 5
        self.x = randint(50, 550)
        self.enemyrect.centerx = self.x
    def enmove(self):
        if self.enemyrect.x == 740:
            self.enemyrect.x -= 4
        elif self.enemyrect.x == -20:
            self.enemyrect.x += 4
        elif self.enemyrect.x > 400:
            self.enemyrect.x += 4
        elif self.enemyrect < 400:
            self.enemyrect.x -= 4
        
