import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    # Base class for all collectible items
    def __init__(self, x, y, item_type, image_path=None, width=30, height=30):
        super().__init__()
        self.item_type = item_type
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        # Position and collision
        self.rect = self.image.get_rect(center=(x, y))
        
class RapidFireItem(Item):
    # Power-up that allows rapid shooting 
    def __init__(self, x, y, image_path):
        super().__init__(x, y, "rapid_fire", image_path)
        self.duration = 3000 

class TripleShotItem(Item):
    # Power-up that shoots 3 bullets at once
    def __init__(self, x, y, image_path):
        super().__init__(x, y, "triple_shot", image_path)
        self.duration = 3000 

class MedKitItem(Item):
    # Health restoration item
    def __init__(self, x, y, image_path):
        super().__init__(x, y, "med_kit", image_path)
        self.heal_amount = 1

class PowerUpManager:
    # Manages active power-ups for the player
    def __init__(self):
        self.active_powerups = {}
        
    def activate_powerup(self, powerup_type, duration):
        # Activate a power-up with a timer
        self.active_powerups[powerup_type] = {'start_time': pygame.time.get_ticks(),'duration': duration }
    
    def is_active(self, powerup_type):
        # Check if a power-up is currently active
        if powerup_type not in self.active_powerups:
            return False
        
        current_time = pygame.time.get_ticks()
        powerup = self.active_powerups[powerup_type]
        elapsed = current_time - powerup['start_time']
        
        if elapsed >= powerup['duration']:
            del self.active_powerups[powerup_type]
            return False
        
        return True
    
    def get_remaining_time(self, powerup_type):
        # Get remaining time for a power-up in seconds
        if powerup_type not in self.active_powerups:
            return 0
        
        current_time = pygame.time.get_ticks()
        powerup = self.active_powerups[powerup_type]
        elapsed = current_time - powerup['start_time']
        remaining = powerup['duration'] - elapsed
        
        return max(0, remaining / 1000)  
    
    def clear_all(self):
        # Clear all active power-ups
        self.active_powerups.clear()

def draw_powerup_icons(screen, powerup_manager):
    # Draw active power-up icons and timers on screen
    icon_size = 30
    icon_spacing = 40
    start_x = SCREEN_WIDTH - 50
    start_y = 20
    
    y_offset = 0
    
    # Rapid Fire icon
    if powerup_manager.is_active("rapid_fire"):
        # Draw icon background
        icon_rect = pygame.Rect(start_x - icon_size, start_y + y_offset, icon_size, icon_size)
        pygame.draw.rect(screen, (255, 165, 0), icon_rect)
        pygame.draw.rect(screen, colors["white"], icon_rect, 2)
        
        # Draw "RF" text
        font = pygame.font.Font(None, 20)
        text = font.render("RF", True, colors["white"])
        text_rect = text.get_rect(center=icon_rect.center)
        screen.blit(text, text_rect)
        
        # Draw timer
        remaining = powerup_manager.get_remaining_time("rapid_fire")
        timer_text = font.render(f"{remaining:.1f}s", True, (255, 165, 0))
        screen.blit(timer_text, (start_x - icon_size - 45, start_y + y_offset + 8))
        
        y_offset += icon_spacing
    
    # Triple Shot icon
    if powerup_manager.is_active("triple_shot"):
        # Draw icon background
        icon_rect = pygame.Rect(start_x - icon_size, start_y + y_offset, icon_size, icon_size)
        pygame.draw.rect(screen, (0, 255, 255), icon_rect)
        pygame.draw.rect(screen, colors["white"], icon_rect, 2)
        
        # Draw "x3" text
        font = pygame.font.Font(None, 20)
        text = font.render("x3", True, colors["white"])
        text_rect = text.get_rect(center=icon_rect.center)
        screen.blit(text, text_rect)
        
        # Draw timer
        remaining = powerup_manager.get_remaining_time("triple_shot")
        timer_text = font.render(f"{remaining:.1f}s", True, (0, 255, 255))
        screen.blit(timer_text, (start_x - icon_size - 45, start_y + y_offset + 8))
        
        y_offset += icon_spacing