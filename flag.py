import pygame
from settings import *

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None, width=40, height=110):
        super().__init__()
        
        # Load flag image
        self.image = pygame.image.load('IMG/flag/flag.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
      
        # Set collision area
        self.rect = self.image.get_rect(topleft=(x, y))
        
       