import pygame, random, sys, json, os           

pygame.init()               

WIDTH, HEIGHT = 400, 720    
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Chytej micky")         


WHITE = (255,255,255)       
RED = (230,50,50)           
BLUE = (50,50,200)         
BLACK = (0,0,0)             

# plosina 
paddle_width = 110        
paddle_height = 16          
paddle_x = WIDTH//2 - paddle_width//2 # pocatecni pozice plosiny na ose X
paddle_y = HEIGHT - 50 # pozice plosiny na ose Y (blizko spodniho okraje)
paddle_speed = 13          

# micky
ball_radius = 15            
ball_count = 2          #najednou můžou být jen 2 micky na obraz
MIN_SPACING_Y = 400         # minimalni svisla vzdalenost mezi micky

base_speeds = [4.0, 4.0]    # zakladni rychlosti jednotlivych micku

# funkce pro nahodnou pozici X v ramci okna
def rand_x():
    return random.randint(ball_radius, WIDTH - ball_radius)

# funkce pro vyber Y tak, aby micky byly rovnomerne rozlozene
def best_spaced_y(existing_y):
    if not existing_y:       # pokud zatim zadne Y neexistuje
        return -random.randint(400, 1000)   # vrat nahodnou hodnotu nad oknem
    best_y = None
    best_score = -1
    for _ in range(300):  # zkusi 300 nahodnych kandidatu
        candidate = -random.randint(400, 1000)  # nahodne Y nad obrazovkou
        distances = [abs(candidate - y) for y in existing_y]  # vypocet vzdalenosti
        min_dist = min(distances)           # nejmensi vzdalenost k ostatnim
        score = min_dist + (10000 if min_dist >= MIN_SPACING_Y else 0)  # hodnoceni pozice
        if score > best_score:       # pokud je lepsi nez dosavadni
            best_score = score
            best_y = candidate
    return best_y                           # vraci optimalni Y

# inicializace micku
balls = []      # seznam micku
speeds = []   # seznam rychlosti
ys = []                # pomocny seznam Y hodnot
for i in range(ball_count):                 # pro kazdy micek
    x = rand_x()                            # nahodna pozice X
    y = best_spaced_y(ys)                   # rozumne rozestavene Y
    balls.append([x, y])                    # ulozime souradnice micku
    speeds.append(base_speeds[i % len(base_speeds)])  # priradime rychlost
    ys.append(y)                            # ulozime Y do seznamu

score = 0                                   # skore hrace
caught = 0                                  # pocet chycenych micku
missed = 0                                  # pocet propadnutych micku
game_over = False                           # stav hry

font = pygame.font.Font(None, 36)           # bezny font
big_font = pygame.font.Font(None, 64)       # vetsi font pro titulky
clock = pygame.time.Clock()                 # casovac pro FPS

# ulozeni odmeny do souboru (napr. pro virtualniho mazlicka)
def save_reward(score):
    reward_file = "reward.json"             # nazev souboru
    data = {"ball": score}                  # struktura dat
    try:
        with open(reward_file, "w") as f:   # otevreni souboru pro zapis
            json.dump(data, f)              # zapis dat do JSON
    except Exception as e:                  # osetreni chyb
        print("Chyba pri ukladani odmeny:", e)

# hlavni herni smycka
while True:
    for e in pygame.event.get():            # zpracovani udalosti
        if e.type == pygame.QUIT:           # kdyz hrac zavre okno
            save_reward(score)              # uloz skore
            pygame.quit()                   # ukonci pygame
            sys.exit()                      # ukonci program

    if game_over:                           # pokud je konec hry
        screen.fill(WHITE)                  # bile pozadi
        go = big_font.render("KONEC HRY", True, BLACK)  # text "Konec hry"
        info = font.render(f"Skore: {score}   Propadlo: {missed}/5", True, BLACK) # info text
        screen.blit(go, (WIDTH//2 - go.get_width()//2, HEIGHT//2 - 60))   # vykresleni napisu
        screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 + 10))
        pygame.display.flip()               # aktualizace obrazovky
        clock.tick(60)                      # cekani pro FPS
        continue                            # preskoci dalsi kod v cyklu

    # pohyb hrace
    keys = pygame.key.get_pressed()         # zjisteni stisknutych klaves
    if keys[pygame.K_LEFT] and paddle_x > 0:  # posun vlevo
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:  # posun vpravo
        paddle_x += paddle_speed

    current_ys = [b[1] for b in balls]      # aktualni seznam Y micku

    for i in range(len(balls)):             # pro kazdy micek
        balls[i][1] += speeds[i]            # posun micku dolu podle rychlosti

        # pokud micek propadne pod spodni okraj
        if balls[i][1] > HEIGHT:
            tmp_ys = current_ys[:]          # kopie Y hodnot
            tmp_ys.pop(i)                   # odebere aktualni
            balls[i][0] = rand_x()          # nove X
            balls[i][1] = best_spaced_y(tmp_ys)  # nove Y nad oknem
            score -= 1                      # zmensi skore
            missed += 1                     # zvysi pocet propadnutych
            if missed >= 5:                 # pokud propadne 5 micku
                save_reward(score)          # uloz skore
                game_over = True            # konec hry

        # kontrola kolize s plosinou
        if (paddle_y < balls[i][1] + ball_radius < paddle_y + paddle_height and
            paddle_x < balls[i][0] < paddle_x + paddle_width):
            score += 1                      # pridani bodu
            caught += 1                     # pocet chycenych
            # zrychleni vsech micku
            for j in range(len(speeds)):
                speeds[j] += 0.5
            tmp_ys = current_ys[:]          # kopie Y hodnot
            tmp_ys.pop(i)
            balls[i][0] = rand_x()          # nove X
            balls[i][1] = best_spaced_y(tmp_ys)  # nove Y nad oknem

    screen.fill(WHITE)                      # vycisteni obrazovky
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))  # vykresleni plosiny
    for b in balls:                         # vykresleni micku
        pygame.draw.circle(screen, RED, (b[0], b[1]), ball_radius)

    hud = font.render(f"Skore: {score}   Propadlo: {missed}/5", True, BLACK)  # text s informacemi
    screen.blit(hud, (10, 10))              # vykresleni textu na obrazovku

    pygame.display.flip()                   # aktualizace obrazovky
    clock.tick(60)                          # omezeni FPS na 60
