import sys
import pygame
import random
pygame.init()

screen = pygame.display.set_mode((700, 600))

win_screen = pygame.image.load("win_screen.png")

state = "Fun Game!"

pygame.display.set_caption(state)

FONT = pygame.font.SysFont("Arial", 30)

coinAmount = 0
coinCounter = FONT.render(f"Coins: {coinAmount}", False, "Black")
coin = pygame.image.load("coin.png")
coin_rect = coin.get_rect(center=(300, 500))

sleep_coin = pygame.image.load("sleep_coin.png")
sleep_coin_rect = sleep_coin.get_rect(center=(200, 200))

player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (80, 80))
player_rect = player.get_rect(center=(350, 300))
player_name = FONT.render("Mar", False, "Black")

clock = pygame.time.Clock()

hell_state = pygame.image.load("hell.png")

hell_active = False

active_coin = "normal"

def spawnC():
    global coin_rect, sleep_coin_rect, coinAmount, coinCounter, NspawnedC, active_coin

    # If we just collected a coin, decide what spawns next:
    if active_coin == "sleep":
        # sleep coin gives +5 and resets the streak
        coinAmount += 5
        coinCounter = FONT.render(f"Coins: {coinAmount}", False, "Black")
        NspawnedC = 0
        active_coin = "normal"

        # spawn a normal coin next
        coin_rect.center = (random.randint(50, 650), random.randint(50, 550))

    else:
        # normal coin gives +1 and increases streak
        coinAmount += 1
        coinCounter = FONT.render(f"Coins: {coinAmount}", False, "Black")
        NspawnedC += 1

        if NspawnedC >= 4:
            # spawn sleep coin
            active_coin = "sleep"
            sleep_coin_rect.center = (random.randint(50, 650), random.randint(50, 550))
        else:
            # spawn normal coin
            coin_rect.center = (random.randint(50, 650), random.randint(50, 550))

    


coin_active = False

NspawnedC = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_LSHIFT] and not hell_active:
                hell_active = True
    
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player_rect.y -= 3
    elif key[pygame.K_s]:
        player_rect.y += 3
    elif key[pygame.K_d]:
        player_rect.x += 3
    elif key[pygame.K_a]:
        player_rect.x -= 3
        
    if hell_active:
        screen.blit(hell_state, (0,0))
        player_rect.x, player_rect.y = random.randint(50, 650), random.randint(50, 550)
        state = "HELL HELL HELL HELL HELL"
        pygame.display.set_caption(state)
    else:
        screen.fill("White")
    
    if active_coin == "normal" and player_rect.colliderect(coin_rect):
        spawnC()

    if active_coin == "sleep" and player_rect.colliderect(sleep_coin_rect):
        spawnC()

    
    if NspawnedC == 4:
        screen.blit(sleep_coin, (sleep_coin_rect.x, sleep_coin_rect.y))
    else:
        screen.blit(coin, (coin_rect.x, coin_rect.y))
    screen.blit(player, (player_rect.x, player_rect.y))
    screen.blit(player_name, (player_rect.x + 10, player_rect.y - 50))
    screen.blit(coinCounter, (300, 50))
    
    if coinAmount >= 100:
        screen.blit(win_screen, (0,0))
        state = "WIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        pygame.display.set_caption(state)
    
    pygame.display.flip()
    
    clock.tick(60)
    