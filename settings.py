import pygame
pygame.font.init()  

# screen
SCREEN_WIDTH = 800   
SCREEN_HEIGHT = 600  
FPS = 60            

# colours 
colors = {
    "black": (0, 0, 0),        
    "white": (255, 255, 255),   
    "red": (255, 0, 0),        
    "green": (0, 255, 0),      
    "blue": (0, 0, 255),       
    "yellow": (255, 255, 0),   
    "darkblue": (0, 0, 100),
    "purple": (138, 43, 226)
}

# font
FONT = pygame.font.SysFont("Arial", 24)  
