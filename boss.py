import pygame
from settings import *
from bullet import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load and scale boss image to reasonable size
        self.original_image = pygame.image.load("IMG/enemy/boss2.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (150, 150))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.max_health = 100
        self.speed = 2
        self.damage = 10
        self.attack_timer = 0
        self.hit_timer = 0  
        self.is_hit = False
        self.last_attack_time = 0
        
        # Facing direction: -1 = right, 1 = left
        self.facing = -1
        
        # Shooting mechanics
        self.shoot_interval = 1500  # Shoot every 1.5 seconds
        self.last_shot_time = 0
        self.bullet_speed = 8
        
        # Physics for platform collision
        self.vel_y = 0
        self.gravity = 0.8
        self.on_ground = False

# direction facing
    def update_sprite_direction(self):
        if self.facing == -1:  # Facing right
            self.image = self.original_image.copy()
        else:  # Facing left
            self.image = pygame.transform.flip(self.original_image, True, False)

    def update(self, platforms, bullet_group, current_time, player):
        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Boss movement towards player (only horizontal now)
        self.move_towards_player(player)
        
        # Apply vertical movement and check platform collisions
        self.rect.y += self.vel_y
        self._collide_vertical(platforms)

        # Shoot at player
        time_since_shot = current_time - self.last_shot_time
        if time_since_shot >= self.shoot_interval:
            self.shoot(bullet_group, current_time)

        # Handle melee attacks (when very close)
        time_since_attack = current_time - self.last_attack_time
        if time_since_attack >= 2000:  # Attack every 2 seconds
            self.attack(player)
            self.last_attack_time = current_time    

        # Handle hit feedback
        if self.is_hit:
            elapsed = current_time - self.hit_timer
            if elapsed >= 200:
                self.is_hit = False

# movement towards player
    def move_towards_player(self, player):
        old_facing = self.facing
        
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
            self.facing = 1  # Face right
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed
            self.facing = -1  # Face left
        
        # Update sprite if facing changed
        if old_facing != self.facing:
            self.update_sprite_direction()

# boss shooting
    def shoot(self, bullet_group, current_time):
        bullet = BossBullet(self.rect.centerx, self.rect.centery, self.facing, speed=self.bullet_speed)
        bullet_group.add(bullet)
        self.last_shot_time = current_time

# melee attack
    def attack(self, player):
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)
    
    def _collide_vertical(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Moving up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

# damage
    def take_damage(self, amount=10):
        self.health -= amount
        self.is_hit = True
        self.hit_timer = pygame.time.get_ticks()  
        if self.health <= 0:
            self.die()
            return True  # Return True when boss dies
        return False

# boss death
    def die(self):
        print("Boss defeated!")
        self.kill()  # Remove boss from sprite groups

# health bar
    def draw_health_bar(self, screen, fixed_position=False):
        bar_width = 200
        bar_height = 20
        health_ratio = max(0, self.health / self.max_health)
        
        if fixed_position:
            # Draw at top of screen
            bar_x = (screen.get_width() - bar_width) // 2
            bar_y = 20
        else:
            # Draw above boss sprite
            bar_x = self.rect.x
            bar_y = self.rect.y - 30
        
        # Background 
        pygame.draw.rect(screen, colors["red"], (bar_x, bar_y, bar_width, bar_height))
        # Health
        pygame.draw.rect(screen, colors["green"], (bar_x, bar_y, bar_width * health_ratio, bar_height))
        # Border
        pygame.draw.rect(screen, colors["white"], (bar_x, bar_y, bar_width, bar_height), 2)

# Draw boss
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)
        if self.is_hit:
            # Flash effect when hit
            pygame.draw.rect(screen, colors["white"], self.rect, 3)