import pygame
from settings import *
from ui import *
from items import *

class GameRenderer:
    #Handles all game drawing 
    
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
    
    def draw_sprites(self, all_sprites, camera, player):
        #Draw all game sprites with camera offset
        for sprite in all_sprites:
            if camera.is_visible(sprite):
                screen_x = sprite.rect.x - camera.x
                screen_y = sprite.rect.y - camera.y
                
                # Handle player invulnerability flashing
                if sprite == player and player.invulnerable:
                    if (pygame.time.get_ticks() // 100) % 2:
                        self.screen.blit(sprite.image, (screen_x, screen_y))
                else:
                    self.screen.blit(sprite.image, (screen_x, screen_y))
    
    def draw_game_scene(self, all_sprites, camera, player, boss, boss_spawned,score, level, boss_trigger_x, current_level):
        # Draw scrolling background
        scroll_x = camera.get_scroll_offset()
        self.background.draw(self.screen, scroll_x)
        
        # Draw all sprites
        self.draw_sprites(all_sprites, camera, player)
        
        # Draw boss health bar if applicable
        if boss_spawned and boss and boss.alive():
            boss.draw_health_bar(self.screen, fixed_position=True)
        
        # Draw HUD
        draw_hud(self.screen, player, score, level, health_style="hearts")
        
        # Draw power-up indicators
        draw_powerup_icons(self.screen, player.powerup_manager)
    
    def draw_state(self, state, menu_manager, score, level, all_sprites=None, 
                   camera=None, player=None, boss=None, boss_spawned=False,
                   boss_trigger_x=0, current_level=1, total_enemies_defeated=0, 
                   time_played=0):
        #Draw the appropriate screen based on game state
        if state == "MENU":
            draw_menu(self.screen)
            menu_manager.draw_buttons(self.screen, 'main_menu')
        
        elif state == "LEVEL_SELECT":
            draw_level_selector(self.screen)
            menu_manager.draw_buttons(self.screen, 'level_select')
        
        elif state == "CONTROLS":
            draw_controls_screen(self.screen)
            menu_manager.draw_buttons(self.screen, 'controls')
        
        elif state == "PLAYING":
            self.draw_game_scene(all_sprites, camera, player, boss, boss_spawned,
                               score, level, boss_trigger_x, current_level)
        
        elif state == "PAUSED":
            self.draw_game_scene(all_sprites, camera, player, boss, boss_spawned,
                               score, level, boss_trigger_x, current_level)
            draw_pause_overlay(self.screen)
            menu_manager.draw_buttons(self.screen, 'pause_menu')
        
        elif state == "GAME_OVER":
            draw_game_over(self.screen, score)
            menu_manager.draw_buttons(self.screen, 'game_over')
        
        elif state == "LEVEL_COMPLETE":
            draw_level_complete(self.screen, score, level)
            menu_manager.draw_buttons(self.screen, 'level_complete')
        
        elif state == "GAME_COMPLETE":
            draw_game_complete(self.screen, score)
            menu_manager.draw_buttons(self.screen, 'game_complete')
        
        elif state == "FINAL_VICTORY":
            draw_final_victory(self.screen, score, 
                             levels_completed=current_level,
                             enemies_defeated=total_enemies_defeated,
                             time_played=None)
            menu_manager.draw_buttons(self.screen, 'final_victory')
        
        pygame.display.flip()