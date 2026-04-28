import pygame
from platform_1 import *
from enemy import * 
from boss import *
from flag import *
from items import *

def load_level(level_num):
   
    if level_num == 1:
        # LEVEL 1 
        platform_data = [
            (-20, 550, 1000, 50),  
            (200, 450, 150, 20), 
            (450, 350, 150, 20),   
            (650, 250, 150, 20),  
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]

        enemies = [
            Enemy(220, 345, patrol_range=80, speed=1, difficulty_level=1), 
            Enemy(470, 245, patrol_range=80, speed=1, difficulty_level=1)  
        ]

        items = [
            MedKitItem(300, 420, image_path='IMG/items/medkit.png'),
            RapidFireItem(500, 320, image_path='IMG/items/RapidFire.png'),        
        ]
        
        flag = Flag(720, 180, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None  

    # LEVEL 2 
    elif level_num == 2:
        platform_data = [
            (-20, 550, 400, 50),    
            (150, 450, 150, 20),  
            (350, 350, 150, 20),
            (550, 280, 150, 20),
            (700, 200, 150, 20),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]

        enemies = [
            Enemy(170, 350, patrol_range=88, speed=2, difficulty_level=2),  
            Enemy(370, 250, patrol_range=88, speed=2, difficulty_level=2),   
            Enemy(570, 180, patrol_range=88, speed=2, difficulty_level=2),  
        ]

        items = [
            MedKitItem(400, 320, image_path='IMG/items/medkit.png'),
            RapidFireItem(600, 250, image_path='IMG/items/RapidFire.png'),
        ]

        flag = Flag(770, 125, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None

    # LEVEL 3
    elif level_num == 3:
        platform_data = [
            (-20, 550, 250, 50),
            (300, 480, 100, 20),
            (450, 420, 100, 20),
            (600, 360, 100, 20),
            (750, 320, 180, 25),  
            (980, 280, 100, 20),
            (1130, 220, 100, 20),
            (1280, 180, 100, 20),
            (1430, 150, 100, 20),
            (1550, 250, 150, 30),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]

        enemies = [
            Enemy(320, 380, patrol_range=50, speed=1.5, difficulty_level=3),    
            Enemy(470, 320, patrol_range=60, speed=1.5, difficulty_level=3),    
            Enemy(620, 260, patrol_range=50, speed=1.5, difficulty_level=3),    
            Enemy(1000, 180, patrol_range=60, speed=2, difficulty_level=3),   
            Enemy(1300, 80, patrol_range=50, speed=2, difficulty_level=3),     
        ]

        items = [
            MedKitItem(800, 270, image_path='IMG/items/medkit.png'),
            RapidFireItem(1150, 190, image_path='IMG/items/RapidFire.png'),
        ]

        flag = Flag(1600, 180, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None

    # LEVEL 4 
    elif level_num == 4:
        platform_data = [
            (-20, 550, 600, 50),
            (480, 500, 180, 20),
            (280, 390, 180, 20),
            (480, 290, 180, 20),
            (680, 170, 150, 20),
            (850, 170, 150, 20),
            (1020, 170, 150, 20),
            (1190, 200, 150, 20),
            (1360, 230, 150, 20),
            (1530, 260, 200, 30),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]

        enemies = [
            Enemy(500, 390, patrol_range=80, speed=2, difficulty_level=4),   
            Enemy(300, 290, patrol_range=80, speed=2, difficulty_level=4),   
            Enemy(500, 190, patrol_range=80, speed=2, difficulty_level=4),   
            Enemy(870, 40, patrol_range=80, speed=2.5, difficulty_level=4),    
            Enemy(1210, 80, patrol_range=80, speed=2.5, difficulty_level=4),   
        ]
        
        items = [
            MedKitItem(380, 350, image_path='IMG/items/medkit.png'),
            RapidFireItem(570, 260, image_path='IMG/items/RapidFire.png'),
        ]

        flag = Flag(1600, 190, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None

    # LEVEL 5
    elif level_num == 5:
        platform_data = [
            (-20, 550, 350, 50),
            (400, 480, 120, 20),
            (580, 420, 120, 20),
            (760, 380, 120, 20),
            (940, 350, 200, 30),
            (1200, 410, 100, 20),
            (1360, 380, 100, 20),
            (1520, 420, 100, 20),
            (1680, 380, 100, 20),
            (1840, 360, 200, 30),
            (2100, 420, 90, 20),
            (2250, 470, 90, 20),
            (2400, 430, 90, 20),
            (2550, 480, 90, 20),
            (2710, 410, 200, 30),
            (2970, 460, 100, 20),
            (3120, 420, 100, 20),
            (3270, 380, 100, 20),
            (3420, 350, 100, 20),
            (3570, 330, 100, 20),
            (3730, 310, 200, 40),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]
        
        enemies = [
            Enemy(430, 380, patrol_range=50, speed=2, difficulty_level=5),   
            Enemy(610, 320, patrol_range=50, speed=2, difficulty_level=5),    
            Enemy(1000, 250, patrol_range=110, speed=2, difficulty_level=5),  
            Enemy(1230, 290, patrol_range=40, speed=2.5, difficulty_level=5),   
            Enemy(1900, 240, patrol_range=110, speed=2.5, difficulty_level=5),  
            Enemy(2130, 300, patrol_range=30, speed=2.5, difficulty_level=5),  
            Enemy(2770, 290, patrol_range=110, speed=2.5, difficulty_level=5), 
            Enemy(3000, 340, patrol_range=50, speed=3, difficulty_level=5),  
            Enemy(3300, 260, patrol_range=50, speed=3, difficulty_level=5),   
        ]
        
        items = [
            RapidFireItem(1000, 300, image_path='IMG/items/RapidFire.png'),
            MedKitItem(1900, 310, image_path='IMG/items/medkit.png'),
            TripleShotItem(2770, 360, image_path='IMG/items/TripleFire.png'),
        ]
        
        flag = Flag(3800, 240, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None

    # LEVEL 6 - 
    elif level_num == 6:
        platform_data = [
            (-20, 550, 350, 50),
            (400, 490, 140, 20),
            (580, 440, 140, 20),
            (760, 390, 140, 20),
            (940, 350, 140, 20),
            (1120, 320, 180, 25),
            (1350, 290, 140, 20),
            (1540, 270, 140, 20),
            (1730, 310, 140, 20),
            (1920, 360, 140, 20),
            (2110, 400, 140, 20),
            (2320, 450, 100, 20),
            (2480, 430, 100, 20),
            (2640, 400, 180, 25),
            (2870, 370, 140, 20),
            (3060, 350, 200, 30),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]
        
        enemies = [
            Enemy(420, 390, patrol_range=90, speed=2.5, difficulty_level=6),   
            Enemy(780, 290, patrol_range=90, speed=2.5, difficulty_level=6),   
            Enemy(1150, 220, patrol_range=120, speed=2.5, difficulty_level=6), 
            Enemy(1560, 170, patrol_range=90, speed=2.5, difficulty_level=6),   
            Enemy(2000, 260, patrol_range=100, speed=2.5, difficulty_level=6),    
            Enemy(2340, 350, patrol_range=70, speed=3, difficulty_level=6),    
            Enemy(2890, 270, patrol_range=100, speed=3, difficulty_level=6),   
        ]
        
        items = [
            MedKitItem(1150, 290, image_path='IMG/items/medkit.png'),
            RapidFireItem(1750, 280, image_path='IMG/items/RapidFire.png'),
            TripleShotItem(2660, 370, image_path='IMG/items/TripleFire.png'),
            MedKitItem(3000, 320, image_path='IMG/items/medkit.png'),
        ]
        
        flag = Flag(3130, 280, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None

    # LEVEL 7 - 
    elif level_num == 7:
        platform_data = [
            (-20, 550, 300, 50),
            (350, 480, 140, 20),
            (540, 430, 120, 20),
            (760, 350, 120, 20),
            (900, 290, 120, 20),
            (1080, 240, 140, 20),
            (1270, 200, 140, 20),
            (710, 490, 120, 20),
            (880, 510, 120, 20),
            (1050, 500, 120, 20),
            (1220, 480, 120, 20),
            (1390, 460, 120, 20),           
            (1560, 420, 150, 25),
            (1560, 220, 100, 20),  
            (1760, 320, 100, 20),
            (1920, 320, 100, 20),
            (2080, 280, 100, 20),
            (2260, 340, 120, 20),
            (2420, 390, 120, 20),
            (2580, 430, 120, 20),
            (2760, 470, 120, 20),   
            (2940, 390, 100, 20),
            (3100, 350, 100, 20),
            (3260, 320, 100, 20),
            (3420, 380, 200, 30),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]
   
        enemies = [
            Enemy(370, 380, patrol_range=90, speed=2.5, difficulty_level=7),    
            Enemy(740, 250, patrol_range=80, speed=3, difficulty_level=7),    
            Enemy(1100, 140, patrol_range=80, speed=3, difficulty_level=7),   
            Enemy(900, 410, patrol_range=90, speed=2.5, difficulty_level=7),
            Enemy(1240, 380, patrol_range=90, speed=2.5, difficulty_level=7),    
            Enemy(1780, 180, patrol_range=60, speed=3, difficulty_level=7),    
            Enemy(2100, 180, patrol_range=60, speed=3.5, difficulty_level=7),   
            Enemy(2440, 290, patrol_range=80, speed=3, difficulty_level=7),   
            Enemy(2960, 290, patrol_range=70, speed=3.5, difficulty_level=7),
            Enemy(3280, 220, patrol_range=70, speed=3.5, difficulty_level=7), 
        ]
        
        items = [
            RapidFireItem(1100, 210, image_path='IMG/items/RapidFire.png'),
            MedKitItem(1050, 470, image_path='IMG/items/medkit.png'),
            MedKitItem(1920, 290, image_path='IMG/items/medkit.png'),
            TripleShotItem(2780, 290, image_path='IMG/items/TripleFire.png'),
            MedKitItem(3180, 320, image_path='IMG/items/medkit.png'),
        ]
        
        flag = Flag(3490, 310, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, None, items, None

    # LEVEL 8 - BOSS BATTLE
    elif level_num == 8:
        platform_data = [
            (-20, 550, 400, 50),
            (500, 470, 120, 20),
            (670, 410, 120, 20),
            (840, 360, 120, 20),
            (1010, 320, 120, 20),
            (1250, 290, 150, 25),
            (1400, 250, 120, 20),
            (1570, 220, 120, 20),
            (1740, 200, 120, 20),
            (1180, 400, 100, 20),
            (1330, 440, 100, 20),
            (1480, 480, 100, 20),
            (1630, 440, 100, 20),
            (1780, 400, 100, 20),
            (1930, 360, 130, 25),
            (2110, 310, 120, 20),
            (2280, 270, 120, 20),
            (2450, 240, 120, 20),          
            (2850, 500, 850, 40),
            (3740, 440, 120, 20),
        ]
        platforms = [Platform(x, y, w, h) for (x, y, w, h) in platform_data]

        enemies = [
            Enemy(530, 350, patrol_range=60, speed=3, difficulty_level=8),   
            Enemy(860, 240, patrol_range=80, speed=3, difficulty_level=8),   
            Enemy(1230, 170, patrol_range=110, speed=3, difficulty_level=8), 
            Enemy(1590, 100, patrol_range=90, speed=3.5, difficulty_level=8),   
            Enemy(1500, 360, patrol_range=70, speed=3, difficulty_level=8),   
            Enemy(1950, 240, patrol_range=100, speed=3.5, difficulty_level=8), 
            Enemy(2130, 190, patrol_range=80, speed=3.5, difficulty_level=8), 
            Enemy(2300, 150, patrol_range=80, speed=3.5, difficulty_level=8),    
            Enemy(2470, 120, patrol_range=80, speed=3.5, difficulty_level=8),   
        ]    

        boss = Boss(3250, 350)
        
        items = [
            MedKitItem(1230, 240, image_path='IMG/items/medkit.png'),
            RapidFireItem(1760, 150, image_path='IMG/items/RapidFire.png'),
            MedKitItem(2300, 220, image_path='IMG/items/medkit.png'),
            TripleShotItem(2450, 190, image_path='IMG/items/TripleFire.png'),
        ]
    
        flag = Flag(3790, 370, image_path="IMG/flag/flag.png", width=50, height=100)
        return platforms, enemies, flag, boss, items, None  

    # Default case
    else:
        return load_level(1)