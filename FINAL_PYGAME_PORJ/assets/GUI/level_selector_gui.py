import pygame
pygame.init()

class Main:
    def __init__(self, level_c_obj):

        self.level_c_obj = level_c_obj

        self.levels = self.level_c_obj.GetLevels()

        self.LevelDisplayData = {}
       
        self.font_path = r"assets\GUI\fonts\main_text.ttf"
        
        self.loaded = False
        
        self.status = "PAGE_1"
        self.level_chosen = None
        
        self.page_1_text = pygame.font.Font(self.font_path, 45).render("[LEVELS]", False, "green")
       
    def LoadLevelStuff(self):
        for level in self.levels:
            self.LevelDisplayData[level] = {}
            self.LevelDisplayData[level]["NAME"] = self.level_c_obj.GetLevelData(level)["NAME"]

    def SetLevels(self):
        
        self.LoadLevelStuff()
        
        perm_x = 550
        temp_y = 200
        
        texts = {}
        
        for level in self.LevelDisplayData: # increment by 50 gap text. I will do like top five                
            
            temp_y += 50
            
            font = pygame.font.Font(self.font_path, 32)
            
            self.LevelDisplayData[level]["TEXT"] = font.render(self.LevelDisplayData[level]["NAME"], False, "white")
            
            self.LevelDisplayData[level]["RECT"] = self.LevelDisplayData[level]["TEXT"].get_rect(center=(perm_x, temp_y))

    def SetLevelStartPage(self, level):
        
        gui_arrangement = {}
        
        small_font = pygame.font.Font(self.font_path, 25)
        title_font = pygame.font.Font(self.font_path, 32)
        start_font = pygame.font.Font(self.font_path, 30)

        gui_arrangement["TITLE"] = title_font.render(self.level_c_obj.GetLevelData(level)["NAME"], False, 'white')
        gui_arrangement["TITLE_RECT"] = gui_arrangement["TITLE"].get_rect(center=(550, 100))
     
        gui_arrangement["LEVEL_SPEED"] = small_font.render(f"Level Speed: {str(self.level_c_obj.GetLevelData(level)["LEVEL_SPEED"])}", False, 'green')
        gui_arrangement["LEVEL_SPEED_RECT"] = gui_arrangement["LEVEL_SPEED"].get_rect(center=(550, 300))
        
        gui_arrangement["DIFFICULTY"] = small_font.render(f"Level Difficulty: {str(self.level_c_obj.GetLevelData(level)["DIFFICULTY"])}", False, 'red')
        gui_arrangement["DIFFICULTY_RECT"] = gui_arrangement["DIFFICULTY"].get_rect(center=(550, 400))

        gui_arrangement["SONG_PATH"] = small_font.render(f"Song Path: {self.level_c_obj.GetLevelData(level)["SONG_PATH"]}", False, 'blue')
        gui_arrangement["SONG_PATH_RECT"] = gui_arrangement["SONG_PATH"].get_rect(center=(550, 500))
    
        gui_arrangement["START"] = start_font.render("START LEVEL", False, "green")
        gui_arrangement["START_RECT"] = gui_arrangement["START"].get_rect(center=(550, 650))
    
        return gui_arrangement

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for level in self.LevelDisplayData:
                        if self.LevelDisplayData[level]["RECT"].collidepoint(event.pos) and self.status == "PAGE_1":
                            self.status = "PAGE_2"
                            self.level_chosen = level
                    
                    if self.level_chosen is not None:
                        if self.SetLevelStartPage(self.level_chosen)["START_RECT"].collidepoint(event.pos):
                            return self.level_chosen
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.status == "PAGE_2":
                    self.status = "PAGE_1"              

    def Update(self, screen, events):
        if not self.loaded:
            self.SetLevels()
            self.loaded = True
        
        if self.status == "PAGE_1":
            screen.blit(self.page_1_text, (450, 50))
            
            for level in self.LevelDisplayData:
                screen.blit(self.LevelDisplayData[level]["TEXT"], self.LevelDisplayData[level]["RECT"])
        elif self.status == "PAGE_2":
            temp_level_gui = self.SetLevelStartPage(self.level_chosen)
            screen.blit(temp_level_gui["TITLE"], temp_level_gui["TITLE_RECT"])
            screen.blit(temp_level_gui["LEVEL_SPEED"], temp_level_gui["LEVEL_SPEED_RECT"])
            screen.blit(temp_level_gui["DIFFICULTY"], temp_level_gui["DIFFICULTY_RECT"])
            screen.blit(temp_level_gui["SONG_PATH"], temp_level_gui["SONG_PATH_RECT"])
            screen.blit(temp_level_gui["START"], temp_level_gui["START_RECT"])
            
        return self.event_handler(events)