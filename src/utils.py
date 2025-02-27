import math
import random
import pygame

def format_number(num):
    """Format a number with K, M, B suffixes for readability"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.1f}"

def calculate_building_cost(building):
    """Calculate the cost of a building based on how many are owned"""
    return math.floor(building["base_cost"] * (1.15 ** building["owned"]))

class FloatingTextManager:
    """Manages floating text effects in the game"""
    
    def __init__(self):
        self.floating_texts = []
    
    def add_floating_text(self, text, position, color=(255, 255, 255), size=24, lifetime=1.0, speed=1.0):
        """Add a new floating text effect"""
        self.floating_texts.append({
            "text": text,
            "position": list(position),
            "color": color,
            "size": size,
            "lifetime": lifetime,
            "speed": speed,
            "creation_time": pygame.time.get_ticks()
        })
    
    def update(self):
        """Update all floating texts"""
        current_time = pygame.time.get_ticks()
        for i in range(len(self.floating_texts) - 1, -1, -1):
            text = self.floating_texts[i]
            elapsed = (current_time - text["creation_time"]) / 1000.0
            
            if elapsed > text["lifetime"]:
                self.floating_texts.pop(i)
            else:
                # Move text upward
                text["position"][1] -= text["speed"]