import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20):
        super().__init__()
        
        # Load and scale platform image
        self.image = pygame.image.load('IMG/Platform/Platform_lava.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        # Set position and collision box
        self.rect = self.image.get_rect(topleft=(x, y))