import pygame
from settings import *

class Camera:
    # Handles camera movement and position tracking
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0.1  
        
    def update(self, target_sprite, platforms):
        # Update camera position to follow target 
        # Calculate target camera position
        target_x = target_sprite.rect.centerx - SCREEN_WIDTH // 2
        target_y = target_sprite.rect.centery - SCREEN_HEIGHT // 2
        
        # Apply camera bounds
        target_x = max(0, target_x)
        target_y = max(-200, target_y)
        target_y = min(400, target_y)  # So it doesn't scroll too far down
        
        # Smooth camera movement
        self.x += (target_x - self.x) * self.speed
        self.y += (target_y - self.y) * self.speed
    
    def get_scroll_offset(self):
        # Get background scroll offset for the parallax effect
        return -self.x * 0.3
    
    def world_to_screen(self, world_pos):
        return (world_pos[0] - self.x, world_pos[1] - self.y)

    def is_visible(self, sprite, margin=600):
        # Check if sprite is visible on screen 
        screen_x = sprite.rect.x - self.x
        screen_y = sprite.rect.y - self.y
        
        return (-margin < screen_x < SCREEN_WIDTH + margin and 
                -margin < screen_y < SCREEN_HEIGHT + margin)