import pygame, os, sys, time
pygame.mixer.init()
pygame.font.init()

pygame.display.set_caption("první hra")

WIDTH, HEIGHT = 900, 500 #velikost obrazovky
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CREAM_COL = (242, 219, 163)
BLACK = (0, 0, 0)
PINK = (232, 0, 156)
YELLOW = (232, 224, 10)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH//2 - 7.5 , 0, 15, HEIGHT)

HIT_SOUND = pygame.mixer.Sound('bubble.wav')
SHOOT_SOUND = pygame.mixer.Sound('shoot.mp3')

HEALTH_FONT = pygame.font.SysFont('harlowsolid', 40)
WINNER_FONT = pygame.font.SysFont('algerian', 115)

FPS = 60 #kolik framu za sekundu
MOVEMENT = 3

BUL_WIDTH = 10
BUL_HEIGHT = 5
BULLET_MOVEMENT = 7
MAX_BULLET = 4

YELLOW_HIT = pygame.USEREVENT + 1 #1==unique id eventu,yellow a pink nemuzou mit stejne cislo
PINK_HIT = pygame.USEREVENT + 2 #nejakej event

#r ->rawstring dělá, aby to bral "\" jako obyč znak(v pythonu je "\" escape backlash ) 
#nebo můžeme "\" zdvojit viz. \\
#nebo místo "\" použít "/"

JELLY_PATH = ("jelly_left.png")
TEDDY_PATH = ("teddy_right.png")
BACK_PATH = ("space1.webp")


#u teddy jsem použila rotate u jelly ne
JELLY_WIDTH, JELLY_HEIGHT = 80, 80
TEDDY_WIDTH, TEDDY_HEIGHT = 80, 80
TEDDY = pygame.image.load(TEDDY_PATH)
TEDDY = pygame.transform.rotate(pygame.transform.scale(TEDDY, (TEDDY_WIDTH, TEDDY_HEIGHT)), -90)#90stupnu rotace
JELLY = pygame.image.load(JELLY_PATH)
JELLY = pygame.transform.scale(JELLY, (JELLY_WIDTH, JELLY_HEIGHT))#nerotace:D

BACKGROUND = pygame.transform.scale(pygame.image.load(BACK_PATH), (WIDTH, HEIGHT))





def yellow_move(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - MOVEMENT + 10 > 0:
             yellow.x -= MOVEMENT
        if keys_pressed[pygame.K_d] and yellow.x + MOVEMENT + TEDDY_WIDTH - 6 < BORDER.x : #musí tam být teddy_width, aby to nepřekročilo border
             yellow.x += MOVEMENT
        if keys_pressed[pygame.K_w] and yellow.y - MOVEMENT + 10 > 0:
             yellow.y -= MOVEMENT
        if keys_pressed[pygame.K_s] and yellow.y + MOVEMENT + TEDDY_HEIGHT - 5 < HEIGHT:
             yellow.y += MOVEMENT
9
def pink_move(keys_pressed, pink):
        if keys_pressed[pygame.K_LEFT] and pink.x - MOVEMENT - 5 > BORDER.x :#left
             pink.x -= MOVEMENT
        if keys_pressed[pygame.K_RIGHT] and pink.x + JELLY_WIDTH + MOVEMENT - 10 < WIDTH:#right -10je par pixelů, aby to bylo víc clean ale není to potřebný
             pink.x += MOVEMENT
        if keys_pressed[pygame.K_UP] and pink.y - MOVEMENT + 12 > 0: #up
             pink.y -= MOVEMENT
        if keys_pressed[pygame.K_DOWN] and pink.y + MOVEMENT + JELLY_HEIGHT - 15 < HEIGHT :#down
             pink.y += MOVEMENT

def handle_bullets(yellow_bullets, pink_bullets, yellow, pink):
     for bullet in yellow_bullets:
          bullet.x += BULLET_MOVEMENT
          if pink.colliderect(bullet):#pokud pink se setká s bullet
               pygame.event.post(pygame.event.Event(PINK_HIT))
               yellow_bullets.remove(bullet)
          elif bullet.x > WIDTH:
               yellow_bullets.remove(bullet)

     for bullet in pink_bullets:
          bullet.x -= BULLET_MOVEMENT
          if yellow.colliderect(bullet):#pokud pink se setká s bullet
               pygame.event.post(pygame.event.Event(YELLOW_HIT))
               pink_bullets.remove(bullet)    
          elif bullet.x < 0:
               pink_bullets.remove(bullet) 
#díky tomuhle je to actually vidět

def grafics(pink, yellow, pink_bullets, yellow_bullets, pink_health, yellow_health ):#aby funkce znala proměné pink yellow
        SCREEN.blit(BACKGROUND,(0, 0))
     #    pygame.draw.rect(SCREEN, BLACK, BORDER)#kam kreslíme, barvu a co kreslímeˇ

        pink_health_text = HEALTH_FONT.render("Health: " + str(pink_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

        pink_health_text = HEALTH_FONT.render("Health: " + str(pink_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        SCREEN.blit(pink_health_text, (WIDTH - pink_health_text.get_width() - 10, 10))#get_width odečíta velikost textu, -10,10 na ose y a x
        SCREEN.blit(yellow_health_text, (10, 10))#tady už nemusíme použít get.width idk jak to vysvětlit prostě si nakres osu Thuy
        
        SCREEN.blit(JELLY, (pink.x, pink.y))#jelly zastupuje pink rectangle->proto x==700 y==300
        SCREEN.blit(TEDDY, (yellow.x, yellow.y))

        for bullet in pink_bullets:
             pygame.draw.rect(SCREEN, PINK, bullet)
        for bullet in yellow_bullets:
             pygame.draw.rect(SCREEN, YELLOW, bullet)

        pygame.display.update()#musime updatenout, aby se to cream col ukázala

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()

    waiting = True
    while waiting:
         for event in pygame.event.get():
              if event.type == pygame.QUIT: #když zavřeme okno
                   pygame.quit()
                   sys.exit()
              if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_SPACE: #Restart
                        waiting = False
                   if event.key == pygame.K_ESCAPE: #quit escapem
                        pygame.quit()     
                        sys.exit()          
                   




def main():
    pink = pygame.Rect(700, 300, JELLY_WIDTH, JELLY_HEIGHT)#
    yellow = pygame.Rect(100, 300, TEDDY_WIDTH, TEDDY_HEIGHT)#pink.x position, y position, width, height

    pink_bullets = []
    yellow_bullets = []

    pink_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    
    running = True #nekonečný cyklus
    while running:
        clock.tick(FPS) #rychlost loopu, nikdy nepřekročíme 60 framu za sekundu
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #pokud se stane event quit ukonči hru
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:#leftcontol
                      bullet = pygame.Rect(
                           yellow.x + TEDDY_WIDTH - 6, yellow.y + TEDDY_HEIGHT//2 - 2.5, BUL_WIDTH,BUL_HEIGHT)#/2 vystřelí zprostředka výšky teddy,-2.5->pol výškybullet,
                      yellow_bullets.append(bullet)
                      SHOOT_SOUND.play() 

                 if event.key == pygame.K_RCTRL and len(pink_bullets) < MAX_BULLET:#nestrilej dalsi bullets pokud na screen už je maximalni pocet bullets
                      bullet = pygame.Rect(
                           pink.x, pink.y + JELLY_HEIGHT//2 , BUL_WIDTH, BUL_HEIGHT)
                      pink_bullets.append(bullet)
                      SHOOT_SOUND.play()

            if event.type == PINK_HIT:
                 pink_health -= 1
                 HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                 yellow_health -= 1
                 HIT_SOUND.play()

            winner_text = "" #prázdný win
            if pink_health <= 0:
                 winner_text = "TEDDY WINS!"
            if yellow_health <= 0:
                 winner_text = "JELLY WINS!"
            if winner_text != "":#pokud není prázdný
                 draw_winner(winner_text)
                 main() #někdo vyhrál
                 return
             

        keys_pressed = pygame.key.get_pressed()
        yellow_move(keys_pressed, yellow)
        pink_move(keys_pressed, pink)
        
        handle_bullets(yellow_bullets, pink_bullets, yellow, pink)
    
        grafics(pink, yellow, pink_bullets, yellow_bullets, pink_health, yellow_health)
    
    main()



#spoštíme hlavní funkci
if __name__ == "__main__":
    main()
