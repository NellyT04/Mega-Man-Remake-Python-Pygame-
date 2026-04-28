import pygame
from settings import *

class ScrollingBackground:
    def __init__(self, width, height, image_path=None):
        # Load and scale the background image to fit screen size
        loaded_image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(loaded_image, (width, height))
            
        self.width = width  

    def draw(self, surface, scroll_x,):
        # Calculate relative position based on scroll amount
        rel_x = scroll_x % self.width
        # Draw three copies of the background 
        surface.blit(self.image, (rel_x - self.width, 0)) 
        surface.blit(self.image, (rel_x, 0))               
        surface.blit(self.image, (rel_x + self.width, 0))  

 