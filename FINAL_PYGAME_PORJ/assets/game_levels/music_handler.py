import pygame
pygame.init()

class Beat(pygame.sprite.Sprite):
    def __init__(self, beat_color, x):
        super().__init__()
        
        self.image = pygame.surface.Surface((90, 60))
        self.image.fill(beat_color)
        
        self.rect = self.image.get_rect(center=(x, -10))
        
class MainMenu:
    def __init__(self):
    
        self.loops = 0
        
        self.song = pygame.mixer.music.load("assets/music/songs/main_menu.mp3")
        
    def Play(self):
        
        pygame.mixer.music.play(loops=self.loops)
        
    def Stop(self):
        
        pygame.mixer.music.pause()
        
    def Check(self):
        if not pygame.mixer.music.get_busy():
            self.loops += 1
            self.Play()

class LevelOne:
    def __init__(self):
        
        self.song = pygame.mixer.Sound("assets/music/songs/BLOOD_DRAIN.mp3")
        
    def Play(self):
        pygame.mixer.music.stop()
        self.song.play()
        
        