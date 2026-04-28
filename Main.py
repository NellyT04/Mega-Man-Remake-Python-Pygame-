import pygame
import sys
from background import *
from levels import *
from player import *
from settings import *
from ui import *
from camera import *
from collisions import *
from game_drawings import *
from game_states import *
from wall import *
from music import *

class Game:
    # Main game class 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Project X")
        self.clock = pygame.time.Clock()

        # Game state
        self.state = "MENU"
        self.current_level = 1  
        self.score = 0

        # Stats tracking
        self.start_time = None
        self.total_enemies_defeated = 0
        self.total_levels_completed = 0

        # Initialize game
        self.camera = Camera()
        self.background = ScrollingBackground(SCREEN_WIDTH, SCREEN_HEIGHT,image_path="IMG/Background/Background.png")
        self.menu_manager = Menu()
        self.renderer = GameRenderer(self.screen, self.background)
        self.state_handler = GameStateHandler(self)
        self.collision_handler = CollisionHandler()

        # Boss system
        self.boss = None
        self.boss_spawned = False
        self.boss_trigger_x = 2800
        self.barrier = None
        
        # Initialize level 
        self.reset_level()

    def get_time_played(self):
        if self.start_time:
            current_time = pygame.time.get_ticks()
            return (current_time - self.start_time) // 1000  # Convert to seconds
        return 0

    def reset_level(self, preserve_health=False):
        #Reset level with option to preserve player health
        current_health = getattr(self, 'player', None) and self.player.health or 3  
        
        # Reset stats if starting over from level 1
        if not preserve_health and self.current_level == 1:
            self.total_enemies_defeated = 0
            self.start_time = pygame.time.get_ticks()
            self.total_levels_completed = 0
            
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        # Create player
        self.player = Player(50, 400) 
        if preserve_health:
            self.player.health = current_health
        else:
            self.player.powerup_manager.clear_all()
        self.all_sprites.add(self.player)

        # Reset camera
        self.camera.x = 0
        self.camera.y = 0

        # Load level data
        level_data = load_level(self.current_level)
        platforms, enemies, flag = level_data[:3]
        self.boss = level_data[3] if len(level_data) > 3 else None
        items = level_data[4] if len(level_data) > 4 else []
        
        # Reset boss state
        self.boss_spawned = False
        self.barrier = None
    
        # Add sprites to groups
        for p in platforms:
            self.platforms.add(p)
            self.all_sprites.add(p)
        
        for e in enemies:
            self.enemies.add(e)
            self.all_sprites.add(e)
        
        for item in items:
            self.items.add(item)
            self.all_sprites.add(item)

        self.flag = flag
        self.all_sprites.add(self.flag)
        
    def spawn_boss(self):
        # Spawn boss and create arena barrier
        if self.boss and not self.boss_spawned:
            self.all_sprites.add(self.boss)
            
            self.boss.arena_left = 2850
            self.boss.arena_right = 3750
            self.boss.arena_bounds_set = True
            
            self.barrier = InvisibleWall(self.boss_trigger_x - 50, 0, 50, 600)
            self.platforms.add(self.barrier)
            self.all_sprites.add(self.barrier)
            
            self.boss_spawned = True
            self.state_handler.play_music(Boss_battle)
            
    def handle_events(self):
        # Handle all game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.state_handler.handle_menu_events(event):
                return False
            if not self.state_handler.handle_keyboard_input(event):
                return False
        return True

    def update_gameplay(self):
        # Update gameplay state
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Boss trigger
        if self.current_level == 8 and not self.boss_spawned:
            if self.player.rect.x >= self.boss_trigger_x:
                self.spawn_boss()

        # Update player
        self.player.update(self.platforms.sprites(), keys)
        self.camera.update(self.player, self.platforms.sprites())

        # Item collection
        self.collision_handler.check_item_collection(self.player, self.items)

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.platforms.sprites(), self.enemy_bullets,current_time, self.player)

        # Update boss
        if self.boss_spawned and self.boss and self.boss.alive():
            self.boss.update(self.platforms.sprites(), self.enemy_bullets,current_time, self.player)

        # Add bullets to sprites
        for b in list(self.enemy_bullets):
            if b not in self.all_sprites:
                self.all_sprites.add(b)
        for b in list(self.player_bullets):
            if b not in self.all_sprites:
                self.all_sprites.add(b)

        # Update bullets
        self.player_bullets.update()
        self.enemy_bullets.update()

        # Handle collisions
        self.handle_collisions()

        # Check level completion
        can_complete = not (self.boss and self.boss.alive())
        if can_complete and self.collision_handler.check_flag_collision(self.player, self.flag):
            if self.current_level == 8:
                self.state = "FINAL_VICTORY"
                self.total_levels_completed = 8
                self.state_handler.play_music(between_levels_music)
            else:
                self.state = "LEVEL_COMPLETE"
                self.total_levels_completed = max(self.total_levels_completed, self.current_level)
                self.state_handler.play_music(between_levels_music)

        # Check fall death
        if self.collision_handler.check_fall_death(self.player,self.platforms.sprites()):
            self.state = "GAME_OVER"
            self.state_handler.play_music(main_menu_music)

    def handle_collisions(self):
        # Player bullets hit enemies
        score_gained = self.collision_handler.check_bullet_enemy_collision(
            self.player_bullets, self.enemies)
        self.score += score_gained
        # Track enemies defeated 
        self.total_enemies_defeated += score_gained // 100

        # Player bullets hit boss
        if self.boss_spawned:
            score_gained = self.collision_handler.check_bullet_boss_collision(self.player_bullets, self.boss,self.boss_spawned)
            self.score += score_gained
            if score_gained >= 1000:  
                self.total_enemies_defeated += 1  # Count boss as an enemy

        damage = self.collision_handler.check_enemy_bullet_player_collision(self.player, self.enemy_bullets)
        if damage > 0:
            if self.player.take_damage(damage):
                self.state = "GAME_OVER"
                self.state_handler.play_music(main_menu_music)
            else:
                self.score = max(0, self.score - 5) # reduce score by 5 for everytime the player gets hits 
        damage = self.collision_handler.check_enemy_player_collision(self.player, self.enemies)
        if damage > 0:
            if self.player.take_damage(damage):
                self.state = "GAME_OVER"
                self.state_handler.play_music(main_menu_music)
            else:
                self.score = max(0, self.score - 5)

        damage = self.collision_handler.check_boss_player_collision(self.player, self.boss)
        if damage > 0:
            if self.player.take_damage(damage):
                self.state = "GAME_OVER"
                self.state_handler.play_music(main_menu_music)
            else:
                self.score = max(0, self.score - 200)
         
    def update(self):
        # Update game state
        if self.state == "PLAYING":
            self.update_gameplay()

    def draw(self):
        # Draw the current game state
        self.renderer.draw_state(
            self.state, 
            self.menu_manager, 
            self.score, 
            self.current_level,
            all_sprites=self.all_sprites,
            camera=self.camera,
            player=self.player,
            boss=self.boss,
            boss_spawned=self.boss_spawned,
            boss_trigger_x=self.boss_trigger_x,
            current_level=self.current_level,
            total_enemies_defeated=self.total_enemies_defeated,
            time_played=self.get_time_played()
        )

    def run(self):
        #Main game loop
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# python sets main file as __main__ automatically so it can be run directly 
if __name__ == "__main__":
    game = Game()
    game.run()

