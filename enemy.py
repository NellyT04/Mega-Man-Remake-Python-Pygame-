import pygame
from bullet import *
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=100, speed=2, image_path=None, difficulty_level=1):
        super().__init__()
        
        # Load and scale enemy image
        self.original_image = pygame.image.load('IMG/enemy/enemy1.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (120, 120))
        
        # Set current image
        self.image = self.original_image.copy()

        # Position and collision detection
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Health
        self.health = 5     
        self.max_health = 5  
        
        # movement 
        self.speed = speed           
        self.direction = 1          
        self.start_x = x            
        self.patrol_range = patrol_range

        # get progressively difficult 
        self.difficulty_level = difficulty_level
        self.apply_difficulty_scaling() 
        
        self.pause_at_edge = False
        self.pause_timer = 0
        self.pause_duration = 30  # frames to pause at edges
        
        # Death animation
        self.is_dying = False
        self.death_timer = 0
        self.death_duration = 20
        
        # Hit flash effect
        self.hit_flash_timer = 0
    
    def apply_difficulty_scaling(self):
        if self.difficulty_level <= 2:
            # easy 
            self.shoot_interval = 1500
            self.sight_range = 200
            self.bullet_speed = 6
        elif self.difficulty_level <= 5:
            # medium 
            self.shoot_interval = 1000
            self.sight_range = 250
            self.bullet_speed = 8
        else:
            # hard 
            self.shoot_interval = 800
            self.sight_range = 300
            self.bullet_speed = 10
        
        # Initialize timing
        self.last_shot = pygame.time.get_ticks()
    
    def update_sprite_direction(self):
        # flip image
        if self.direction == 1: 
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:  
            self.image = self.original_image.copy()
        
        # Death animation 
        if self.is_dying:
            alpha = int(255 * (1 - self.death_timer / self.death_duration))
            self.image.set_alpha(alpha)
        
        # Hit flash effect
        if self.hit_flash_timer > 0:
            self.image.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
    
    def has_line_of_sight(self, player, platforms):
        # Get start and end points
        start_x = self.rect.centerx
        start_y = self.rect.centery
        end_x = player.rect.centerx
        end_y = player.rect.centery
        
        # Calculate distance
        dx = end_x - start_x
        dy = end_y - start_y
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance == 0:
            return True
        
        # Number of points to check along the line
        steps = int(distance / 10)  
        if steps < 2:
            steps = 2
        
        # Check each point along the line
        for i in range(1, steps):
            t = i / steps
            check_x = start_x + dx * t
            check_y = start_y + dy * t
            
            # Create a small rect at this point to check collision
            check_rect = pygame.Rect(check_x - 2, check_y - 2, 4, 4)
            
            # Check if this point intersects any platform
            for platform in platforms:
                if check_rect.colliderect(platform.rect):
                    return False 
        
        return True  
        
    def can_see_player(self, player, platforms=None):   
        # Get horizontal distance
        horizontal_distance = player.rect.centerx - self.rect.centerx
        
        # Get vertical distance
        vertical_distance = player.rect.centery - self.rect.centery
        
        # Calculate total distance
        distance_squared = (horizontal_distance * horizontal_distance) + (vertical_distance * vertical_distance)
        range_squared = self.sight_range * self.sight_range
        
        # Check if player is too far
        if distance_squared > range_squared:
            return False
        
        # Check if player is in front based on direction
        if self.direction == 1: 
            if horizontal_distance < 20:
                return False
        else:  
            if horizontal_distance > -20:
                return False
        
        # Vertical checking 
        if self.difficulty_level <= 2:
            vertical_limit = 120
        elif self.difficulty_level <= 5:
            vertical_limit = 150
        else:
            vertical_limit = 180
            
        if vertical_distance > vertical_limit or vertical_distance < -vertical_limit:
            return False
        
        # Check line of sight
        if platforms and not self.has_line_of_sight(player, platforms):
            return False
            
        return True

    def update(self, platforms=None, bullet_group=None, current_time=None, player=None):
        # Update hit flash timer
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
        
        # Handle death animation
        if self.is_dying:
            self.death_timer += 1
            self.update_sprite_direction()
            if self.death_timer >= self.death_duration:
                self.kill()
            return
        
        # Handle pause at edges (for harder enemies)
        if self.pause_at_edge:
            self.pause_timer += 1
            if self.pause_timer >= self.pause_duration:
                self.pause_at_edge = False
                self.pause_timer = 0
            else:
                # Still shoot while paused if can see player
                if bullet_group is not None and current_time is not None and player is not None:
                    time_passed = current_time - self.last_shot
                    if time_passed >= self.shoot_interval:
                        if self.can_see_player(player, platforms):
                            self.shoot(bullet_group, current_time)
                return
        
        # Store old direction to check if it changed
        old_direction = self.direction
        
        # Move left or right
        self.rect.x = self.rect.x + (self.speed * self.direction)
        
        # Check if reached edge of patrol area
        distance_from_start = self.rect.x - self.start_x
        
        # Turn around if too far from start position
        if distance_from_start < -self.patrol_range:
            self.direction = 1
            # Pause at edge for harder enemies (more tactical)
            if self.difficulty_level >= 6:
                self.pause_at_edge = True
        elif distance_from_start > self.patrol_range:
            self.direction = -1
            # Pause at edge for harder enemies (more tactical)
            if self.difficulty_level >= 6:
                self.pause_at_edge = True
        
        # Update sprite if direction changed
        if old_direction != self.direction:
            self.update_sprite_direction()

        # Shoot at player if can see them
        if bullet_group is not None and current_time is not None and player is not None:
            time_passed = current_time - self.last_shot
            
            if time_passed >= self.shoot_interval:
                if self.can_see_player(player, platforms):
                    self.shoot(bullet_group, current_time)

    def shoot(self, bullet_group, current_time):
        bullet = EnemyBullet(self.rect.centerx, self.rect.centery, self.direction, speed=self.bullet_speed)
        bullet_group.add(bullet)  
        self.last_shot = current_time

    def take_damage(self, amount=1):
        self.health = self.health - amount
        
        # Trigger hit flash effect
        self.hit_flash_timer = 5
        
        if self.health <= 0:
            # Start death animation instead of instant kill
            self.is_dying = True
            return True  
        return False