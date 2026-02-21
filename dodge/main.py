import pygame
import time
import random
from random import randint
import sys
import enemy
import playership
from playership import Bullet
print(playership.__file__) 
print(dir(playership))
pygame.init()

screen = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

background = pygame.image.load(r"background.png")
background = pygame.transform.scale(background, (1100, 1100))
background_rect = background.get_rect(center=(400, 400))

winscreen = pygame.image.load(r"winscreen.png")
winscreen = pygame.transform.scale(winscreen, (800, 800))
winscreen_rect = winscreen.get_rect(center=(400,400))

score = 0
scorestr = str(score)
font = pygame.font.Font(None, 50) 
scoreC = font.render(f"Score: {score}", True, (255, 255, 255))

playerimg = pygame.image.load(r"player.png")
player = pygame.transform.scale(playerimg, (85, 85))
playerect = player.get_rect(center=(400, 700))

bullet_speed = 6

    
pspeed = 2

enemy_set = enemy.Enemy(1)
enemy_surf = enemy_set.enemy
enemy_rect = enemy_set.enemyrect
enemy_rect.center = (enemy_rect.x, enemy_rect.y)
enemy_rect.x, enemy_rect.y = 400, 100


shot = False

enemySpawnx = enemy_set.enspawn()

CHANGE_DIR = pygame.USEREVENT + 1

pygame.time.set_timer(CHANGE_DIR, 1000)

enemy_speed_x = random.randint(-200, 200)

while True:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
        if event.type == CHANGE_DIR:
            enemy_speed_x = random.randint(-200, 200)
                
    screen.blit(background, (background_rect.x, background_rect.y))
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        playerect.x -= pspeed
    elif key[pygame.K_d] or key[pygame.K_RIGHT]:
        playerect.x += pspeed
    
    try:
        
        if enemy_rect.x >= 740:
            enemy_rect.x = 739
        elif enemy_rect.x <= -20:
            enemy_rect.x = -19
        else:
            enemy_rect.x += enemy_speed_x * (dt/1000)
        
    except:
        print("Enemy Broken")
        
    if key[pygame.K_SPACE] and not shot:
        bullet_set = playership.Bullet()
        bullet_surf = bullet_set.bullet_surf
        bullet_rect = bullet_set.bullet_rect
        bullet_rect.x, bullet_rect.y = playerect.x, playerect.y
        bullet_rect.x, bullet_rect.y = bullet_rect.x, bullet_rect.y
        shot = True
    
    
    
    
       
    if playerect.x >= 740:
        playerect.x = 740
    elif playerect.x <= -20:
        playerect.x = -20
    
    
    
    if shot:
        if enemy_rect.colliderect(bullet_rect):
            del bullet_set
            score += 1
            scoreC = font.render(f"Score: {score}", True, (255, 255, 255))

            del enemy_rect, enemy_surf, enemySpawnx
            
            enemySpawnx = enemy_set.enspawn()
            enemy_surf = enemy_set.enemy
            enemy_rect = enemy_set.enemyrect
            
            shot = False
        
        elif bullet_rect.y <= enemy_rect.y:
            del bullet_rect, bullet_surf
            shot = False
        
        try:
            bullet_rect.y -= 9
            screen.blit(bullet_surf, (bullet_rect.x, bullet_rect.y))  
        except:
            print("")  
    
    
    screen.blit(player, (playerect.x, playerect.y))
    
    try:
        screen.blit(enemy_surf, (enemy_rect.x, enemy_rect.y))
    except:
        print("Enemy Broken")
    
    screen.blit(scoreC, (0, 0))
    
    if score >= 10 and score < 20:
        pspeed = 3
    elif score >= 20 and score < 29:
        pspeed = 4
    elif score >= 30 and score < 39:
        pspeed = 5
    elif score >= 40 and score < 49:
        pspeed = 6
    elif score >= 50 and score < 59:
        pspeed = 7
    elif score >= 100:
        screen.blit(winscreen, (winscreen_rect.x, winscreen_rect.y))
            
    
    pygame.display.flip()
    
    clock.tick(60)