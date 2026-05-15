import pygame
pygame.init()
        
class MainMenu:
    def __init__(self):
    
        self.loops = 0
        
        self.song = pygame.mixer.music.load("assets/music/songs/main_menu.mp3")
        
    def Play(self):
        
        pygame.mixer.music.play(loops=-1)
        
    def Stop(self):
        
        pygame.mixer.music.pause()
        
    def Check(self):
        if not pygame.mixer.music.get_busy():
            self.Play()

class Level_Songs:
    def __init__(self, path):
        
        self.path = path
        
    def Play(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
        
    def Pause(self):
        pygame.mixer.music.pause()
        
    def Unpause(self):
        pygame.mixer.music.unpause()
        
    def Stop(self):
        pygame.mixer.music.stop()
        
        