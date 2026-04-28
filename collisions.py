import pygame
class CollisionHandler:
    #Handles all collision detection and response in the game
    def __init__(self):
        self.hit_positions = []  
    
    def check_item_collection(self, player, items):
        collected_items = pygame.sprite.spritecollide(player, items, False)
        for item in collected_items:
            if player.collect_item(item):
                item.kill()
        return len(collected_items) > 0

    def check_bullet_enemy_collision(self, bullets, enemies):
        score = 0
        for bullet in list(bullets):
            hits = pygame.sprite.spritecollide(bullet, enemies, False)
            if hits:
                bullet.kill()
                for enemy in hits:
                    # Add hit position for visual effect
                    self.hit_positions.append([enemy.rect.centerx, enemy.rect.centery, 20])
                    if enemy.take_damage():
                        score += 100
        return score
    
    def check_bullet_boss_collision(self, bullets, boss,boss_spawned):
        if not boss or not boss.alive() or not boss_spawned:
            return 0
        
        score = 0
        for bullet in list(bullets):
            if pygame.sprite.collide_rect(boss, bullet):
                bullet.kill()
                # Add hit position for visual feedback
                self.hit_positions.append([boss.rect.centerx, boss.rect.centery, 15])
                if boss.take_damage():
                    score += 1000  # Bonus for defeating boss
                else:
                    score += 10  # Points for damaging boss
        return score
    
    def check_enemy_bullet_player_collision(self, player, enemy_bullets):
        if player.invulnerable:
            return 0
        
        hit_bullets = pygame.sprite.spritecollide(player, enemy_bullets, True)
        # Return 1 damage per bullet hit
        return len(hit_bullets)

    def check_enemy_player_collision(self, player, enemies):
        if player.invulnerable:
            return 0
        
        hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
        # Return 1 damage per enemy hit
        return len(hit_enemies)

    def check_boss_player_collision(self, player, boss):
        if player.invulnerable or not boss or not boss.alive():
            return 0
        # Boss deals 2 damage on contact!
        return 2 if pygame.sprite.collide_rect(player, boss) else 0

    def check_flag_collision(self, player, flag):
        return player.rect.colliderect(flag.rect)
    
    def check_fall_death(self, player, platforms):
        if not platforms:
            return False
        
        lowest_platform_y = max([platform.rect.bottom for platform in platforms])
        fall_threshold = lowest_platform_y + 300
        
        return player.rect.y > fall_threshold
    
    def update_hit_effects(self):
        self.hit_positions = [[x, y, t-1] for x, y, t in self.hit_positions if t > 1]
    
    def draw_hit_effects(self, screen, camera_x, camera_y):
        for x, y, timer in self.hit_positions:
            # Convert world coordinates to screen coordinates
            screen_x = int(x - camera_x)
            screen_y = int(y - camera_y)
            
            # Calculate visual properties based on timer
            size = int(timer * 1.5)  
            alpha = int(255 * (timer / 20))  
            
            # Create color with fade effect
            color = (255, 255, 100) 
            
            # Draw expanding circle
            if size > 0:
                pygame.draw.circle(screen, color, (screen_x, screen_y), size, 2)
                
                # Draw inner circle for more impact
                if size > 5:
                    inner_size = max(1, size - 3)
                    pygame.draw.circle(screen, color, (screen_x, screen_y), inner_size, 1)