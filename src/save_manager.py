import json
import os
from datetime import datetime

class SaveManager:
    """Handles saving and loading game state"""
    
    def __init__(self, game):
        self.game = game
        self.save_file = "save.json"
    
    def save_game(self):
        """Save the current game state to a file"""
        save_data = {
            "bufos": self.game.bufos,
            "total_bufos_earned": self.game.total_bufos_earned,
            "click_power": self.game.click_power,
            "current_theme": self.game.current_theme,
            "buildings": self.game.buildings,
            "upgrades": self.game.upgrades,
            "achievements": self.game.achievements,
            "stats": self.game.stats
        }
        
        try:
            with open(self.save_file, "w") as f:
                json.dump(save_data, f)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self):
        """Load game state from a file"""
        try:
            if not os.path.exists(self.save_file):
                return False
                
            with open(self.save_file, "r") as f:
                save_data = json.load(f)
            
            # Load basic game state
            self.game.bufos = save_data.get("bufos", 0)
            self.game.total_bufos_earned = save_data.get("total_bufos_earned", 0)
            self.game.click_power = save_data.get("click_power", 1)
            self.game.current_theme = save_data.get("current_theme", "forest")
            
            # Load buildings
            for i, building_data in enumerate(save_data.get("buildings", [])):
                if i < len(self.game.buildings):
                    self.game.buildings[i]["owned"] = building_data.get("owned", 0)
            
            # Load upgrades
            for i, upgrade_data in enumerate(save_data.get("upgrades", [])):
                if i < len(self.game.upgrades):
                    self.game.upgrades[i]["purchased"] = upgrade_data.get("purchased", False)
            
            # Load achievements
            for i, achievement_data in enumerate(save_data.get("achievements", [])):
                if i < len(self.game.achievements):
                    self.game.achievements[i]["earned"] = achievement_data.get("earned", False)
            
            # Load stats
            self.game.stats = save_data.get("stats", self.game.stats)
            
            # Recalculate bufos per second
            self.game.bufos_per_second = self.game.calculate_bufos_per_second()
            
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def delete_save(self):
        """Delete the save file to start a new game"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                return True
            return False  # File didn't exist
        except Exception as e:
            print(f"Error deleting save file: {e}")
            return False
    
    def start_new_game(self):
        """Reset the game state to start a new game"""
        # Delete the existing save file first
        self.delete_save()
        
        # Reset game state
        self.game.bufos = 0
        self.game.total_bufos_earned = 0
        self.game.bufos_per_second = 0
        self.game.click_power = 1
        
        # Reset buildings
        for building in self.game.buildings:
            building["owned"] = 0
        
        # Reset upgrades
        for upgrade in self.game.upgrades:
            upgrade["purchased"] = False
        
        # Reset achievements
        for achievement in self.game.achievements:
            achievement["earned"] = False
        
        # Reset stats but keep the current start time
        self.game.stats = {
            "clicks": 0,
            "play_time": 0,
            "buildings_purchased": 0,
            "upgrades_purchased": 0,
            "game_started": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Recalculate bufos per second
        self.game.bufos_per_second = self.game.calculate_bufos_per_second()
        
        return True