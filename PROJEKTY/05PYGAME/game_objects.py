import pygame
from utility import image_cutter

class GameObjects(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image_cutter(pygame.image.load("assets/sproutlands/Objects/Basic_Furniture.png"), 4, 2, 16, 16, 1)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)