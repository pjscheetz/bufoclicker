import pygame
import random
import math
import os
from datetime import datetime

from src.constants import WIDTH, HEIGHT, FPS, GOLD, THEMES, CHEAT_CODES, ASSETS_PATH
from src.buildings import BUILDINGS
from src.upgrades import UPGRADES
from src.achievements import ACHIEVEMENTS
from src.boosts import BOOSTS
from src.ui import UI
from src.utils import format_number, calculate_building_cost, FloatingTextManager
from src.audio import AudioManager
from src.save_manager import SaveManager
import asyncio

class BufoClicker:
    def __init__(self):
        # Initialize pygame synchronously
        pygame.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BufoClicker")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.bufos = 0
        self.bufos_per_second = 0
        self.total_bufos_earned = 0
        self.click_power = 1
        self.current_theme = "forest"
        
        # Game data
        self.buildings = self.initialize_buildings()
        self.upgrades = self.initialize_upgrades()
        self.achievements = self.initialize_achievements()
        self.boosts = self.initialize_boosts()
        
        # Stats
        self.stats = {
            "clicks": 0,
            "play_time": 0,
            "buildings_purchased": 0,
            "upgrades_purchased": 0,
            "game_started": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # UI elements
        self._bufo_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 200)
        self.last_update = pygame.time.get_ticks()
        self.show_buildings_menu = False
        self.show_upgrade_menu = False
        self.show_achievements = False
        self.show_stats = False
        self.show_theme_selector = False
        self.cheat_input = ""
        self.show_cheat_box = False
        self.cheat_message = ""
        self.cheat_message_time = 0
        
        # Golden bufo event
        self.golden_bufo_active = False
        self.golden_bufo_rect = None
        self.golden_bufo_end_time = 0
        self.golden_bufo_boost = None
        
        # Initialize managers
        self.floating_text_manager = FloatingTextManager()
        self.audio_manager = AudioManager()
        self.save_manager = SaveManager(self)
        
        # Debug variables
        self.debug_click_positions = []
        self.debug_mode = False  # Set to True to see debug info
        
        # Load assets first so UI can reference them
        self.load_assets()
        
        # Initialize UI after assets are loaded
        self.ui = UI(self)
        
        # Random events
        self.last_random_event = pygame.time.get_ticks()
        
        # Load game save and start music
        self.audio_manager.play_theme_music(self.current_theme)
    
    # Use a property to access bufo_rect to ensure it's always up to date
    @property
    def bufo_rect(self):
        return self._bufo_rect
    
    def initialize_buildings(self):
        """Create a deep copy of buildings to avoid modifying the original"""
        return [dict(building) for building in BUILDINGS]
    
    def initialize_upgrades(self):
        """Create a deep copy of upgrades to avoid modifying the original"""
        return [dict(upgrade) for upgrade in UPGRADES]
    
    def initialize_achievements(self):
        """Create a deep copy of achievements to avoid modifying the original"""
        return [dict(achievement) for achievement in ACHIEVEMENTS]
    
    def initialize_boosts(self):
        """Create a deep copy of boosts to avoid modifying the original"""
        return {k: dict(v) for k, v in BOOSTS.items()}
    
    def load_assets(self):
        """Load all game assets"""
        # Create directories if they don't exist
        os.makedirs(ASSETS_PATH, exist_ok=True)
        
        # Debug - print current directory and check if assets folder exists
        print(f"Current working directory: {os.getcwd()}")
        print(f"Assets path: {ASSETS_PATH}")
        print(f"Assets folder exists: {os.path.exists(ASSETS_PATH)}")
        
        # List files in assets directory if it exists
        if os.path.exists(ASSETS_PATH):
            print(f"Files in assets folder: {os.listdir(ASSETS_PATH)}")
        
        # Load images with better error handling
        try:
            # Main bufo image
            bufo_path = os.path.join(ASSETS_PATH, "bufo.png")
            print(f"Looking for bufo image at: {bufo_path}")
            print(f"File exists: {os.path.exists(bufo_path)}")
            
            if os.path.exists(bufo_path):
                self.bufo_img = pygame.image.load(bufo_path)
                self.bufo_img = pygame.transform.scale(self.bufo_img, (200, 200))
            else:
                print("Using fallback bufo image")
                self.bufo_img = pygame.Surface((200, 200))
                self.bufo_img.fill((0, 180, 0))
                pygame.draw.circle(self.bufo_img, (255, 215, 0), (100, 100), 80)
            
            # Golden bufo image
            golden_bufo_path = os.path.join(ASSETS_PATH, "golden_bufo.png")
            print(f"Looking for golden bufo image at: {golden_bufo_path}")
            print(f"File exists: {os.path.exists(golden_bufo_path)}")
            
            if os.path.exists(golden_bufo_path):
                self.golden_bufo_img = pygame.image.load(golden_bufo_path)
                self.golden_bufo_img = pygame.transform.scale(self.golden_bufo_img, (200, 200))
            else:
                print("Using fallback golden bufo image")
                self.golden_bufo_img = pygame.Surface((200, 200))
                self.golden_bufo_img.fill((255, 215, 0))
                pygame.draw.circle(self.golden_bufo_img, (0, 180, 0), (100, 100), 80)
            
            # Load building images
            self.building_imgs = {}
            for building in self.buildings:
                image_name = f"{building['name'].lower().replace(' ', '_')}.png"
                image_path = os.path.join(ASSETS_PATH, image_name)
                print(f"Looking for building image at: {image_path}")
                print(f"File exists: {os.path.exists(image_path)}")
                
                if os.path.exists(image_path):
                    img = pygame.image.load(image_path)
                    self.building_imgs[building['name']] = pygame.transform.scale(img, (50, 50))
                else:
                    print(f"Using fallback image for {building['name']}")
                    # Create a fallback colored image if missing
                    self.building_imgs[building['name']] = pygame.Surface((50, 50))
                    self.building_imgs[building['name']].fill((0, 180, 0))
                    pygame.draw.circle(self.building_imgs[building['name']], (255, 215, 0), (25, 25), 20)
            
            # Load background images
            self.background_imgs = {}
            for theme in THEMES:
                bg_path = os.path.join(ASSETS_PATH, THEMES[theme]["background"])
                print(f"Looking for background image at: {bg_path}")
                print(f"File exists: {os.path.exists(bg_path)}")
                
                if os.path.exists(bg_path):
                    self.background_imgs[theme] = pygame.image.load(bg_path)
                    self.background_imgs[theme] = pygame.transform.scale(self.background_imgs[theme], (WIDTH, HEIGHT))
                else:
                    print(f"Using fallback background for {theme}")
                    # Create a fallback colored background if missing
                    self.background_imgs[theme] = pygame.Surface((WIDTH, HEIGHT))
                    self.background_imgs[theme].fill(THEMES[theme]["color"])
                    
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Create fallback assets
            self.bufo_img = pygame.Surface((200, 200))
            self.bufo_img.fill((0, 180, 0))
            pygame.draw.circle(self.bufo_img, (255, 215, 0), (100, 100), 80)
            
            self.golden_bufo_img = pygame.Surface((200, 200))
            self.golden_bufo_img.fill((255, 215, 0))
            pygame.draw.circle(self.golden_bufo_img, (0, 180, 0), (100, 100), 80)
            
            # Create fallback building images
            self.building_imgs = {}
            for building in self.buildings:
                self.building_imgs[building['name']] = pygame.Surface((50, 50))
                self.building_imgs[building['name']].fill((0, 180, 0))
                pygame.draw.circle(self.building_imgs[building['name']], (255, 215, 0), (25, 25), 20)
            
            # Create fallback backgrounds
            self.background_imgs = {}
            for theme in THEMES:
                self.background_imgs[theme] = pygame.Surface((WIDTH, HEIGHT))
                self.background_imgs[theme].fill(THEMES[theme]["color"])
    
    def calculate_building_cost(self, building):
        """Calculate the cost of a building based on how many are owned"""
        return calculate_building_cost(building)
    
    def format_number(self, num):
        """Format a number with K, M, B suffixes for readability"""
        return format_number(num)
    
    def calculate_bufos_per_second(self):
        """Calculate the current rate of bufo production"""
        bps = 0
        for building in self.buildings:
            production = building["base_production"] * building["owned"]
            
            # Apply building-specific multipliers from upgrades
            for upgrade in self.upgrades:
                if upgrade["purchased"] and upgrade["effect"] == "building_multi" and upgrade["building"] == self.buildings.index(building):
                    production *= upgrade["value"]
            
            bps += production
        
        # Apply global multipliers from upgrades
        for upgrade in self.upgrades:
            if upgrade["purchased"] and upgrade["effect"] == "global_multi":
                bps *= upgrade["value"]
        
        # Apply temporary boosts
        for boost_name, boost in self.boosts.items():
            if boost["active"] and not boost.get("click_only", False):
                bps *= boost["multiplier"]
        
        return bps
    
    def add_floating_text(self, text, position, color=GOLD, size=24, lifetime=1.0, speed=1.0):
        """Add a floating text animation at the specified position"""
        self.floating_text_manager.add_floating_text(text, position, color, size, lifetime, speed)
    
    def click_bufo(self):
        """Handle clicking on the main bufo"""
        click_value = self.click_power
        
        # Apply click power multipliers from upgrades
        for upgrade in self.upgrades:
            if upgrade["purchased"] and upgrade["effect"] == "click_power":
                click_value *= upgrade["value"]
        
        # Apply temporary boosts
        for boost_name, boost in self.boosts.items():
            if boost["active"] and (boost.get("click_only", False) or not boost.get("click_only", False)):
                click_value *= boost["multiplier"]
        
        self.bufos += click_value
        self.total_bufos_earned += click_value
        self.stats["clicks"] += 1
        
        # Play click sound
        self.audio_manager.play_click_sound(self.current_theme)
        
        # Add floating text
        text_pos = (self.bufo_rect.centerx + random.randint(-50, 50), 
                    self.bufo_rect.centery + random.randint(-50, -20))
        self.add_floating_text(f"+{self.format_number(click_value)}", text_pos, GOLD)
        
        # Check click achievements
        for achievement in self.achievements:
            if not achievement["earned"] and achievement.get("type") == "clicks":
                if self.stats["clicks"] >= achievement["requirement"]:
                    self.unlock_achievement(achievement)
    
    def buy_building(self, index):
        """Purchase a building if the player can afford it"""
        building = self.buildings[index]
        cost = self.calculate_building_cost(building)
        
        if self.bufos >= cost:
            self.bufos -= cost
            building["owned"] += 1
            self.stats["buildings_purchased"] += 1
            self.bufos_per_second = self.calculate_bufos_per_second()
            
            # Play upgrade sound
            self.audio_manager.play_upgrade_sound()
            
            # Check building achievements
            for achievement in self.achievements:
                if not achievement["earned"] and achievement.get("type") == "buildings":
                    all_owned = all(b["owned"] > 0 for b in self.buildings)
                    if all_owned:
                        self.unlock_achievement(achievement)
            
            return True
        return False
    
    def buy_upgrade(self, index):
        """Purchase an upgrade if the player can afford it"""
        upgrade = self.upgrades[index]
        
        if not upgrade["purchased"] and self.bufos >= upgrade["cost"]:
            self.bufos -= upgrade["cost"]
            upgrade["purchased"] = True
            self.stats["upgrades_purchased"] += 1
            
            # Apply global multiplier effects
            if upgrade["effect"] == "global_multi" or upgrade["effect"] == "click_power" or upgrade["effect"] == "building_multi":
                self.bufos_per_second = self.calculate_bufos_per_second()
            
            # Play upgrade sound
            self.audio_manager.play_upgrade_sound()
            
            return True
        return False
    
    def trigger_random_event(self):
        """Trigger a random boost event"""
        event_type = random.choice(list(self.boosts.keys()))
        boost = self.boosts[event_type]
        
        if not boost["active"]:
            boost["active"] = True
            boost["end_time"] = pygame.time.get_ticks() + (boost["duration"] * 1000)
            
            # Play boost sound
            self.audio_manager.play_boost_sound()
            
            # Add notification
            self.add_floating_text(boost["description"], (WIDTH // 2 - 150, HEIGHT // 2 - 50), 
                                  GOLD, 36, 3.0, 0.5)
    
    def update_boosts(self):
        """Update all active boosts"""
        current_time = pygame.time.get_ticks()
        
        for boost_name, boost in self.boosts.items():
            if boost["active"] and current_time >= boost["end_time"]:
                boost["active"] = False
                boost["end_time"] = None
    
    def update_random_events(self):
        """Check if a random event should be triggered"""
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_random_event) / 1000.0
        
        # For testing, increase the chance temporarily
        # Reduce chance for more rarity (0.0005 = average of 1 every ~33 minutes)
        # For testing use 0.01 = average of 1 every ~100 seconds
        if random.random() < (0.00001 * elapsed) and not self.golden_bufo_active:
            self.spawn_golden_bufo()
            self.last_random_event = current_time
    
    def spawn_golden_bufo(self):
        """Spawn a golden bufo at a random position that can be clicked for a boost"""
        # Create a new attribute to track the golden bufo
        print("Spawning golden bufo!")
        self.golden_bufo_active = True
        
        # Choose a random position (keeping away from edges)
        margin = 100
        x = random.randint(margin, WIDTH - margin - 100)
        y = random.randint(margin, HEIGHT - margin - 100)
        
        # Create a rect for the golden bufo (smaller than regular bufo)
        self.golden_bufo_rect = pygame.Rect(x, y, 100, 100)
        
        # Choose which boost will be activated when clicked
        self.golden_bufo_boost = random.choice(list(self.boosts.keys()))
        
        # Add a floating notification
        self.add_floating_text("Golden Bufo appeared!", 
                            (WIDTH // 2 - 120, HEIGHT // 4), 
                            GOLD, 36, 2.0, 0.5)
        
        # Set a timeout for the golden bufo (disappears after 10 seconds if not clicked)
        self.golden_bufo_end_time = pygame.time.get_ticks() + 3000
        
    def activate_golden_bufo_boost(self):
        """Activate the boost associated with the clicked golden bufo"""
        # Deactivate the golden bufo
        print("Golden bufo clicked! Activating boost.")
        self.golden_bufo_active = False
        self.golden_bufo_rect = None
        
        # Activate the selected boost
        boost = self.boosts[self.golden_bufo_boost]
        boost["active"] = True
        boost["end_time"] = pygame.time.get_ticks() + (boost["duration"] * 1000)
        
        # Play boost sound
        self.audio_manager.play_boost_sound()
        
        # Add notification
        self.add_floating_text(f"Boost activated: {boost['description']}", 
                             (WIDTH // 2 - 150, HEIGHT // 2 - 50), 
                             GOLD, 36, 3.0, 0.5)
        
        # Add stats for golden bufos caught
        if "golden_bufos_clicked" not in self.stats:
            self.stats["golden_bufos_clicked"] = 0
        self.stats["golden_bufos_clicked"] += 1
        
    def unlock_achievement(self, achievement):
        """Unlock an achievement and display a notification"""
        if not achievement["earned"]:
            achievement["earned"] = True
            self.add_floating_text(f"Achievement Unlocked: {achievement['name']}", 
                                 (WIDTH // 2 - 200, HEIGHT // 4), 
                                 GOLD, 36, 3.0, 0.5)
            # Play achievement sound
            self.audio_manager.play_achievement_sound()
    
    def check_achievements(self):
        """Check if any achievements should be unlocked"""
        for achievement in self.achievements:
            if not achievement["earned"]:
                if "type" not in achievement or achievement["type"] is None:
                    # Bufo count achievement
                    if self.total_bufos_earned >= achievement["requirement"]:
                        self.unlock_achievement(achievement)
                
                elif achievement["type"] == "time" and self.stats["play_time"] >= achievement["requirement"]:
                    self.unlock_achievement(achievement)
                
                elif achievement["type"] == "clicks" and self.stats["clicks"] >= achievement["requirement"]:
                    self.unlock_achievement(achievement)
                
                elif achievement["type"] == "buildings":
                    all_owned = all(b["owned"] > 0 for b in self.buildings)
                    if all_owned:
                        self.unlock_achievement(achievement)
                
                elif achievement["type"] == "golden_bufos" and "golden_bufos_clicked" in self.stats:
                    if self.stats["golden_bufos_clicked"] >= achievement["requirement"]:
                        self.unlock_achievement(achievement)
    
    def process_cheat_code(self, code):
        """Process a cheat code and apply its effects"""
        if code in CHEAT_CODES:
            cheat = CHEAT_CODES[code]
            
            if cheat["effect"] == "bufos":
                self.bufos += cheat["value"]
                self.total_bufos_earned += cheat["value"]
                self.cheat_message = f"Cheat activated: {cheat['description']}"
            
            elif cheat["effect"] == "multiplier":
                # Create a temporary boost
                temp_boost = {
                    "active": True,
                    "end_time": pygame.time.get_ticks() + (cheat["duration"] * 1000),
                    "multiplier": cheat["value"],
                    "duration": cheat["duration"],
                    "description": cheat["description"]
                }
                self.boosts["cheat_boost"] = temp_boost
                self.cheat_message = f"Cheat activated: {cheat['description']}"
            
            elif cheat["effect"] == "unlock_all":
                for upgrade in self.upgrades:
                    upgrade["purchased"] = True
                self.bufos_per_second = self.calculate_bufos_per_second()
                self.cheat_message = f"Cheat activated: {cheat['description']}"
            
            self.cheat_message_time = pygame.time.get_ticks()
            return True
        
        return False
    
    def transform_coordinates(self, browser_pos):
        """
        Transform browser/canvas coordinates to game coordinates
        accounting for any scaling that may be happening
        """
        try:
            # Get the actual canvas size in the browser
            canvas_width = pygame.display.get_surface().get_width()
            canvas_height = pygame.display.get_surface().get_height()
            
            # Get the logical size we're using in our game
            logical_width, logical_height = WIDTH, HEIGHT
            
            # Calculate the scale factors (avoid division by zero)
            scale_x = logical_width / max(canvas_width, 1)
            scale_y = logical_height / max(canvas_height, 1)
            
            # Transform the coordinates
            game_x = browser_pos[0] * scale_x
            game_y = browser_pos[1] * scale_y
            
            # Debug output
            if self.debug_mode:
                print(f"Browser pos: {browser_pos}, Game pos: ({game_x}, {game_y})")
                print(f"Canvas: {canvas_width}x{canvas_height}, Logical: {logical_width}x{logical_height}")
            
            return (game_x, game_y)
        except Exception as e:
            print(f"Error transforming coordinates: {e}")
            return browser_pos  # Return original coordinates as fallback
    
    def process_click(self, pos):
        """Process a click or touch at the given position"""
        # Store click positions for debugging
        if self.debug_mode:
            self.debug_click_positions.append(pos)
            if len(self.debug_click_positions) > 10:
                self.debug_click_positions.pop(0)
            print(f"Click detected at position: {pos}")
        
        # Check if golden bufo was clicked
        if self.golden_bufo_active and self.golden_bufo_rect and self.golden_bufo_rect.collidepoint(pos):
            print("Golden bufo clicked!")
            self.activate_golden_bufo_boost()
            return  # Skip other processing
        
        # Handle cheat box input if active
        if self.show_cheat_box:
            submit_button, cancel_button = self.ui.draw_cheat_box()
            
            if submit_button.collidepoint(pos):
                print("Submit button clicked")
                if self.process_cheat_code(self.cheat_input):
                    self.bufos_per_second = self.calculate_bufos_per_second()
                self.cheat_input = ""
                self.show_cheat_box = False
            elif cancel_button.collidepoint(pos):
                print("Cancel button clicked")
                self.cheat_input = ""
                self.show_cheat_box = False
            return  # Skip other processing
        
        # Handle menu interactions
        if self.show_buildings_menu:
            # Check building clicks
            y_pos = 80
            building_height = 80
            
            for i, building in enumerate(self.buildings):
                building_rect = pygame.Rect(WIDTH // 2 - 300, y_pos, 600, building_height)
                
                if building_rect.collidepoint(pos):
                    print(f"Building {building['name']} clicked")
                    self.buy_building(i)
                    break
                
                y_pos += building_height + 10
            
            # Check back button
            back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
            if back_button.collidepoint(pos):
                print("Back button clicked from buildings menu")
                self.show_buildings_menu = False
            return
        
        elif self.show_upgrade_menu:
            # Check upgrade clicks - using the new available_upgrades approach
            available_upgrades = [u for u in self.upgrades if not u["purchased"]]
            
            if available_upgrades:
                upgrades_per_row = 2
                upgrade_width = (WIDTH - 60) // upgrades_per_row
                upgrade_height = 60
                
                for i, upgrade in enumerate(available_upgrades):
                    # Calculate position - matches the UI drawing
                    col = i % upgrades_per_row
                    row = i // upgrades_per_row
                    
                    x_pos = 30 + (col * upgrade_width)
                    y_pos = 80 + (row * (upgrade_height + 10))
                    
                    upgrade_rect = pygame.Rect(x_pos, y_pos, upgrade_width - 10, upgrade_height)
                    
                    if upgrade_rect.collidepoint(pos):
                        print(f"Upgrade {upgrade['name']} clicked")
                        # Find the original index in the full upgrades list
                        original_index = self.upgrades.index(upgrade)
                        self.buy_upgrade(original_index)
                        break
            
            # Check back button
            back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
            if back_button.collidepoint(pos):
                print("Back button clicked from upgrades menu")
                self.show_upgrade_menu = False
            return
        
        elif self.show_achievements:
            # Check back button
            back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
            if back_button.collidepoint(pos):
                print("Back button clicked from achievements menu")
                self.show_achievements = False
            return
        
        elif self.show_stats:
            # Check back button
            back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
            if back_button.collidepoint(pos):
                print("Back button clicked from stats menu")
                self.show_stats = False
            return
        
        elif self.show_theme_selector:
            # Check theme clicks
            y_pos = 80
            theme_height = 100
            
            for theme_name in THEMES:
                theme_rect = pygame.Rect(WIDTH // 2 - 200, y_pos, 400, theme_height)
                
                if theme_rect.collidepoint(pos):
                    print(f"Theme {theme_name} selected")
                    self.current_theme = theme_name
                    self.audio_manager.play_theme_music(self.current_theme)
                    break
                
                y_pos += theme_height + 10
            
            # Check back button
            back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
            if back_button.collidepoint(pos):
                print("Back button clicked from theme selector")
                self.show_theme_selector = False
            return
        
        # If no menus are active, check main bufo
        if self.bufo_rect.collidepoint(pos):
            print("Main bufo clicked!")
            self.click_bufo()
            return
        
        # Check main menu buttons
        button_y = HEIGHT - 50
        button_width = 150
        button_spacing = 160
        
        # Buildings button (first position)
        buildings_button = pygame.Rect(10, button_y, button_width, 40)
        if buildings_button.collidepoint(pos):
            print("Buildings button clicked")
            self.show_buildings_menu = True
            return
        
        # Upgrades button (second position)
        upgrades_button = pygame.Rect(10 + button_spacing, button_y, button_width, 40)
        if upgrades_button.collidepoint(pos):
            print("Upgrades button clicked")
            self.show_upgrade_menu = True
            return
        
        # Achievements button (third position)
        achievements_button = pygame.Rect(10 + button_spacing * 2, button_y, button_width, 40)
        if achievements_button.collidepoint(pos):
            print("Achievements button clicked")
            self.show_achievements = True
            return
        
        # Stats button (fourth position)
        stats_button = pygame.Rect(10 + button_spacing * 3, button_y, button_width, 40)
        if stats_button.collidepoint(pos):
            print("Stats button clicked")
            self.show_stats = True
            return
        
        # Themes button (fifth position)
        themes_button = pygame.Rect(10 + button_spacing * 4, button_y, button_width, 40)
        if themes_button.collidepoint(pos):
            print("Themes button clicked")
            self.show_theme_selector = True
            return
        
        # Cheat code button (top-right corner)
        cheat_button = pygame.Rect(WIDTH - 50, 10, 40, 40)
        if cheat_button.collidepoint(pos):
            print("Cheat button clicked")
            self.show_cheat_box = True
            return
    
    def handle_events(self):
        """Process user input events with better browser support"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle both mouse clicks and touch events
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN, pygame.FINGERUP):
                # Get click position based on event type
                if event.type == pygame.MOUSEBUTTONDOWN:
                    browser_pos = event.pos
                else:  # FINGERDOWN or FINGERUP event
                    # For touch events, coordinates are normalized [0-1]
                    browser_pos = (event.x * WIDTH, event.y * HEIGHT)
                
                # Transform coordinates to account for screen scaling
                game_pos = self.transform_coordinates(browser_pos)
                
                # Process the click with transformed coordinates
                self.process_click(game_pos)
            
            elif event.type == pygame.KEYDOWN:
                # Handle cheat code input
                if self.show_cheat_box:
                    if event.key == pygame.K_RETURN:
                        if self.process_cheat_code(self.cheat_input):
                            self.bufos_per_second = self.calculate_bufos_per_second()
                        self.cheat_input = ""
                        self.show_cheat_box = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.cheat_input = self.cheat_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.cheat_input = ""
                        self.show_cheat_box = False
                    else:
                        # Add character to cheat input (with max length)
                        if len(self.cheat_input) < 20:
                            self.cheat_input += event.unicode
    
    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update) / 1000.0  # Convert to seconds
        
        # Update play time (in seconds)
        self.stats["play_time"] += delta_time
        
        # Update bufos from automatic production
        self.bufos += self.bufos_per_second * delta_time
        self.total_bufos_earned += self.bufos_per_second * delta_time
        
        # Update temporary boosts
        self.update_boosts()
        
        # Check for random events
        self.update_random_events()
        
        # Check if golden bufo has timed out
        if self.golden_bufo_active and current_time >= self.golden_bufo_end_time:
            print("Golden bufo disappeared")
            self.golden_bufo_active = False
            self.golden_bufo_rect = None
            self.add_floating_text("Golden Bufo disappeared!", 
                                 (WIDTH // 2 - 120, HEIGHT // 4), 
                                 (200, 200, 200), 24, 2.0, 0.5)
        
        # Check achievements
        self.check_achievements()
        
        # Update floating texts
        self.floating_text_manager.update()
        
        self.last_update = current_time
    
    def draw(self):
        """Render the game with debug overlay"""
        # Draw main UI
        self.ui.draw_main_ui()
        
        # Draw floating texts
        self.ui.draw_floating_texts()
        
        # Draw debugging elements if debug mode is enabled
        if self.debug_mode and self.debug_click_positions:
            # Draw the last 10 click positions
            for i, pos in enumerate(self.debug_click_positions):
                # Draw a small circle at each click position
                radius = 10 - i  # Decreasing size for older clicks
                color = (255, 0, 0) if i == 0 else (200, 0, 0)  # Brighter for most recent
                pygame.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), radius, 2)
            
            # Draw debug info for bufo rect
            pygame.draw.rect(self.screen, (0, 255, 0), self.bufo_rect, 2)
        
        # Draw buildings menu if active
        if self.show_buildings_menu:
            self.ui.draw_buildings_menu()
        
        # Draw upgrades menu if active
        if self.show_upgrade_menu:
            self.ui.draw_upgrades_menu()
        
        # Draw achievements menu if active
        if self.show_achievements:
            self.ui.draw_achievements_menu()
        
        # Draw stats menu if active
        if self.show_stats:
            self.ui.draw_stats_menu()
        
        # Draw theme selector if active
        if self.show_theme_selector:
            self.ui.draw_theme_selector()
        
        # Draw cheat input box if active
        if self.show_cheat_box:
            self.ui.draw_cheat_box()
        
        pygame.display.flip()
    
    async def async_run(self):
        """Async main game loop for Pygbag"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw game
            self.draw()
            
            # Allow browser to process events - using a small delay
            # to improve responsiveness in browser environment
            await asyncio.sleep(0.01)
        
        # Save game on exit
        self.save_manager.save_game()
        pygame.quit()
        
    def run(self):
        """Compatibility method for traditional Pygame"""
        try:
            asyncio.run(self.async_run())
        except Exception as e:
            print(f"Error in game loop: {e}")
            pygame.quit()