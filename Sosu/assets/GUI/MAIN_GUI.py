import pygame
import math
import random
from assets.GUI import level_selector_gui

pygame.init()

# TODO: Add level selector and creator

class MAIN_MENU_GUI:
    def __init__(self, music, json_config_obj, level_creator_obj):
        
        self.MAIN_BACKGROUND = pygame.image.load(r"assets\backgrounds\MAIN_BACKGROUND.png").convert_alpha()
        self.MAIN_BACKGROUND.set_alpha(40)
        
        self.MAIN_JSON_CONFIG = json_config_obj
        self.MAIN_LVL_CREATOR = level_creator_obj
        
        self.MAIN_LVL_SELECTOR = level_selector_gui.Main(self.MAIN_LVL_CREATOR)
        
        self.level_name = ""
        
        self.current_stat_texts = {}
        
        self.music = music
        
        self.base_size = 100
        self.base_x = 550
        self.base_y = 100
        
        self.font_path = "assets/GUI/fonts/main_text.ttf"
        
        self.pulse = 0.0
        self.pulse_speed = 0.2
        self.pulse_decay = 0.85
        self.pulse_active = False
        
        self.Pulse_Event = pygame.USEREVENT + 1   
        
                                                                                    #600         500             400      
                                                                                  #  5_B         6_B             4_B     
        pygame.time.set_timer(self.Pulse_Event, 544) # 1 2 3 4 5__6 7 8 9 10 11__12 13 14 15 
        
        self.beats = 0
        
        # GUI BUTTONS ~~~~~~~~~~~~~~~~~~~~~~~~
        
        self.Start_Button_IMG = pygame.image.load(r"assets\GUI\mini_assets\start_button.png").convert_alpha()
        self.Start_Button_RECT = self.Start_Button_IMG.get_rect(center=(550, 400))
        
        self.Stats_Button_IMG = pygame.image.load(r"assets\GUI\mini_assets\stats_button.png").convert_alpha()
        self.Stats_Button_RECT = self.Stats_Button_IMG.get_rect(center=(550, 500))
    
        self.past_numx = 0
        self.past_numy = 0
        
        # GUI TEXT LEADERBOARD~~~~~~~~~
        
        font = pygame.font.Font(self.font_path, 100)
        self.LeaderBoardText = font.render("STATS", False, "white")
        self.LeaderBoardTextRect = self.LeaderBoardText.get_rect(center=(550, 100))
        
        self.current_tab = None
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        self.username = ""
        
        self.status = "MAIN_MENU"
          
    def trigger_pulse(self): 
        self.beats += 1
        self.pulse_active = not self.pulse_active
        if self.beats == 5: 
            self.pulse = 1.9
            self.beats = 0
        else: 
            self.pulse = 1.0
        
    def Text_Update(self, events): # Beat pulsing for game using list behind to last for most of song. TODO: Import all songs into audio thing and list ms when supposed to pulse
        self.music.Check()
        # 90 BPM (Unrelated but just here to save)
        
        # 90 / ~666 ms (UPDATE): I am just tweaking until works now (-_-)
        
        # REMEMBER: 5365 ms (When beats should start)
        
        for event in events:
            if event.type == self.Pulse_Event and pygame.mixer.music.get_pos() >= 5365:
                self.trigger_pulse()
                
        if self.pulse_active:
            self.pulse *= self.pulse_decay
            if self.pulse < 0.01:
                self.pulse = 0
                self.pulse_active = False
        
        scale = 1 + self.pulse * 0.25
        size = int(self.base_size * scale)
        
        font = pygame.font.Font(self.font_path, size)
        self.text = font.render("SOSU", False, "white")
        
        self.text_rect = self.text.get_rect(center=(self.base_x, self.base_y))
        
    def Button_Update(self, events): # Button anims and input for menu  
        for event in events: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Start_Button_RECT.collidepoint(pygame.mouse.get_pos()) and self.status != "PLAYING" and self.status != "STATS" and self.status != "CREATE" and self.status != "START" and self.status != "END_OF_LEVEL":
                    self.status = "START"
                elif self.Stats_Button_RECT.collidepoint(pygame.mouse.get_pos()) and self.status != "PLAYING" and self.status != "CREATE" and self.status != "START" and self.status != "END_OF_LEVEL":
                    self.status = "STATS"
                    self.current_stat_texts = self.GetStats()
                    
                for key, item in self.current_stat_texts.items():
                    if item.get("is_tab") and item["rect"].collidepoint(event.pos):
                        self.current_tab = item["tab_name"]
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.status == "STATS":
                    self.status = "MAIN_MENU"
        
        if self.Start_Button_RECT.collidepoint(pygame.mouse.get_pos()):
            numx = random.randint(-3, 3)
            numy = random.randint(-3, 3)
            
            if self.Start_Button_RECT.centerx >= 556: # 550, 400 
                self.Start_Button_RECT.centerx = 550
            elif self.Start_Button_RECT.centerx <= 544:
                self.Start_Button_RECT.centerx = 550
            
            if self.Start_Button_RECT.centery >= 406:
                self.Start_Button_RECT.centery = 400
            if self.Start_Button_RECT.centery <= 394:
                self.Start_Button_RECT.centery = 400
            
            self.Start_Button_RECT.x += numx
            self.Start_Button_RECT.y += numy
            self.past_numx = numx
            self.past_numy = numy
        elif self.Stats_Button_RECT.collidepoint(pygame.mouse.get_pos()):
            numx = random.randint(-3, 3)
            numy = random.randint(-3, 3)
            
            if self.Stats_Button_RECT.centerx >= 556: # 550, 500 
                self.Stats_Button_RECT.centerx = 550
            elif self.Stats_Button_RECT.centerx <= 544:
                self.Stats_Button_RECT.centerx = 550
            
            if self.Stats_Button_RECT.centery >= 506:
                self.Stats_Button_RECT.centery = 500
            if self.Stats_Button_RECT.centery <= 494:
                self.Stats_Button_RECT.centery = 500
            
            self.Stats_Button_RECT.x += numx
            self.Stats_Button_RECT.y += numy
            self.past_numx = numx
            self.past_numy = numy
                    
    def GetStats(self):
        arranged = self.MAIN_JSON_CONFIG.Arranged()
    
        if self.current_tab is None or self.current_tab not in arranged:
            self.current_tab = list(arranged.keys())[0] 
    
        texts = {}
        font = pygame.font.Font(self.font_path, 30)
        tab_font = pygame.font.Font(self.font_path, 25)
        perm_x = 550

    
        tab_x = 300
        for level_name in arranged.keys():
            color = "yellow" if level_name == self.current_tab else "white"
            tab_text = tab_font.render(f"[ {level_name} ]", False, color)
            tab_rect = tab_text.get_rect(center=(tab_x, 200))
            texts[f"tab_{level_name}"] = {"text": tab_text, "rect": tab_rect, "is_tab": True, "tab_name": level_name}
            tab_x += 280

        temp_y = 250
        for i, person in enumerate(arranged[self.current_tab]):
            temp_text = font.render(f"| {i+1} | {person['name']} | SCORE: {person['score']} |", False, "white")
            temp_y += 50
            temp_rect = temp_text.get_rect(center=(perm_x, temp_y))
            texts[f"text{i+1}"] = {"text": temp_text, "rect": temp_rect, "is_tab": False}

        return texts
    
    def Score_Level_Breakdown(self, score, amount_of_beats, level_data, screen, events):
        
        return_thing = ""
        
        gui_arrangement = {}
        
        small_font = pygame.font.Font(self.font_path, 25)
        title_font = pygame.font.Font(self.font_path, 32)
        start_font = pygame.font.Font(self.font_path, 30)

        gui_arrangement["TITLE"] = title_font.render(level_data["NAME"], False, 'white')
        gui_arrangement["TITLE_RECT"] = gui_arrangement["TITLE"].get_rect(center=(550, 100))
    
        gui_arrangement["SCORE_SECTION"] = start_font.render(f"~~~Score Details~~~", False, "green")
        gui_arrangement["SCORE_SECTION_RECT"] = gui_arrangement["SCORE_SECTION"].get_rect(center=(550, 250))
        
        gui_arrangement["SCORE_NUM"] = small_font.render(f"{str(score)} / {str(amount_of_beats)} ", False, "green")
        gui_arrangement["SCORE_NUM_RECT"] = gui_arrangement["SCORE_NUM"].get_rect(center=(550, 300))
        
        score_percentage = round((score / amount_of_beats) * 100)
        
        gui_arrangement["SCORE_PERCENTAGE"] = small_font.render(f"{str(score_percentage)}% ", False, "green")
        gui_arrangement["SCORE_PERCENTAGE_RECT"] = gui_arrangement["SCORE_PERCENTAGE"].get_rect(center=(550, 350))
    
        # RANKING/(A - F) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        if score_percentage >= 95:
            ranking = ["S", pygame.Color(255, 80, 80)]
        elif score_percentage >= 80:
            ranking = ["A", pygame.Color(255, 165, 0)]
        elif score_percentage >= 70:
            ranking = ["B", pygame.Color(255, 255, 80)]
        elif score_percentage >= 60:
            ranking = ["C", pygame.Color(100, 220, 100)]
        elif score_percentage >= 50:
            ranking = ["D", pygame.Color(80, 210, 210)]
        elif score_percentage >= 40:
            ranking = ["E", pygame.Color(120, 120, 230)]
        else:
            ranking = ["F", pygame.Color(210, 120, 210)]
    
    
        gui_arrangement["RANKING"] = small_font.render(f"{ranking[0]} RANK", False, ranking[1])
        gui_arrangement["RANKING_RECT"] = gui_arrangement["RANKING"].get_rect(center=(550, 500))
    
        if self.username != "":
            color = "green"
        else:
            color = "grey"
    
        gui_arrangement["CONTINUE"] = start_font.render("[CONTINUE]", False, color)
        gui_arrangement["CONTINUE_RECT"] = gui_arrangement["CONTINUE"].get_rect(center=(550, 750))
    
        screen.blit(gui_arrangement["TITLE"], gui_arrangement["TITLE_RECT"])
        
        screen.blit(gui_arrangement["SCORE_SECTION"], gui_arrangement["SCORE_SECTION_RECT"])
        screen.blit(gui_arrangement["SCORE_NUM"], gui_arrangement["SCORE_NUM_RECT"])
        screen.blit(gui_arrangement["SCORE_PERCENTAGE"], gui_arrangement["SCORE_PERCENTAGE_RECT"])
        screen.blit(gui_arrangement["RANKING"], gui_arrangement["RANKING_RECT"])
        
        screen.blit(gui_arrangement["CONTINUE"], gui_arrangement["CONTINUE_RECT"])
        
        gui_arrangement["USERNAME_SECTION"] = small_font.render(r"~\/~[ENTER USERNAME]~\/~", False, "red")
        gui_arrangement["USERNAME_SECTION_RECT"] = gui_arrangement["USERNAME_SECTION"].get_rect(center=(550, 580))
        
        gui_arrangement["USERNAME_SHOW"] = small_font.render(self.username, False, "white")
        gui_arrangement["USERNAME_SHOW_RECT"] = gui_arrangement["USERNAME_SHOW"].get_rect(center=(550, 630))

        screen.blit(gui_arrangement["USERNAME_SECTION"], gui_arrangement["USERNAME_SECTION_RECT"])

        screen.blit(gui_arrangement["USERNAME_SHOW"], gui_arrangement["USERNAME_SHOW_RECT"])
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gui_arrangement["CONTINUE_RECT"].collidepoint(event.pos):
                    return_thing = self.username
                    
        return return_thing 
    
    def Draw(self, screen, events, score=0, amount_of_beats=0, level_data={}):
        if self.status != "CREATE":
            self.Text_Update(events)
        self.Button_Update(events)
        
        # GUI BLITS ~~~~~~~~~~~~~~~~~~
        
        if self.status != "PLAYING":
            screen.blit(self.MAIN_BACKGROUND, (0, 0))
        
        if self.status == "MAIN_MENU":
            
            screen.blit(self.text, self.text_rect)
            screen.blit(self.Start_Button_IMG, self.Start_Button_RECT)
            screen.blit(self.Stats_Button_IMG, self.Stats_Button_RECT)
            
        elif self.status == "START":
            temp_lvl = self.MAIN_LVL_SELECTOR.Update(screen, events)
            if temp_lvl in self.MAIN_LVL_CREATOR.GetLevels():
                self.level_name = temp_lvl
            else:
                self.level_name = "CHOOSING"
                
            return [self.status, self.level_name]
            
        elif self.status == "STATS":
            self.current_stat_texts = self.GetStats()
            
            screen.blit(self.LeaderBoardText, self.LeaderBoardTextRect)
            font = pygame.font.Font(self.font_path, 50)
            space_to_exit_text = font.render("[SPACE] : EXIT", False, "white")
            space_to_exit_text_rect = space_to_exit_text.get_rect(center=(550, 780))
            screen.blit(space_to_exit_text, space_to_exit_text_rect)
            
            for key, item in self.current_stat_texts.items():
                screen.blit(item["text"], item["rect"])
                
        elif self.status == "END_OF_LEVEL":
            return self.Score_Level_Breakdown(score, amount_of_beats, level_data, screen, events)
        
        return [self.status, self.level_name] # Will only do something if status is equal to level id. Other than that it is just for class