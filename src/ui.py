import pygame
from src.constants import WIDTH, HEIGHT, WHITE, BLACK, BLUE, GREEN, PURPLE, RED, GOLD, FONT_SIZE, LARGE_FONT_SIZE, THEMES

class UI:
    """
    Handles all UI rendering for the BufoClicker game.
    
    This class is responsible for drawing all elements of the game interface,
    including menus, buttons, and visual effects.
    """
    
    def __init__(self, game):
        """Initialize the UI with a reference to the game instance"""
        self.game = game
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.large_font = pygame.font.SysFont("Arial", LARGE_FONT_SIZE)
        
        # Button definitions for easy reuse
        self.button_height = 40
        self.standard_button_width = 150
        self.small_button_width = 100
        
        # Cache commonly used UI elements
        self.back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
    
    def create_button(self, x, y, width, height, color, text, text_color=WHITE):
        """Helper to create a button with text"""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.game.screen, color, button_rect)
        
        button_text = self.font.render(text, True, text_color)
        self.game.screen.blit(button_text, (
            button_rect.centerx - button_text.get_width() // 2,
            button_rect.centery - button_text.get_height() // 2
        ))
        
        return button_rect
    
    def draw_semi_transparent_background(self):
        """Draw a semi-transparent black background for menus"""
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        bg_surface.set_alpha(200)
        bg_surface.fill(BLACK)
        self.game.screen.blit(bg_surface, (0, 0))
    
    def draw_title(self, title_text):
        """Draw a centered title for menus"""
        title_surface = self.large_font.render(title_text, True, WHITE)
        self.game.screen.blit(title_surface, (
            WIDTH // 2 - title_surface.get_width() // 2,
            20
        ))
    
    def draw_back_button(self):
        """Draw a standard back button and return its rect"""
        return self.create_button(
            WIDTH // 2 - 50,
            HEIGHT - 50,
            100,
            40,
            BLUE,
            "Back"
        )
    
    def draw_main_ui(self):
        """Draw the main game interface"""
        # Draw current theme background
        self.game.screen.blit(self.game.background_imgs[self.game.current_theme], (0, 0))
        
        # Draw bufo image (golden if boost is active)
        if any(boost["active"] for boost_name, boost in self.game.boosts.items()):
            self.game.screen.blit(self.game.golden_bufo_img, self.game.bufo_rect)
        else:
            self.game.screen.blit(self.game.bufo_img, self.game.bufo_rect)
        
        # Draw golden bufo if active (special smaller golden bufo that appears randomly)
        if hasattr(self.game, 'golden_bufo_active') and self.game.golden_bufo_active and self.game.golden_bufo_rect:
            # Scale the golden bufo image to the correct size
            scaled_golden_img = pygame.transform.scale(self.game.golden_bufo_img, 
                                               (self.game.golden_bufo_rect.width, 
                                                self.game.golden_bufo_rect.height))
            
            # Draw the golden bufo at its position
            self.game.screen.blit(scaled_golden_img, self.game.golden_bufo_rect)
            
            # Add a pulsing effect to make it more noticeable
            pulse_time = pygame.time.get_ticks() % 1000 / 1000  # 0 to 1 over 1 second
            pulse_size = int(10 * pulse_time)  # 0 to 10 pixels
            glow_rect = self.game.golden_bufo_rect.inflate(pulse_size, pulse_size)
            pygame.draw.rect(self.game.screen, GOLD, glow_rect, 2)
            
            # Add a countdown timer over it
            time_left = max(0, int((self.game.golden_bufo_end_time - pygame.time.get_ticks()) / 1000))
            time_text = self.font.render(f"{time_left}s", True, GOLD)
            self.game.screen.blit(time_text, 
                                 (self.game.golden_bufo_rect.centerx - time_text.get_width() // 2, 
                                  self.game.golden_bufo_rect.top - 20))
        
        # Draw bufo counter
        bufo_text = self.large_font.render(f"{self.game.format_number(self.game.bufos)} Bufos", True, WHITE)
        self.game.screen.blit(bufo_text, (WIDTH // 2 - bufo_text.get_width() // 2, 50))
        
        # Draw bufos per second
        bps_text = self.font.render(f"{self.game.format_number(self.game.bufos_per_second)} bufos per second", True, WHITE)
        self.game.screen.blit(bps_text, (WIDTH // 2 - bps_text.get_width() // 2, 100))
        
        # Draw active boosts
        boost_y = 150
        for boost_name, boost in self.game.boosts.items():
            if boost["active"]:
                time_left = (boost["end_time"] - pygame.time.get_ticks()) / 1000
                boost_text = self.font.render(f"{boost_name.replace('_', ' ').title()}: {time_left:.1f}s", True, GOLD)
                self.game.screen.blit(boost_text, (WIDTH // 2 - boost_text.get_width() // 2, boost_y))
                boost_y += 30
        
        # Draw main menu buttons
        button_y = HEIGHT - 50
        button_width = self.standard_button_width
        button_spacing = 160
        
        # Create main menu buttons (removed Save/New Game)
        buttons = [
            # x, y, width, height, color, text, text_color
            (10, button_y, button_width, self.button_height, GOLD, "Buildings",BLACK),
            (10 + button_spacing, button_y, button_width, self.button_height, GOLD, "Upgrades",BLACK),
            (10 + button_spacing * 2, button_y, button_width, self.button_height, GOLD, "Achievements",BLACK),
            (10 + button_spacing * 3, button_y, button_width, self.button_height, GOLD, "Stats",BLACK),
            (10 + button_spacing * 4, button_y, button_width, self.button_height, GOLD, "Themes", BLACK),
        ]
        
        # Draw all buttons
        for button_data in buttons:
            self.create_button(*button_data)
        
        # Cheat code button
        cheat_button = pygame.Rect(WIDTH - 50, 10, 40, 40)
        pygame.draw.rect(self.game.screen, PURPLE, cheat_button)
        cheat_text = self.font.render("C", True, WHITE)
        self.game.screen.blit(cheat_text, (
            cheat_button.centerx - cheat_text.get_width() // 2,
            cheat_button.centery - cheat_text.get_height() // 2
        ))
        
        # Draw cheat message if active
        if self.game.cheat_message and pygame.time.get_ticks() - self.game.cheat_message_time < 3000:
            cheat_msg_text = self.font.render(self.game.cheat_message, True, GOLD)
            self.game.screen.blit(cheat_msg_text, (WIDTH // 2 - cheat_msg_text.get_width() // 2, 20))
        
        # Draw bufos per second
        bps_text = self.font.render(f"{self.game.format_number(self.game.bufos_per_second)} bufos per second", True, WHITE)
        self.game.screen.blit(bps_text, (WIDTH // 2 - bps_text.get_width() // 2, 100))
        
        # Draw active boosts
        boost_y = 150
        for boost_name, boost in self.game.boosts.items():
            if boost["active"]:
                time_left = (boost["end_time"] - pygame.time.get_ticks()) / 1000
                boost_text = self.font.render(f"{boost_name.replace('_', ' ').title()}: {time_left:.1f}s", True, GOLD)
                self.game.screen.blit(boost_text, (WIDTH // 2 - boost_text.get_width() // 2, boost_y))
                boost_y += 30
        

    def draw_buildings_menu(self):
        """Draw the buildings menu"""
        # Draw semi-transparent background
        self.draw_semi_transparent_background()
        
        # Draw title
        self.draw_title("Buildings")
        
        # Draw buildings list
        y_pos = 80
        building_height = 80  # Increased height to accommodate images
        
        for i, building in enumerate(self.game.buildings):
            # Building container
            building_rect = pygame.Rect(WIDTH // 2 - 300, y_pos, 600, building_height)
            
            # Determine if building is affordable
            affordable = self.game.bufos >= self.game.calculate_building_cost(building)
            color = GREEN if affordable else RED
            
            pygame.draw.rect(self.game.screen, color, building_rect, 2)
            
            # Draw building image
            image_rect = pygame.Rect(building_rect.x + 10, building_rect.y + 15, 50, 50)
            self.game.screen.blit(self.game.building_imgs[building['name']], image_rect)
            
            # Building name and owned
            name_text = self.font.render(f"{building['name']} ({building['owned']})", True, WHITE)
            self.game.screen.blit(name_text, (building_rect.x + 70, building_rect.y + 10))
            
            # Building description
            desc_text = self.font.render(building['description'], True, GOLD)
            self.game.screen.blit(desc_text, (building_rect.x + 70, building_rect.y + 40))
            
            # Building cost and production
            cost = self.game.calculate_building_cost(building)
            cost_text = self.font.render(f"Cost: {self.game.format_number(cost)} bufos", True, WHITE)
            prod_text = self.font.render(f"Produces: {self.game.format_number(building['base_production'])} bps", True, WHITE)
            
            self.game.screen.blit(cost_text, (building_rect.right - cost_text.get_width() - 10, building_rect.y + 10))
            self.game.screen.blit(prod_text, (building_rect.right - prod_text.get_width() - 10, building_rect.y + 40))
            
            y_pos += building_height + 10
        
        # Back button
        self.draw_back_button()
    
    def draw_upgrades_menu(self):
        """Draw the upgrades menu"""
        # Draw semi-transparent background
        self.draw_semi_transparent_background()
        
        # Draw title
        self.draw_title("Upgrades")
        
        # Draw upgrades list
        upgrade_height = 60
        upgrades_per_row = 2
        upgrade_width = (WIDTH - 60) // upgrades_per_row
        
        # Count available (unpurchased) upgrades
        available_upgrades = [u for u in self.game.upgrades if not u["purchased"]]
        
        if not available_upgrades:
            # No upgrades available
            no_upgrades_text = self.font.render("All upgrades purchased!", True, GOLD)
            self.game.screen.blit(no_upgrades_text, (
                WIDTH // 2 - no_upgrades_text.get_width() // 2,
                HEIGHT // 2 - no_upgrades_text.get_height() // 2
            ))
        else:
            # Draw available upgrades
            for i, upgrade in enumerate(available_upgrades):
                # Calculate position
                col = i % upgrades_per_row
                row = i // upgrades_per_row
                
                x_pos = 30 + (col * upgrade_width)
                y_pos = 80 + (row * (upgrade_height + 10))
                
                # Upgrade container
                upgrade_rect = pygame.Rect(x_pos, y_pos, upgrade_width - 10, upgrade_height)
                
                # Determine if upgrade is affordable
                affordable = self.game.bufos >= upgrade["cost"]
                color = GREEN if affordable else RED
                
                pygame.draw.rect(self.game.screen, color, upgrade_rect, 2)
                
                # Upgrade name
                name_text = self.font.render(upgrade["name"], True, WHITE)
                self.game.screen.blit(name_text, (upgrade_rect.x + 10, upgrade_rect.y + 5))
                
                # Upgrade description
                desc_text = self.font.render(upgrade["description"], True, GOLD)
                desc_rect = desc_text.get_rect(x=upgrade_rect.x + 10, y=upgrade_rect.y + 30)
                
                # Truncate description if too long
                if desc_rect.width > upgrade_rect.width - 20:
                    desc_text = self.font.render(upgrade["description"][:30] + "...", True, GOLD)
                
                self.game.screen.blit(desc_text, (upgrade_rect.x + 10, upgrade_rect.y + 30))
                
                # Upgrade cost
                cost_text = self.font.render(f"Cost: {self.game.format_number(upgrade['cost'])}", True, WHITE)
                self.game.screen.blit(cost_text, (upgrade_rect.right - cost_text.get_width() - 10, upgrade_rect.y + 5))
        
        # Back button
        self.draw_back_button()
    
    def draw_achievements_menu(self):
        """Draw the achievements menu"""
        # Draw semi-transparent background
        self.draw_semi_transparent_background()
        
        # Draw title
        self.draw_title("Achievements")
        
        # Count unlocked achievements
        unlocked = sum(1 for a in self.game.achievements if a["earned"])
        total = len(self.game.achievements)
        progress_text = self.font.render(f"Progress: {unlocked}/{total}", True, GOLD)
        self.game.screen.blit(progress_text, (WIDTH // 2 - progress_text.get_width() // 2, 60))
        
        # Draw achievements list
        y_pos = 100
        achievement_height = 50
        
        for achievement in self.game.achievements:
            # Achievement container
            achievement_rect = pygame.Rect(WIDTH // 2 - 300, y_pos, 600, achievement_height)
            
            color = GOLD if achievement["earned"] else (100, 100, 100)
            pygame.draw.rect(self.game.screen, color, achievement_rect, 2)
            
            # Achievement name
            name_text = self.font.render(achievement["name"], True, WHITE if achievement["earned"] else (150, 150, 150))
            self.game.screen.blit(name_text, (achievement_rect.x + 10, achievement_rect.y + 5))
            
            # Achievement description
            desc_text = self.font.render(achievement["description"], True, color)
            self.game.screen.blit(desc_text, (achievement_rect.x + 10, achievement_rect.y + 25))
            
            y_pos += achievement_height + 10
        
        # Back button
        self.draw_back_button()
    
    def draw_stats_menu(self):
        """Draw the stats menu"""
        # Draw semi-transparent background
        self.draw_semi_transparent_background()
        
        # Draw title
        self.draw_title("Statistics")
        
        # Draw stats
        y_pos = 80
        line_height = 30
        
        # Define all stats to display
        stats_to_display = [
            ("Total bufos earned", self.game.format_number(self.game.total_bufos_earned)),
            ("Total clicks", str(self.game.stats['clicks'])),
            ("Buildings purchased", str(self.game.stats['buildings_purchased'])),
            ("Upgrades purchased", str(self.game.stats['upgrades_purchased'])),
            (f"Play time", f"{self.game.stats['play_time'] // 60} minutes, {self.game.stats['play_time'] % 60} seconds"),
            ("Game started", self.game.stats['game_started']),
            ("Current production", f"{self.game.format_number(self.game.bufos_per_second)} bufos per second"),
            ("Click power", str(self.game.click_power))
        ]
        
        # Add golden bufos stat if available
        if "golden_bufos_clicked" in self.game.stats:
            stats_to_display.append(("Golden bufos caught", str(self.game.stats['golden_bufos_clicked'])))
        
        # Draw each stat line
        for label, value in stats_to_display:
            stat_text = self.font.render(f"{label}: {value}", True, WHITE)
            self.game.screen.blit(stat_text, (WIDTH // 2 - 200, y_pos))
            y_pos += line_height
        
        # Back button
        self.draw_back_button()
    
    def draw_theme_selector(self):
        """Draw the theme selection menu"""
        # Draw semi-transparent background
        self.draw_semi_transparent_background()
        
        # Draw title
        self.draw_title("Select Theme")
        
        # Draw theme options
        y_pos = 80
        theme_height = 100
        
        for theme_name in THEMES:
            # Theme container
            theme_rect = pygame.Rect(WIDTH // 2 - 200, y_pos, 400, theme_height)
            
            color = GOLD if theme_name == self.game.current_theme else WHITE
            pygame.draw.rect(self.game.screen, color, theme_rect, 2)
            
            # Theme preview (small thumbnail of background)
            preview_rect = pygame.Rect(theme_rect.x + 10, theme_rect.y + 10, 80, 80)
            preview_img = pygame.transform.scale(self.game.background_imgs[theme_name], (80, 80))
            self.game.screen.blit(preview_img, preview_rect)
            
            # Theme name
            name_text = self.font.render(theme_name.title(), True, color)
            self.game.screen.blit(name_text, (theme_rect.x + 100, theme_rect.y + theme_height // 2 - name_text.get_height() // 2))
            
            y_pos += theme_height + 10
        
        # Back button
        self.draw_back_button()
    
    def draw_cheat_box(self):
        """Draw the cheat code input box"""
        # Draw input box
        input_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 40)
        pygame.draw.rect(self.game.screen, WHITE, input_rect)
        
        # Draw input text
        cheat_text = self.font.render(self.game.cheat_input, True, BLACK)
        self.game.screen.blit(cheat_text, (input_rect.x + 10, input_rect.y + 10))
        
        # Draw blinking cursor
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_rect.x + 10 + cheat_text.get_width()
            pygame.draw.line(self.game.screen, BLACK, (cursor_x, input_rect.y + 5), (cursor_x, input_rect.y + 35), 2)
        
        # Draw label
        label_text = self.font.render("Enter Cheat Code:", True, GOLD)
        self.game.screen.blit(label_text, (WIDTH // 2 - label_text.get_width() // 2, input_rect.y - 30))
        
        # Draw submit button
        submit_button = self.create_button(
            WIDTH // 2 - 50,
            input_rect.bottom + 20,
            100,
            40,
            GREEN,
            "Submit"
        )
        
        # Draw cancel button
        cancel_button = self.create_button(
            WIDTH // 2 - 50,
            submit_button.bottom + 20,
            100,
            40,
            RED,
            "Cancel"
        )
        
        return submit_button, cancel_button
    
    def draw_floating_texts(self):
        """Draw all floating text effects"""
        current_time = pygame.time.get_ticks()
        for text in self.game.floating_text_manager.floating_texts:
            elapsed = (current_time - text["creation_time"]) / 1000.0
            alpha = 255 * (1 - (elapsed / text["lifetime"]))
            
            font = pygame.font.SysFont("Arial", text["size"])
            text_surface = font.render(text["text"], True, text["color"])
            
            # Apply fading
            text_surface.set_alpha(int(alpha))
            
            self.game.screen.blit(text_surface, text["position"])