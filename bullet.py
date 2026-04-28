import pygame
from settings import * 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=10, color=None, size=(10,5)):
        super().__init__()
        
        self.image = pygame.Surface(size)  
        self.image.fill(colors["yellow"]) 
        self.rect = self.image.get_rect(center=(x, y))
        
        # direction: 1 = right, -1 = left
        self.vx = speed * direction
        
        self.spawn_x = x
        self.max_distance = 1000

    def update(self, *args):
        self.rect.x += self.vx
        
        distance_traveled = abs(self.rect.x - self.spawn_x)
        if distance_traveled > self.max_distance:
            self.kill()
        elif self.rect.right < -200 or self.rect.left > 4000:
            self.kill()

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction, speed=6):
        super().__init__(x, y, direction, speed, color=colors["red"], size=(8,4))
        self.max_distance = 800
        
    def update(self):
        self.rect.x += self.vx

        if abs(self.rect.x - self.spawn_x) > self.max_distance:
            self.kill()
        elif (self.rect.right < -200 or self.rect.left > 4000 or 
              self.rect.top > 800 or self.rect.bottom < -100):
            self.kill()

class BossBullet(Bullet):
    def __init__(self, x, y, direction, speed=8):
        super().__init__(x, y, direction, speed, color=colors["purple"], size=(12, 6))
        self.max_distance = 900
        
    def update(self, *args):
        self.rect.x += self.vx

        if abs(self.rect.x - self.spawn_x) > self.max_distance:
            self.kill()
        elif (self.rect.right < -200 or self.rect.left > 4000 or 
              self.rect.top > 800 or self.rect.bottom < -100):
            self.kill()

class AngledEnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=6, angle=0):
        super().__init__()
        
        self.image = pygame.Surface((8, 4))
        self.image.fill(colors["red"])
        self.rect = self.image.get_rect(center=(x, y))

        self.vx = speed * direction
        self.vy = speed * angle   # angle as a vertical multiplier (-1 to 1)
        
        self.spawn_x = x
        self.spawn_y = y
        self.max_distance = 800
        self.lifetime = 0
        self.max_lifetime = 200

    def update(self, *args):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.lifetime += 1

        dist_x = self.rect.x - self.spawn_x
        dist_y = self.rect.y - self.spawn_y
        distance_traveled = (dist_x**2 + dist_y**2) ** 0.5

        if (distance_traveled > self.max_distance or
            self.lifetime > self.max_lifetime or
            self.rect.right < -200 or self.rect.left > 4000 or 
            self.rect.top > 800 or self.rect.bottom < -100):
            self.kill()
        
        