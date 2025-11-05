import pygame, sys, json,time            # knihovna pro tvorbu her

import subprocess          # umoznuje spoustet dalsi python skripty (minihry)

# Inicializace 
pygame.init()              # inicializace pygame modulu
screen = pygame.display.set_mode((800, 600))   # vytvori herni okno 800x600
pygame.display.set_caption("Virtualni mazlicek")  # nastavi nazev okna
clock = pygame.time.Clock()                     # vytvori casovac pro FPS
font = pygame.font.Font(None, 40)               # velky font pro text
stat_font = pygame.font.Font(None, 28)          # mensi font pro statistiky

#  Herni stavy 
STATE_MAIN = "main"                            # stav hlavni hry
STATE_MINIGAME_MENU = "minigame_menu"          # stav menu miniher
game_state = STATE_MAIN                        # startovni stav hry

# -Ulozene penize 
SAVE_FILE = "save.json"                        # soubor, kam se ukladaji penize

def load_money():                              # funkce pro nacteni penez
    if os.path.exists(SAVE_FILE):              # pokud soubor existuje
        try:
            with open(SAVE_FILE, "r") as f:    # otevre soubor pro cteni
                data = json.load(f)            # precte JSON data
            return data.get("money", 0)        # vrati ulozene penize nebo 0
        except:
            return 0                           # pri chybe vrati 0
    return 0                                   # kdyz soubor neexistuje, vrati 0

def save_money(amount):                        # funkce pro ulozeni penez
    try:
        with open(SAVE_FILE, "w") as f:        # otevre soubor pro zapis
            json.dump({"money": amount}, f)    # ulozi penize jako JSON
    except Exception as e:
        print("Chyba pri ukladani penez:", e)  # vypise chybu, kdyz neulozi

money = load_money()                           # nacte penize pri spusteni hry

# Mistnosti a objekty 
rooms = {                                      # definice mistnosti
    "Obyvak": {"color": (150, 200, 255), "objects": {"Konzole": (600, 300, 120, 70)}},
    "Kuchyn": {"color": (200, 180, 150), "objects": {"Lednice": (100, 200, 80, 120)}},
    "Loznice": {"color": (180, 150, 200), "objects": {"Postel": (300, 350, 200, 100)}},
    "Koupelna": {"color": (150, 220, 220), "objects": {"Sprcha": (350, 200, 80, 120)}}
}
current_room = "Obyvak"                        # startovni mistnost

room_buttons = []                              # seznam tlacitek pro prepinani mistnosti
x, y = 20, 500                                 # pozice prvniho tlacitka
for room_name in rooms:                        # pro kazdou mistnost
    room_buttons.append((room_name, pygame.Rect(x, y, 150, 40)))  # vytvori tlacitko
    x += 160                                   # posune tlacitko doprava

# Statistiky mazlicka 
pet_stats = {                                  # zacatek statistik
    "hlad": 100,
    "zabava": 100,
    "hygiena": 100,
    "spanek": 100
}
DECAY_RATE = 0.05                              # rychlost poklesu statistik
last_update = time.time()                      # cas posledni aktualizace

#  Animace mazlicka -
pet_size = 80                                  # velikost mazlicka
pet_pos = (screen.get_width()//2 - pet_size//2, screen.get_height()//2 - pet_size//2)  
# pozice mazlicka doprostred obrazovky
pet_color = (255, 200, 0)                      # barva mazlicka
t = 0                                          # cas pro animaci (sinusovy pohyb)

#Pomocne funkce 
def draw_text(text, x, y, fnt=font):           # funkce pro vykresleni textu
    screen.blit(fnt.render(text, True, (255, 255, 255)), (x, y))

def draw_pet_stats():                          # funkce pro vykresleni statistik mazlicka
    x = 150
    y = 20
    for stat, value in pet_stats.items():      # projde vsechny statistiky
        pygame.draw.rect(screen, (50,50,50), (x, y+20, 100, 10), border_radius=5)  # pozadi pruhu
        pygame.draw.rect(screen, (0,200,0), (x, y+20, int(value), 10), border_radius=5)  # aktualni hodnota
        screen.blit(stat_font.render(f"{stat.capitalize()}", True, (255,255,255)), (x, y)) # nazev statistiky
        x += 150

def run_minigame(file_name):                   # funkce pro spusteni minihry
    global money
    try:
        subprocess.run(["python", file_name])  # spusti minihru jako dalsi skript
        reward_file = "reward.json"
        if os.path.exists(reward_file):        # pokud existuje soubor s odmenou
            with open(reward_file, "r") as f:
                data = json.load(f)            # precte data
            reward = 0
            if "snake" in file_name:           # pokud je to snake
                reward = data.get("snake", 0)
            elif "ball" in file_name:          # pokud je to ball hra
                reward = data.get("ball", 0)
            elif "reakce" in file_name:        # pokud je to reakce
                reward = data.get("reaction", 0)
            money += reward                    # prida odmenu k penezum
            save_money(money)                  # ulozi nove penize
            with open(reward_file, "w") as f:
                json.dump({}, f)               # smaze soubor s odmenou (vynuluje)
    except Exception as e:
        print("Chyba pri spusteni hry:", e)


while True:                                   # nekonecna smycka hry
    for event in pygame.event.get():          # zpracovani udalosti
        if event.type == pygame.QUIT:         # kdyz hrac zavre okno
            save_money(money)                 # ulozi penize
            pygame.quit()                     # vypne pygame
            sys.exit()                        # ukonci program

    #  Pokles statistik mazlicka 
    now = time.time()                         # aktualni cas
    delta = now - last_update                 # kolik ubehlo sekund
    if delta > 1:                             # kazdou sekundu sniz statistiky
        pet_stats["hlad"] = max(0, pet_stats["hlad"] - DECAY_RATE * 10)
        pet_stats["zabava"] = max(0, pet_stats["zabava"] - DECAY_RATE * 5)
        pet_stats["hygiena"] = max(0, pet_stats["hygiena"] - DECAY_RATE * 3)
        pet_stats["spanek"] = max(0, pet_stats["spanek"] - DECAY_RATE * 2)
        last_update = now                     # ulozi novy cas

    # Vykresleni mistnosti 
    screen.fill(rooms[current_room]["color"]) # vyplni obrazovku barvou mistnosti

    for obj_name, rect_data in rooms[current_room]["objects"].items():  # projde objekty
        rect = pygame.Rect(rect_data)
        pygame.draw.rect(screen, (180, 100, 250), rect, border_radius=10)
        pygame.draw.rect(screen, (120,60,200), rect, 3, border_radius=10)
        draw_text(obj_name, rect.x + 5, rect.y + 5, stat_font)
        if pygame.mouse.get_pressed()[0]:     # pokud hrac drzi leve tlacitko mysi
            mx, my = pygame.mouse.get_pos()   # zjisti pozici mysi
            if rect.collidepoint(mx, my):     # pokud klikne na objekt
                pygame.time.wait(150)         # kratke cekani proti dvojkliku
                if current_room == "Obyvak" and obj_name == "Konzole":
                    game_state = STATE_MINIGAME_MENU   # otevre menu miniher
                elif current_room == "Kuchyn" and obj_name == "Lednice":
                    pet_stats["hlad"] = min(100, pet_stats["hlad"] + 20)   # doplni hlad
                elif current_room == "Koupelna" and obj_name == "Sprcha":
                    pet_stats["hygiena"] = min(100, pet_stats["hygiena"] + 30) # zvysi hygienu
                elif current_room == "Loznice" and obj_name == "Postel":
                    pet_stats["spanek"] = min(100, pet_stats["spanek"] + 30)   # doplni spanek

    for name, rect in room_buttons:           # projde vsechny tlacitka mistnosti
        pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
        pygame.draw.rect(screen, (50,50,200), rect, 3, border_radius=10)
        draw_text(name, rect.x + 10, rect.y + 5)
        if pygame.mouse.get_pressed()[0]:     # pri kliknuti na tlacitko
            mx, my = pygame.mouse.get_pos()
            if rect.collidepoint(mx, my):
                current_room = name           # zmeni aktivni mistnost
                pygame.time.wait(150)         # kratke cekani

    draw_text(f"💰 {money}", 20, 20)          # zobrazi pocet penez
    draw_pet_stats()                          # vykresli pruhy statistik


    # Menu miniher
    if game_state == "minigame_menu":         # pokud je hrac v menu miniher
        screen.fill((40, 50, 70))             # zmeni pozadi
        draw_text("Vyber minihru:", 300, 150)
        buttons = [                           # seznam miniher
            ("🎾 Ball", (300, 250, 200, 50), "ball.py"),
            ("⚡ Reakce", (300, 320, 200, 50), "reakce.py"),
            ("🐍 Snake", (300, 390, 200, 50), "snake.py"),
            ("⬅️ Zpet", (300, 470, 200, 50), None)
        ]
        for label, rect_data, file_name in buttons:   # vykresli tlacitka miniher
            rect = pygame.Rect(rect_data)
            pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
            pygame.draw.rect(screen, (50,50,200), rect, 3, border_radius=10)
            draw_text(label, rect.x + 30, rect.y + 10)
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()):
                pygame.time.wait(150)
                if file_name:
                    run_minigame(file_name)   # spusti vybranou minihru
                game_state = STATE_MAIN       # po konci se vrati do hlavni hry

    pygame.display.flip()                    
    clock.tick(30)                          
