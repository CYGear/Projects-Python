import pygame
import os
import json

# When opened It will create new folder for custom levels

class Main:
    def __init__(self):
        self.custom_levels = {}
        self.directory = "assets/LEVELS/custom_levels"
        try:
            for entry in os.scandir(self.directory):
                if entry.is_file():
                    self.custom_levels[entry.name] = {}
                    self.custom_levels[entry.name]["path"] = entry.path
        
        except:
            os.makedirs(r"assets/LEVELS/custom_levels", exist_ok=True)
    
    def CreateLevel(self, file_name, display_name, song_path, difficulty, background):
        with open(f"{self.directory}/{file_name}", "w") as file:
            json.dump({}, file)
            
        with open(f"{self.directory}/{file_name}", "r") as file:  
            temp_data = json.load(file)
            temp_data["NAME"] = display_name
            temp_data["SONG_PATH"] = song_path
            temp_data["DIFFICULTY"] = difficulty
            temp_data["BACKGROUND"] = background
            
        with open(f"{self.directory}/{file_name}", "w") as file:
            json.dump(temp_data, file, indent=4)
    
    def EditLevel(self, file_name, notes_dictionary = {}):
        with open(f"{self.directory}/{file_name}", "r") as file:  
            temp_data = json.load(file)
            temp_data["NOTES"] = notes_dictionary
            
        with open(f"{self.directory}/{file_name}", "w") as file:
            json.dump(temp_data, file, indent=4)
    
    def GetLevels(self):
        self.SaveLevels()  
        return self.custom_levels
    
    def GetLevelData(self, file_name):
        try:
            with open(f"{self.directory}/{file_name}") as file:
                return json.load(file)
        except Exception as e:
            print(f"Invalid file: {file_name!r} -> {e}")
    
    def SaveLevels(self):
        for entry in os.scandir(self.directory):
            if entry.is_file():
                self.custom_levels[entry.name] = {}
                self.custom_levels[entry.name]["path"] = entry.path