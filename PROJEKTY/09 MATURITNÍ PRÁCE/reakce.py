import pygame
import random
import sys
import time
import json
import os

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Klikni na kruh")

WHITE = (255,255,255)
RED = (230,50,50)
BLACK = (0,0,0)

font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 64)

circle_radius = 50
circle_x = random.randint(circle_radius, WIDTH - circle_radius)
circle_y = random.randint(circle_radius, HEIGHT - circle_radius)

score = 0
missed = 0
zivotnost = 1.2
spawn_time = time.time()

clock = pygame.time.Clock()
game_over = False

#unkce pro ukládání odměny
def save_reward(score):
    reward_file = "reward.json"
    data = {"reaction": score}  # identifikátor hry
    try:
        with open(reward_file, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Chyba při ukládání odměny:", e)


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save_reward(score)
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            dist = ((mx - circle_x)**2 + (my - circle_y)**2)**0.5
            if dist <= circle_radius:
                score += 1

                if score % 3 == 0 and zivotnost > 0.4:
                    zivotnost -= 0.1

                circle_x = random.randint(circle_radius, WIDTH - circle_radius)
                circle_y = random.randint(circle_radius, HEIGHT - circle_radius)
                spawn_time = time.time()

    if not game_over:
        if time.time() - spawn_time > zivotnost:
            missed += 1
            if missed >= 5:
                save_reward(score)  # uloží skóre při konci hry
                game_over = True
            else:
                circle_x = random.randint(circle_radius, WIDTH - circle_radius)
                circle_y = random.randint(circle_radius, HEIGHT - circle_radius)
                spawn_time = time.time()

 
    screen.fill(WHITE)

    if not game_over:
        pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
        text1 = font.render(f"Skóre: {score}", True, BLACK)
        text2 = font.render(f"Netrefeno: {missed}/5", True, BLACK)
        screen.blit(text1, (10,10))
        screen.blit(text2, (10,50))
    else:
        t1 = bigfont.render("KONEC HRY", True, BLACK)
        t2 = font.render(f"Skóre: {score}", True, BLACK)
        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 60))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)
