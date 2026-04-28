import pygame
from bullet import *
from settings import *
from items import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Load all animation frames
        self.animations = {
            'idle': [
                pygame.transform.scale(pygame.image.load('IMG/X/X.PNG').convert_alpha(), (80, 80)),
            ],
            'run': [
                pygame.transform.scale(pygame.image.load('IMG/X/RunX.png').convert_alpha(), (80, 80)),
                pygame.transform.scale(pygame.image.load('IMG/X/Run2X.png').convert_alpha(), (80, 80)),
            ],
            'jump': [
                pygame.transform.scale(pygame.image.load('IMG/X/start jump X.png').convert_alpha(), (80, 80)), 
                pygame.transform.scale(pygame.image.load('IMG/X/jump X.png').convert_alpha(), (80, 80)),  
                pygame.transform.scale(pygame.image.load('IMG/X/Air X.png').convert_alpha(), (80, 80)),   
            ],
        }
        # Animation state tracking
        self.anim_state = 'idle'
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_speed = 120  

        self.original_image = self.animations['idle'][0]
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = 15
        self.gravity = 0.8
        self.on_ground = False
        self.facing = 1

        # Health
        self.health = 8
        self.max_health = 8

        # Invincibility frames
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 800

        # Shooting cooldown
        self.last_shot_time = 0
        self.shoot_cooldown = 300
        self.normal_cooldown = 300
        self.rapid_fire_cooldown = 100

        # Dash ability
        self.dash_speed = 15
        self.dash_duration = 200
        self.dash_cooldown = 700
        self.is_dashing = False
        self.dash_start_time = 0
        self.last_dash_time = 0
        self.dash_direction = 0

        # Dash invulnerability
        self.dash_invulnerable = True

        # Power-up manager
        self.powerup_manager = PowerUpManager()

    def update_sprite_direction(self):
        current_time = pygame.time.get_ticks()

        # animation state  
        if not self.on_ground:
            new_state = 'jump'
        elif self.vel_x != 0:
            new_state = 'run'
        else:
            new_state = 'idle'

        # rest state if changed
        if new_state != self.anim_state:
            self.anim_state = new_state
            self.anim_frame = 0
            self.anim_timer = current_time

        frames = self.animations[self.anim_state]

        if self.anim_state == 'run':
            if current_time - self.anim_timer >= self.anim_speed:
                self.anim_frame = (self.anim_frame + 1) % len(frames)
                self.anim_timer = current_time

    #Jumping animation
        elif self.anim_state == 'jump':
            if self.vel_y < -5:
                self.anim_frame = 0   
            elif self.vel_y < 2:
                self.anim_frame = 1  
            else:
                self.anim_frame = 2   

        else:
            # Idle 
            self.anim_frame = 0

        # flip animation dpending on direction
        frame = frames[self.anim_frame]
        if self.facing == -1:
            self.image = pygame.transform.flip(frame, True, False)
        else:
            self.image = frame.copy()

        # Semi-transparent during dash
        if self.is_dashing:
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(255)

    def update(self, platforms, keys):
        current_time = pygame.time.get_ticks()

        self.update_invulnerability()

        # Update shooting cooldown based on rapid fire status
        if self.powerup_manager.is_active("rapid_fire"):
            self.shoot_cooldown = self.rapid_fire_cooldown
        else:
            self.shoot_cooldown = self.normal_cooldown

        # Handle dash movement
        if self.is_dashing:
            dash_elapsed = current_time - self.dash_start_time
            if dash_elapsed >= self.dash_duration:
                self.is_dashing = False
                self.update_sprite_direction()
            else:
                old_x = self.rect.x

                self.rect.x += self.dash_speed * self.dash_direction
                self._collide_horizontal(platforms)

                # Stop dashing if we hit a wall
                if self.rect.x == old_x:
                    self.is_dashing = False
                    self.update_sprite_direction()

                self.vel_y += self.gravity * 0.3
                if self.vel_y > 15:
                    self.vel_y = 15
                self.rect.y += self.vel_y
                self._collide_vertical(platforms)
                return

        # Horizontal movement
        self.vel_x = 0

        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing = -1
        if keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing = 1

        # Update animation
        self.update_sprite_direction()

        # Gravity
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15

        # Horizontal collision
        self.rect.x += self.vel_x
        self._collide_horizontal(platforms)

        # Vertical collision
        self.rect.y += self.vel_y
        self._collide_vertical(platforms)

    def dash(self):
        current_time = pygame.time.get_ticks()

        if not self.is_dashing and current_time - self.last_dash_time >= self.dash_cooldown:
            self.is_dashing = True
            self.dash_start_time = current_time
            self.last_dash_time = current_time
            self.dash_direction = self.facing

            if self.dash_invulnerable:
                self.invulnerable = True
                self.invulnerable_time = current_time
            return True
        return False

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

    def _collide_horizontal(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0 or (self.is_dashing and self.dash_direction > 0):
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0 or (self.is_dashing and self.dash_direction < 0):
                    self.rect.left = platform.rect.right

    def _collide_vertical(self, platforms):
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def shoot(self, bullet_group):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_cooldown:
            bullet_x = self.rect.centerx + (self.facing * 20)
            bullet_y = self.rect.centery

            if self.powerup_manager.is_active("triple_shot"):
                bullet_group.add(Bullet(bullet_x, bullet_y, self.facing))
                bullet_group.add(Bullet(bullet_x, bullet_y - 15, self.facing))
                bullet_group.add(Bullet(bullet_x, bullet_y + 15, self.facing))
            else:
                bullet_group.add(Bullet(bullet_x, bullet_y, self.facing))

            self.last_shot_time = current_time

    def update_invulnerability(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time > self.invulnerable_duration:
                self.invulnerable = False

    def take_damage(self, amount=1):
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
        return self.health <= 0

    def heal(self, amount=1):
        if self.health < self.max_health:
            self.health = min(self.health + amount, self.max_health)
            return True
        return False

    def collect_item(self, item):
        if item.item_type == "rapid_fire":
            self.powerup_manager.activate_powerup("rapid_fire", item.duration)
            return True
        elif item.item_type == "triple_shot":
            self.powerup_manager.activate_powerup("triple_shot", item.duration)
            return True
        elif item.item_type == "med_kit":
            return self.heal(item.heal_amount)
        return False

    def get_dash_cooldown_percent(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_dash_time
        if elapsed >= self.dash_cooldown:
            return 1.0
        return elapsed / self.dash_cooldown
    