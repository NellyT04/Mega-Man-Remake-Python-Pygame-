import pygame

class InvisibleWall(pygame.sprite.Sprite):
    # Invisible barrier to block player movement
    def __init__(self, x, y, width, height):
        super().__init__()
        
        # Create invisible surface
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(0)
        
        # Set position and collision box
        self.rect = self.image.get_rect(topleft=(x, y))