import pygame
import sys

#------------

from assets import player
from assets.LEVELS.game_levels import music_handler
from assets.GUI import MAIN_GUI

from assets.DATA import json_config

from assets.LEVELCREATOR import lvl_c as level_creator

# LEVELS---------------------------------
from assets.LEVELS.game_levels import level_loader

#------------

pygame.init()
screen = pygame.display.set_mode((1100, 850))

icon = pygame.image.load("assets\icon.png")

pygame.display.set_icon(icon)
pygame.display.set_caption("Sosu")

clock = pygame.time.Clock()

#MAIN SETUP---------------

music_handler_thing = music_handler.MainMenu()


js_obj = json_config.Config()
'''
js_obj.Add_Player("TEST_1")
js_obj.Add_Score(500)
'''

level_creator_obj = level_creator.Main()

main_menu_gui = MAIN_GUI.MAIN_MENU_GUI(music_handler_thing, js_obj, level_creator_obj)

#--------------------------

player_obj = player.Player()

level_loader_obj = level_loader.Main_Level(level_creator_obj)

GAME_STATE = [" ", " "]

GAME_STATE[0] = "MAIN_MENU"
          
ending_dec = "PLAYING"

# FPS-COUNTER-----

font = pygame.font.Font(r"assets\GUI\fonts\main_text.ttf", 32)
          
while True:
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if GAME_STATE[0] == "PLAYING":
            level_loader_obj.event_handler(event)
            
    screen.fill("black")

    if GAME_STATE[0] == "MAIN_MENU" or GAME_STATE[0] == "STATS":
        GAME_STATE[0], GAME_STATE[1] = main_menu_gui.Draw(screen, events)

    elif GAME_STATE[0] == "START":
        if main_menu_gui.level_name != "CHOOSING":
            main_menu_gui.status = "PLAYING"
            level_loader_obj.Load_Level(GAME_STATE[1])
            beat_list = level_loader_obj.GetBeatList()
            GAME_STATE[0] = "PLAYING"
        else:
            GAME_STATE[0], GAME_STATE[1] = main_menu_gui.Draw(screen, events)
    
    elif GAME_STATE[0] == "PLAYING": 
        if not ending_dec == "PAUSED":
            ending = player_obj.Update(screen, beat_list, events)
            beat_list = ending[1]
            fps_counter_text = font.render(f"FPS: {str(round(clock.get_fps()))}", False, "green")
            screen.blit(fps_counter_text, (0, 50))
            
        ending_dec = level_loader_obj.Update_Level(screen, ending[0])
        
        if ending_dec == "COMPLETE":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/songs/main_menu.mp3")
            pygame.mixer.music.play(loops=-1)
            
            level_loader_obj.notes = []
            level_loader_obj.paused = False
            level_loader_obj.pause_return = "PAUSED"
            
            main_menu_gui.MAIN_LVL_SELECTOR.status = "PAGE_1"
            
            last_level_chosen = main_menu_gui.MAIN_LVL_SELECTOR.level_chosen
            main_menu_gui.MAIN_LVL_SELECTOR.level_chosen = None
            main_menu_gui.level_name = "CHOOSING"
            main_menu_gui.status = "END_OF_LEVEL"
            GAME_STATE[0] = "END_OF_LEVEL"
            ending_dec = "PLAYING"
            
        elif ending_dec == "EXITED":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/songs/main_menu.mp3")
            pygame.mixer.music.play(loops=-1)
            
            level_loader_obj.notes = []
            level_loader_obj.paused = False
            level_loader_obj.pause_return = "PAUSED"
            
            main_menu_gui.MAIN_LVL_SELECTOR.status = "PAGE_1"
            
            last_level_chosen = main_menu_gui.MAIN_LVL_SELECTOR.level_chosen
            main_menu_gui.MAIN_LVL_SELECTOR.level_chosen = None
            main_menu_gui.level_name = "CHOOSING"
            main_menu_gui.status = "MAIN_MENU"
            GAME_STATE[0] = "MAIN_MENU"
            ending_dec = "PLAYING"
        
            
    elif GAME_STATE[0] == "END_OF_LEVEL":
        new_p_name = main_menu_gui.Draw(screen, events, score=ending[0], level_data=main_menu_gui.MAIN_LVL_CREATOR.GetLevelData(last_level_chosen), amount_of_beats=level_loader_obj.GetBeatAmount_GLOBAL(last_level_chosen))
                                    
        if new_p_name != "":                                                
            js_obj.Add_Player(new_p_name, main_menu_gui.MAIN_LVL_CREATOR.GetLevelData(last_level_chosen)["NAME"])
            perc = (ending[0] / level_loader_obj.GetBeatAmount_GLOBAL(last_level_chosen) * 100)
            
            if perc >= 95:
                rank = "S"
            elif perc >= 80:
                rank = "A"
            elif perc >= 70:
                rank = "B"
            elif perc >= 60:
                rank = "C"
            elif perc >= 50:
                rank = "D"
            elif perc >= 40:
                rank = "E"
            else:
                rank = "F"
                
            score_data_temp = [perc, rank]
            js_obj.Add_Score(score_data_temp)
            main_menu_gui.status = "MAIN_MENU"
            GAME_STATE[0] = "MAIN_MENU"
            
    pygame.display.flip()
    clock.tick(70)