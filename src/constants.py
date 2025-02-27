import pygame
import os

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 1024, 768
FPS = 60
FONT_SIZE = 24
LARGE_FONT_SIZE = 36

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Web-friendly paths
# For web deployment, assets should be in the root /assets folder
# Check if we're running in a browser
try:
    import platform
    IN_BROWSER = platform.system() == 'Emscripten'
except ImportError:
    IN_BROWSER = False

# Use relative paths that work both locally and in the browser
if IN_BROWSER:
    ASSETS_PATH = "./assets"
    SOUNDS_PATH = "./sounds"
else:
    # Local development paths
    ASSETS_PATH = "./assets"
    SOUNDS_PATH = "./sounds"
    #ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bufoclicker2.0/assets")
    #SOUNDS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bufoclicker2.0/sounds")

# Game themes
THEMES = {
    "forest": {
        "background": "forest_bg.png",
        "color": (34, 139, 34),
        "click_sound": "forest_click.wav",
        "music": "forest_music.mp3"
    },
    "desert": {
        "background": "desert_bg.png",
        "color": (210, 180, 140),
        "click_sound": "desert_click.wav",
        "music": "desert_music.mp3"
    },
    "swamp": {
        "background": "swamp_bg.png",
        "color": (107, 142, 35),
        "click_sound": "swamp_click.wav",
        "music": "swamp_music.mp3"
    }
}

# Cheat codes
CHEAT_CODES = {
    "ribbit": {"effect": "bufos", "value": 1000, "description": "Gain 1,000 bufos"},
    "hypnobufo": {"effect": "multiplier", "value": 10, "duration": 60, "description": "10x production for 60 seconds"},
    "allglory": {"effect": "unlock_all", "description": "Unlock all upgrades"},
    "todayistuesday": {"effect": "bufos", "value": 1000000, "description": "Gain 1,000,000 bufos"}
}