# Program momentálně není funkční, v příští hodině dokončíme přesouvání kódu a hru opět zprovozníme

import pygame
from sys import exit
from settings import *
from utility import image_cutter
from player import Player
from monster import Monster
import json
from game_objects import GameObjects
from player import Player

# inicializuje hru - spustíme pygame
pygame.init()

furniture_group = pygame.sprite.Group()

def create_furniture():
    path_to_json = "assets/world/data.json"
    furniture_img = image_cutter(pygame.image.load("assets/sproutlands/Objects/Basic_Furniture.png"), 4, 2, 16, 16, 1)#x,y,width,height,scale
    with open(path_to_json, mode = "r") as file:
        data = json.load(file)

    for entity in data["entities"]["Furniture"]:
        x = entity["x"]
        y = entity["y"]
        w = entity["w"]
        h = entity["h"]
        furniture = GameObjects(x, y, w, h)
        furniture_group.add(furniture)
    

# vytvoříme obraz
screen = pygame.display.set_mode((screen_width, screen_height))

# vytvoř hodiny
clock = pygame.time.Clock()

running = True

background_img = pygame.image.load("assets/world/background.png")

monsters = pygame.sprite.Group()
monsters.add(Monster(3, 500, 200), Monster(1, 500, 400))

player = pygame.sprite.GroupSingle()
player.add(Player())

# Vytvoření fontu k vykreslení životů - pokud nechcete vlastní font, použijte None (bez uvozovek) místo názvu fontu
font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 25)


# herní smyčka
while running:
    # kontroluje nám události, které se dějí v naší hře
    for event in pygame.event.get():
        # pokud dojde k události vypnout, vypne
        if event.type == pygame.QUIT:
            running = False
            exit()
    
    # proměnná key, pod ní schováme stisknutou klávesu
  

    # pokud je stisknutá klávesa w, pohni hráčem o (x, y)

  
    # obarví obrazovku na bílo
    screen.blit(background_img, (0,0))

    # render fontu
    text_lives = font.render(f"Lives: {player.sprite.lives}", False, "#000000") 
    # vykreslení textu na obrazovku
    screen.blit(text_lives, (screen_width-100, 10))

    text_points = font.render(f"points: {player.sprite.lives}", False, "#000000") 
    # vykreslení textu na obrazovku
    screen.blit(text_points, (screen_width-200, 10))

    # na obrazovku vykresli - surface na rectangle (recntagle má souřadnice, viz výše)
    create_furniture()
    furniture_group.draw(screen)

    player.draw(screen)
    player.update(monsters,furniture_group, clock)
    
    monsters.draw(screen)
    monsters.update()


    # updatuje vše
    pygame.display.update()
    # pygame.display.flip() - alternativní funkce k .update

    # omez tickrate (rychlost hry) na 60fps, ať je to konzistentní napříč zařízeními
    clock.tick(60)