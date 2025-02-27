"""
Main entry point for BufoClicker web deployment using Pygbag.
This file handles initialization and asset setup for the web environment.
"""

import asyncio
import os
import pygame
import sys
import platform

# Check if we're running in a browser
try:
    IN_BROWSER = platform.system() == 'Emscripten'
except ImportError:
    IN_BROWSER = False

# Create essential directories for web compatibility
os.makedirs('assets', exist_ok=True)
os.makedirs('sounds', exist_ok=True)

# Import BufoClicker class
from src.game import BufoClicker

# This function creates placeholder assets if they don't exist
def create_placeholder_assets():
    """Create minimal placeholder assets for the game to run"""
    print("Checking for placeholder assets...")
    
    if not os.path.exists("assets") or not os.path.exists("assets/bufo.png"):
        print("Creating placeholder assets...")
        
        # Initialize pygame for asset creation
        pygame.init()
        
        # Create bufo image
        bufo = pygame.Surface((200, 200), pygame.SRCALPHA)
        bufo.fill((0, 0, 0, 0))
        pygame.draw.circle(bufo, (0, 180, 0), (100, 100), 80)
        pygame.draw.circle(bufo, (255, 215, 0), (75, 75), 20)
        pygame.draw.circle(bufo, (255, 215, 0), (125, 75), 20)
        pygame.image.save(bufo, "assets/bufo.png")
        
        # Create golden bufo
        golden = pygame.Surface((200, 200), pygame.SRCALPHA)
        golden.fill((0, 0, 0, 0))
        pygame.draw.circle(golden, (255, 215, 0), (100, 100), 80)
        pygame.draw.circle(golden, (0, 180, 0), (75, 75), 20)
        pygame.draw.circle(golden, (0, 180, 0), (125, 75), 20)
        pygame.image.save(golden, "assets/golden_bufo.png")
        
        # Create theme backgrounds
        themes = {
            "forest": (34, 139, 34),
            "desert": (210, 180, 140),
            "swamp": (107, 142, 35)
        }
        
        for theme, color in themes.items():
            bg = pygame.Surface((1024, 768))
            bg.fill(color)
            pygame.image.save(bg, f"assets/{theme}_bg.png")
            
            # Create empty sound files
            with open(f"sounds/{theme}_click.wav", 'wb') as f:
                f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
            with open(f"sounds/{theme}_music.mp3", 'wb') as f:
                f.write(b'ID3\x03\x00\x00\x00\x00\x00\x00')
        
        # Create building images
        buildings = ["tadpole", "froglet", "bufo", "bufo_magnus", 
                    "giant_bufo", "hypnobufo", "bufo_shrine", "bufo_factory"]
        for building in buildings:
            img = pygame.Surface((50, 50))
            img.fill((0, 180, 0))
            pygame.draw.circle(img, (255, 215, 0), (25, 25), 20)
            pygame.image.save(img, f"assets/{building}.png")
        
        # Create sound effects
        for sound in ["achievement.wav", "upgrade.wav", "boost.wav", "default_click.wav"]:
            with open(f"sounds/{sound}", 'wb') as f:
                f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
        
        print("Placeholder assets created successfully!")
    else:
        print("Assets already exist")

# The async entry point that Pygbag uses
async def main():
    """
    Main entry point for the web version of BufoClicker.
    Pygbag will call this function to start the game.
    """
    # Initialize pygame
    pygame.init()
    
    # Print debug info
    print("Starting BufoClicker...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Available files in current directory: {os.listdir('.')}")
    
    if os.path.exists('assets'):
        print(f"Assets directory contents: {os.listdir('assets')}")
    
    # Create placeholder assets if needed
    create_placeholder_assets()
    
    # Create and start the game
    print("Initializing game...")
    game = BufoClicker()
    
    print("Starting game loop...")
    # Call the async run method
    await game.async_run()

# This is the entry point Pygbag will use
if __name__ == "__main__":
    if IN_BROWSER:
        print("Running in browser environment")
    else:
        print("Running in desktop environment")
    asyncio.run(main())