import pygame
import sys
import random
from random import randint
pygame.init()

screen = pygame.display.set_mode((800, 800))

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 800))
background_rect = background.get_rect(center=(400,400))

score = 0
font = pygame.font.Font(None, 50)
score_surf = font.render(f"Score: {score}", False, "White")

player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (100, 100))
player_rect = player.get_rect(center=(400,400))

apple = pygame.image.load("apple.png")
apple = pygame.transform.scale(apple, (75, 75))
apple_rect = apple.get_rect()

def spawn():
    global apple_rect
    apple_rect.x = randint(50, 750)
    apple_rect.y = randint(50, 750)

clock = pygame.time.Clock()

pSpeed = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    key = pygame.key.get_pressed()        
    if key[pygame.K_w]:
        player_rect.y -= pSpeed
    elif key[pygame.K_s]:
        player_rect.y += pSpeed
    elif key[pygame.K_d]:
        player_rect.x += pSpeed
    elif key[pygame.K_a]:
        player_rect.x -= pSpeed
    
    if player_rect.colliderect(apple_rect):
        spawn()
        score += 1
        score_surf = font.render(f"Score: {score}", False, "White")
        pSpeed += 0.5
        
    
    screen.blit(background, (background_rect.x, background_rect.y))
    screen.blit(apple, (apple_rect.x, apple_rect.y))
    screen.blit(player, (player_rect.x, player_rect.y))
    screen.blit(score_surf, (350, 50))
    
    
    pygame.display.flip()
    
    clock.tick(60)