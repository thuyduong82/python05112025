import pygame
from utility import image_cutter
from player import Player
from settings import *


class Monster(Player):
    def __init__(self, type, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.spritesheet = pygame.image.load("assets/characters/monsters/monster_spritesheet.png")
        self.type = type
        self.image = image_cutter(self.spritesheet, 0, self.type, 15, 16, 3)
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.index = 0
        self.speed = 10
        self.direction = "left"
        self.frame_count = 2
    
    def update(self):

        if self.rect.x < 0:
            self.direction = "right"
        elif self.rect.x > screen_width:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.right += self.speed

        self.animation(self.type)
        

        


# TODO:
# 1. Pohyb zprava do leva zpět
# 2. Přidat animaci 
# 3. Při tvorbě instance monstra přidat možnost zvolit, 
# jak bude monstrum vypadat (tzn. vykreslovat jiné monstrum ze spritesheetu)
    
