import pygame
import math
pygame.init()
pygame.mixer.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load(r"assets\sprites\player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        
        self.rect = self.image.get_rect(center=(550, 425))
        
        self.score = 0

        self.temp_beat = 0
        
        self.beat_hit = pygame.mixer.Sound(r"assets\music\sounds\beat_hit.mp3")
        self.beat_hit.set_volume(1.0)
        
        self.beat_miss = pygame.mixer.Sound(r"assets\music\sounds\beat_miss.mp3")
        self.beat_miss.set_volume(1.0)

    def Input(self, events, beats_list):
        for event in events:
            if event.type == pygame.KEYDOWN:
                for beat in beats_list:
                    if self.rect.colliderect(beat.rect):
                        if beat.direction == 1:
                            correct_key = pygame.K_UP
                        elif beat.direction == 2:
                            correct_key = pygame.K_DOWN
                        elif beat.direction == 3:
                            correct_key = pygame.K_RIGHT
                        elif beat.direction == 4:
                            correct_key = pygame.K_LEFT    
                        
                        if event.key == correct_key:
                            self.score += 1
                            beat.hit = True
                            beats_list.remove(beat)
                            self.beat_hit.play()
                            break
                        
                        elif event.key != correct_key:
                            self.score -= 1
                            beat.hit = True
                            beats_list.remove(beat)
                            self.beat_miss.play()
                            break
        
        for beat in beats_list:
        
            if beat.direction == 1:
                if beat.rect.y > self.rect.bottom + 10:
                    self.score -= 1
                    beat.hit = True
                    beats_list.remove(beat)
                    self.beat_miss.play()
                    break
            
            elif beat.direction == 2:
                if beat.rect.y < self.rect.top - 10:
                    self.score -= 1
                    beat.hit = True
                    beats_list.remove(beat)
                    self.beat_miss.play()
                    break
            
            elif beat.direction == 3:
                if beat.rect.x < self.rect.left - 10:
                    self.score -= 1
                    beat.hit = True
                    beats_list.remove(beat)
                    self.beat_miss.play()
                    break
            
            elif beat.direction == 4:
                if beat.rect.x > self.rect.right + 10:
                    self.score -= 1
                    beat.hit = True
                    beats_list.remove(beat)
                    self.beat_miss.play()
                    break
                
        return beats_list
                        
        
    def Update(self, screen, beats_list, events):
        new_beat_list = self.Input(events, beats_list)
        screen.blit(self.image, self.rect)
        return [self.score, new_beat_list]