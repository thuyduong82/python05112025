import pygame
from utility import image_cutter

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 150
        self.y = 150
        self.spritesheet = pygame.image.load("assets/characters/player/man_brownhair_run.png").convert_alpha()  
        self.image = image_cutter(self.spritesheet, 0, 0, 15, 16, 3)
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.index = 0
        self.speed = 10
        self.lives = 3
        self.invulnerability = False
        self.frame_count = 3
        self.elapsed_time = 0
    
    def animation(self, row):

        self.index += 0.1
        if self.index >= self.frame_count:
            self.index = 0
        
        self.image = image_cutter(self.spritesheet, int(self.index), row, 15, 16, 3)


    def update(self, monster_group,sprite_groups, clock):
        key = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if key[pygame.K_w]:
            self.animation(1)
            self.rect.top -= self.speed
        if key[pygame.K_a]:
            self.animation(2)
            self.rect.left -= self.speed
        if key[pygame.K_s]:
            self.animation(0)
            self.rect.bottom += self.speed
        if key[pygame.K_d]:
            self.animation(3)
            self.rect.right += self.speed
        
        if self.elapsed_time > 2000:
            # vypni nesmrtelnost
            self.invulnerability = False

        self.elapsed_time += clock.get_time()

        if pygame.sprite.spritecollide(self, monster_group, False):
            if not self.invulnerability:
                self.lives -= 1 # odeber život
                self.invulnerability = True # zapni nesmrtelnost
                self.elapsed_time = 0 # vynuluj časomíru
        
        if pygame.sprite.spritecollide(self, sprite_groups, False):
            if not self.invulnerability:
                self.lives += 1 # odeber život
                self.invulnerability = True # zapni nesmrtelnost
                self.elapsed_time = 0 # vynuluj časomíru
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)