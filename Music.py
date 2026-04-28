import pygame 
pygame.mixer.init()
#load in music files
main_menu_music = pygame.mixer.Sound('music/Main_Menu.mp3')
gameplay_music = pygame.mixer.Sound('music/Game.mp3')
between_levels_music = pygame.mixer.Sound('music/Main_Menu.mp3')
final_screen_music = pygame.mixer.Sound('music/Final Screen.mp3')
Boss_battle = pygame.mixer.Sound('music/Boss.mp3')
main_menu_music.set_volume(0.5)
gameplay_music.set_volume(0.5)
between_levels_music.set_volume(0.5)   
final_screen_music.set_volume(0.5)
Boss_battle.set_volume(0.5)

all_tracks = [main_menu_music, gameplay_music, between_levels_music, final_screen_music, Boss_battle]

# to turn music on or off
class MusicManager:
    def __init__(self):
        self.muted = False

    def toggle(self):
        self.muted = not self.muted
        if self.muted:
            for track in all_tracks:
                track.set_volume(0)
        else:
            for track in all_tracks:
                track.set_volume(0.5)

    def is_muted(self):
        return self.muted

music_manager = MusicManager()