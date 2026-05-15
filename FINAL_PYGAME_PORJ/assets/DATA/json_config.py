import json
import os
from assets.LEVELCREATOR import lvl_c

class Config:
    def __init__(self):
        try:
            with open(r"assets\DATA\scores.json", "r") as file:
                self.data = json.load(file)
        except:
            with open(r"assets\DATA\scores.json", "w") as file:
                json.dump({}, file)
                self.data = {}
        
    def Add_Player(self, name, level):
        if self.GetNum() < 5:
            self.data[f"USER_{str(self.GetNum() + 1)}"] = {}
            self.data[f"USER_{str(self.GetNum())}"]["name"] = name
            self.data[f"USER_{str(self.GetNum())}"]["level"] = level
            self.Save()
    
    def Add_Score(self, score_data): # Adds score to newest player
        self.data[F"USER_{self.GetNum()}"]["score"] = f"{round(score_data[0])}% | {score_data[1]} RANK"
        self.Save()
        
    def GetAllData(self):
        return self.data

    def GetNum(self):
        num = 0
        for i in self.data:
            num += 1
        return num
    
    def Arranged(self):
        final_data = {}
        
        for level in lvl_c.Main().GetLevels():
            level_name = lvl_c.Main().GetLevelData(level)["NAME"]
            
            level_players = [p for p in self.data.values() if p["level"] == level_name]
            
            level_players.sort(key=lambda x: x["score"], reverse=True)
            
            final_data[level_name] = level_players
        
        return final_data
        
    def Save(self):
        with open(r"assets\DATA\scores.json", 'w') as file:
            json.dump(self.data, file, indent=4)