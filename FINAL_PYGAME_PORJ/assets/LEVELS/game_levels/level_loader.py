import pygame
from assets.LEVELS.game_levels import music_handler
pygame.init()

class Beat(pygame.sprite.Sprite): # Beat class will be inside template so that child level files can inherit this class
    def __init__(self, direction, spawn_time, speed=2):
        super().__init__()
        
        self.direction = direction
        
        self.speed = speed
        
        self.spawn_time = spawn_time # Time it spawns in song
        
        self.spawned = False
        
        self.hit = False
        
        # Direction = 1 UP
        # 2 DOWN
        # 3 RIGHT
        # 4 LEFT
        
        path = 0
        pos = [0,0]
        
        if self.direction == 1:
            path = r"assets\sprites\up_beat.png"
            pos[0], pos[1] = 550, -5
            
        elif self.direction == 2:
            path = r"assets\sprites\down_beat.png"
            pos[0], pos[1] = 550, 855
            
        elif self.direction == 3:
            path = r"assets\sprites\right_beat.png"
            pos[0], pos[1] = 1105, 425
            
        elif self.direction == 4:
            path = r"assets\sprites\left_beat.png"
            pos[0], pos[1] = -5, 425
             
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=tuple(pos))
        
    def Move(self):        
        if self.direction == 1:
            self.rect.y += self.speed
        elif self.direction == 2: 
            self.rect.y -= self.speed
        elif self.direction == 3: 
            self.rect.x -= self.speed
        elif self.direction == 4:
            self.rect.x += self.speed
                          
    def Update(self, screen, current_time):
        if self.spawned and not self.hit:
            self.Move()
            screen.blit(self.image, self.rect)
        
        if current_time >= self.spawn_time * 1000 and not self.spawned:
            self.spawned = True

class Main_Level:
    def __init__(self, level_creator_obj):
        self.MAIN_LVL_C = level_creator_obj
        
        # Level_data-------
        self.level = None
        self.level_speed = 2
        
        self.notes = []
        
        self.level_song = ""
        
        self.level_start_time = 0
        
        self.font = pygame.font.Font(r"assets\GUI\fonts\main_text.ttf", 32)
        
        self.level_background = ""
        
        self.paused = False
        
        self.pause_return = "PAUSED"
        
        self.last_score = -1
        
        self.score_text = None
        
    def Load_Level(self, file_name):
        
        self.level = self.MAIN_LVL_C.GetLevelData(file_name)
        
        self.level_speed = self.level["LEVEL_SPEED"]
        
        for note in self.level["NOTES"].keys():    

            self.notes.append(Beat(self.level["NOTES"][note]["direction"], self.level["NOTES"][note]["spawn_time"],  self.level["NOTES"][note]["speed"]))
            
        self.level_song = music_handler.Level_Songs(self.level["SONG_PATH"])
        
        self.level_background = pygame.image.load(self.level["BACKGROUND"]).convert_alpha()
        self.level_background = pygame.transform.scale(self.level_background, (1100, 850))
        self.level_background.set_alpha(128)
        
        self.level_song.Play()
        
        self.level_start_time = pygame.time.get_ticks()
        
        self.pause_start = 0
        self.total_paused_time = 0
        
    def GetBeatList(self):
        
        return self.notes
    
    def GetBeatAmount_GLOBAL(self, file_name):
        level = self.MAIN_LVL_C.GetLevelData(file_name)
        
        return len(level["NOTES"])
    
    def GetPauseMenu(self):
        
        texts = {}
        
        title_font = pygame.font.Font(r"assets\GUI\fonts\main_text.ttf", 32)
        button_font = pygame.font.Font(r"assets\GUI\fonts\main_text.ttf", 28)
        
        texts["TITLE"] = title_font.render("[PAUSED]", False, "white")
        texts["TITLE_RECT"] = texts["TITLE"].get_rect(center=(550, 100)) 
        
        texts["CONTINUE"] = button_font.render("[CONTINUE]", False, "green")
        texts["CONTINUE_RECT"] = texts["CONTINUE"].get_rect(center=(400, 650))
        
        texts["EXIT"] = button_font.render("[EXIT]", False, "red")
        texts["EXIT_RECT"] = texts["EXIT"].get_rect(center=(700, 650))
        
        return texts
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = True
                self.pause_return = "PAUSED"
                self.pause_start = pygame.time.get_ticks()
                self.level_song.Pause()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.GetPauseMenu()["CONTINUE_RECT"].collidepoint(event.pos):
                self.paused = False
                self.pause_return = "PAUSED"
                self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                self.level_song.Unpause()
                
            elif self.GetPauseMenu()["EXIT_RECT"].collidepoint(event.pos):
                self.pause_return = "EXITED"
                self.level_song.Stop()
    
    def Update_Level(self, screen, score):
        current_time = (pygame.time.get_ticks() - self.level_start_time) - self.total_paused_time
        
        if not self.paused:
            screen.blit(self.level_background, (0,0))
            
            if score != self.last_score:
                self.score_text = self.font.render(f"Score: {str(score)}", False, "green")
                self.last_score = score
                
            screen.blit(self.score_text, (0,0))
        
            for note in self.notes:
                note.Update(screen, current_time)
        
        else:
            temp_pause_menu = self.GetPauseMenu()
            screen.blit(temp_pause_menu["TITLE"], temp_pause_menu["TITLE_RECT"])
            screen.blit(temp_pause_menu["CONTINUE"], temp_pause_menu["CONTINUE_RECT"])
            screen.blit(temp_pause_menu["EXIT"], temp_pause_menu["EXIT_RECT"])
        
        if not self.paused:  
            if len(self.notes) <= 0:
                return "COMPLETE"
      
            return "PLAYING"
        else:
            return self.pause_return
