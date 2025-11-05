import pygame
import sys
import random
import json
import os

# Inicializace
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("🐍 Snake")
clock = pygame.time.Clock()

# Barvy
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Velikost bloku hada
block_size = 25
font = pygame.font.Font(None, 36)

def draw_snake(snake_blocks):
    for block in snake_blocks:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], block_size, block_size))
        pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(block[0], block[1], block_size, block_size), 2)

# Funkce pro uložení odměny do JSON
def save_reward(score):
    reward_file = "reward.json"
    data = {"snake": score}  # můžeš rozšířit pro další hry
    try:
        with open(reward_file, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Chyba při ukládání odměny:", e)

def game_loop():
    snake = [(100, 100), (75, 100), (50, 100)]
    direction = "RIGHT"
    food = (
        random.randrange(0, 600 - block_size, block_size),
        random.randrange(0, 400 - block_size, block_size)
    )
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_reward(score)  # uloží skóre i při ESC
                    return
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Pohyb hada
        x, y = snake[0]
        if direction == "UP":
            y -= block_size
        elif direction == "DOWN":
            y += block_size
        elif direction == "LEFT":
            x -= block_size
        elif direction == "RIGHT":
            x += block_size

        new_head = (x, y)

        # Kolize = konec hry
        if x < 0 or x >= 600 or y < 0 or y >= 400 or new_head in snake:
            save_reward(score)  # uloží skóre při prohře
            screen.fill(BLACK)
            text = font.render(f"KONEC HRY! Skóre: {score}", True, WHITE)
            screen.blit(text, (170, 180))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        snake.insert(0, new_head)

        # Jídlo
        if new_head == food:
            score += 1
            food = (
                random.randrange(0, 600 - block_size, block_size),
                random.randrange(0, 400 - block_size, block_size)
            )
        else:
            snake.pop()

        # Kreslení
        screen.fill(BLACK)
        draw_snake(snake)
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], block_size, block_size))
        score_text = font.render(f"Skóre: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(8)

if __name__ == "__main__":
    game_loop()

