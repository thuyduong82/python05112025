import pygame
import random
from sys import exit

pygame.init()
pygame.display.set_caption("Opyluj květinu")

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
MOVEMENT = 5

BEE_WIDTH, BEE_HEIGHT = 50, 50
BEE = pygame.image.load("bee.png")
BEE = pygame.transform.scale(BEE, (BEE_WIDTH, BEE_HEIGHT))

TULIP_WIDTH, TULIP_HEIGHT = 50, 50
TULIP = pygame.image.load("tulipan.png")
TULIP = pygame.transform.scale(TULIP, (TULIP_WIDTH, TULIP_HEIGHT))

FONT = pygame.font.Font(None, 40)

def bee_move(bee_direction):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and bee_direction != "DOWN":
                return "UP"
            elif event.key == pygame.K_DOWN and bee_direction != "UP":
                return "DOWN"
            elif event.key == pygame.K_LEFT and bee_direction != "RIGHT":
                return "LEFT"
            elif event.key == pygame.K_RIGHT and bee_direction != "LEFT":
                return "RIGHT"
    return bee_direction

def move_bee(yellow, direction):
    if direction == "UP":
        yellow.y -= MOVEMENT
    elif direction == "DOWN":
        yellow.y += MOVEMENT
    elif direction == "LEFT":
        yellow.x -= MOVEMENT
    elif direction == "RIGHT":
        yellow.x += MOVEMENT
    
    yellow.x = max(0, min(SCREEN_WIDTH - BEE_WIDTH, yellow.x))
    yellow.y = max(0, min(SCREEN_HEIGHT - BEE_HEIGHT, yellow.y))

def place_tulip():
    return pygame.Rect(
        random.randint(0, SCREEN_WIDTH - TULIP_WIDTH),
        random.randint(0, SCREEN_HEIGHT - TULIP_HEIGHT),
        TULIP_WIDTH,
        TULIP_HEIGHT
    )

def draw_graphics(yellow, pink, score):
    SCREEN.fill("powderblue")
    SCREEN.blit(BEE, (yellow.x, yellow.y))
    SCREEN.blit(TULIP, (pink.x, pink.y))
    
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    SCREEN.blit(score_text, (20, 20))
    
    pygame.display.update()

def main():
    bee_direction = "RIGHT"
    pink = place_tulip()  #někam dát tulipán
    yellow = pygame.Rect(100, 150, BEE_WIDTH, BEE_HEIGHT)
    clock = pygame.time.Clock()
    score = 0  
    
    while True:
        clock.tick(FPS)
        bee_direction = bee_move(bee_direction)  #změnit směr včeličky
        move_bee(yellow, bee_direction) 
        
        if yellow.colliderect(pink):
            score += 1  
            pink = place_tulip()  
        
        draw_graphics(yellow, pink, score) 

if __name__ == "__main__":
    main()
