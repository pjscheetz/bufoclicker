import pygame
import os
from src.constants import SOUNDS_PATH, THEMES

class AudioManager:
    """Manages all game audio including sound effects and music"""
    
    def __init__(self):
        pygame.mixer.init()
        
        # Initialize sound dictionaries
        self.click_sounds = {}
        self.music_tracks = {}
        
        # Load all audio assets
        self.load_audio_assets()
    
    def load_audio_assets(self):
        """Load all sound effects and music tracks"""
        try:
            # Load click sounds for each theme
            for theme in THEMES:
                try:
                    self.click_sounds[theme] = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, THEMES[theme]["click_sound"]))
                except:
                    # Create a dummy sound if missing
                    default_click_path = os.path.join(SOUNDS_PATH, "default_click.wav")
                    if os.path.exists(default_click_path):
                        self.click_sounds[theme] = pygame.mixer.Sound(default_click_path)
                    else:
                        # If even the default is missing, create a silent sound
                        self.click_sounds[theme] = None
                
                # Store music track paths
                self.music_tracks[theme] = os.path.join(SOUNDS_PATH, THEMES[theme]["music"])
            
            # Load other sound effects
            achievement_path = os.path.join(SOUNDS_PATH, "achievement.wav")
            upgrade_path = os.path.join(SOUNDS_PATH, "upgrade.wav")
            boost_path = os.path.join(SOUNDS_PATH, "boost.wav")
            
            self.achievement_sound = pygame.mixer.Sound(achievement_path) if os.path.exists(achievement_path) else None
            self.upgrade_sound = pygame.mixer.Sound(upgrade_path) if os.path.exists(upgrade_path) else None
            self.boost_sound = pygame.mixer.Sound(boost_path) if os.path.exists(boost_path) else None
            
        except Exception as e:
            print(f"Error loading audio assets: {e}")
            # Set up fallbacks
            self.click_sounds = {theme: None for theme in THEMES}
            self.music_tracks = {theme: None for theme in THEMES}
            self.achievement_sound = None
            self.upgrade_sound = None
            self.boost_sound = None
    
    def play_theme_music(self, theme):
        """Play background music for the specified theme"""
        try:
            if theme in self.music_tracks:
                music_path = self.music_tracks[theme]
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Error playing theme music: {e}")
    
    def play_sound(self, sound):
        """Play a sound effect if it exists"""
        if sound is not None:
            try:
                sound.play()
            except Exception as e:
                print(f"Error playing sound: {e}")
    
    def play_click_sound(self, theme):
        """Play the click sound for the specified theme"""
        self.play_sound(self.click_sounds.get(theme))
    
    def play_achievement_sound(self):
        """Play the achievement unlocked sound"""
        self.play_sound(self.achievement_sound)
    
    def play_upgrade_sound(self):
        """Play the upgrade purchased sound"""
        self.play_sound(self.upgrade_sound)
    
    def play_boost_sound(self):
        """Play the boost activated sound"""
        self.play_sound(self.boost_sound)