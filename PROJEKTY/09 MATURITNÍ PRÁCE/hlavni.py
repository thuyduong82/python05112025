import pygame, sys, json, time         # knihovny pro hru, ukončení programu, práci se soubory a čas
import subprocess                      # umožní spouštět další python skripty (minihry)
import os                              # potřebné pro kontrolu existence souborů
import math                            # pro animaci mazlíčka (sinusový pohyb)

# -------------------- Inicializace --------------------
pygame.init()                                           # spustí všechny pygame moduly
screen = pygame.display.set_mode((800, 600))            # vytvoří herní okno o velikosti 800x600
pygame.display.set_caption("Virtuální mazlíček")        # nastaví titulek okna
clock = pygame.time.Clock()                             # objekt pro řízení FPS
font = pygame.font.Font(None, 40)                       # základní větší font
stat_font = pygame.font.Font(None, 28)                  # menší font pro texty statistik

# -------------------- Herní stavy --------------------
STATE_MAIN = "main"                                     # hlavní herní stav
STATE_MINIGAME_MENU = "minigame_menu"                   # stav, kdy se zobrazuje menu miniher
game_state = STATE_MAIN                                # výchozí stav hry

# -------------------- Uložené peníze --------------------
SAVE_FILE = "save.json"                                 # soubor, kde se ukládají peníze hráče

# funkce pro načtení peněz ze souboru
def load_money():
    if os.path.exists(SAVE_FILE):                       # pokud soubor existuje
        try:
            with open(SAVE_FILE, "r") as f:             # otevře soubor pro čtení
                data = json.load(f)                     # načte JSON data
            return data.get("money", 0)                 # vrátí hodnotu „money“ nebo 0
        except:
            return 0
    return 0                                            # když soubor neexistuje, vrátí 0

# funkce pro uložení peněz
def save_money(amount):
    try:
        with open(SAVE_FILE, "w") as f:                 # otevře soubor pro zápis
            json.dump({"money": amount}, f)             # zapíše JSON s penězi
    except Exception as e:
        print("Chyba při ukládání peněz:", e)           # vypíše chybu, pokud se zápis nepovede

money = load_money()                                    # načte uložené peníze při startu hry

# -------------------- Místnosti a objekty --------------------
rooms = {                                               # každá místnost má svoji barvu a objekty
    "Obyvak": {"color": (150, 200, 255), "objects": {"Konzole": (600, 300, 120, 70)}},
    "Kuchyn": {"color": (200, 180, 150), "objects": {"Lednice": (100, 200, 80, 120)}},
    "Loznice": {"color": (180, 150, 200), "objects": {"Postel": (300, 350, 200, 100)}},
    "Koupelna": {"color": (150, 220, 220), "objects": {"Sprcha": (350, 200, 80, 120)}}
}
current_room = "Obyvak"                                 # výchozí místnost

# vytvoří tlačítka pro přepínání místností
room_buttons = []
x, y = 20, 500                                          # počáteční pozice tlačítek
for room_name in rooms:                                 # pro každou místnost vytvoř tlačítko
    room_buttons.append((room_name, pygame.Rect(x, y, 150, 40)))
    x += 160                                            # posuň další tlačítko doprava

# -------------------- Statistiky mazlíčka --------------------
pet_stats = {                                           # základní hodnoty vlastností
    "hlad": 100,
    "zabava": 100,
    "hygiena": 100,
    "spanek": 100
}
DECAY_RATE = 0.05                                       # rychlost, jakou se statistiky snižují
last_update = time.time()                               # čas poslední aktualizace statistik

# -------------------- Vzhled mazlíčka --------------------
pet_size = 80                                           # velikost mazlíčka
pet_pos = (screen.get_width()//2 - pet_size//2,         # pozice mazlíčka uprostřed obrazovky
           screen.get_height()//2 - pet_size//2)
pet_color = (255, 200, 0)                               # barva mazlíčka (žlutý)
t = 0                                                   # časový ukazatel pro animaci

# -------------------- Pomocné funkce --------------------
def draw_text(text, x, y, fnt=font):
    """Vykreslí text na dané pozici"""
    screen.blit(fnt.render(text, True, (255, 255, 255)), (x, y))

def draw_pet_stats():
    """Vykreslí pruhy se statistikami mazlíčka"""
    x = 150
    y = 20
    for stat, value in pet_stats.items():               # projde všechny vlastnosti mazlíčka
        pygame.draw.rect(screen, (50,50,50), (x, y+20, 100, 10), border_radius=5)      # pozadí pruhu
        pygame.draw.rect(screen, (0,200,0), (x, y+20, int(value), 10), border_radius=5) # aktuální hodnota
        screen.blit(stat_font.render(f"{stat.capitalize()}", True, (255,255,255)), (x, y))
        x += 150

def run_minigame(file_name):
    """Spustí vybranou minihru a načte odměnu z reward.json"""
    global money
    try:
        subprocess.run(["python", file_name])           # spustí externí skript (např. snake.py)
        reward_file = "reward.json"
        if os.path.exists(reward_file):                 # pokud existuje soubor s odměnou
            with open(reward_file, "r") as f:
                data = json.load(f)
            reward = 0
            # zjistí, která hra byla spuštěna
            if "snake" in file_name:
                reward = data.get("snake", 0)
            elif "ball" in file_name:
                reward = data.get("ball", 0)
            elif "reakce" in file_name:
                reward = data.get("reaction", 0)
            money += reward                             # přičte odměnu k penězům
            save_money(money)                           # uloží nové peníze
            with open(reward_file, "w") as f:
                json.dump({}, f)                        # vymaže obsah odměn
    except Exception as e:
        print("Chyba při spuštění hry:", e)

# -------------------- Hlavní smyčka hry --------------------
while True:
    clicked = False                                    # proměnná pro detekci kliknutí
    click_pos = (0,0)

    # -------- Události --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                  # když hráč zavře okno
            save_money(money)                          # uloží peníze
            pygame.quit()                              # ukončí pygame
            sys.exit()                                 # ukončí program
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True                             # kliknutí levým tlačítkem
            click_pos = event.pos                      # uloží pozici kliknutí

    # -------- Snižování statistik --------
    now = time.time()
    delta = now - last_update
    if delta > 1:                                      # každou sekundu
        pet_stats["hlad"] = max(0, pet_stats["hlad"] - DECAY_RATE * 10)
        pet_stats["zabava"] = max(0, pet_stats["zabava"] - DECAY_RATE * 5)
        pet_stats["hygiena"] = max(0, pet_stats["hygiena"] - DECAY_RATE * 3)
        pet_stats["spanek"] = max(0, pet_stats["spanek"] - DECAY_RATE * 2)
        last_update = now

    # -------- Vykreslení pozadí a objektů --------
    screen.fill(rooms[current_room]["color"])          # vyplní pozadí barvou místnosti

    for obj_name, rect_data in rooms[current_room]["objects"].items():
        rect = pygame.Rect(rect_data)                  # vytvoří obdélník objektu
        pygame.draw.rect(screen, (180, 100, 250), rect, border_radius=10)
        pygame.draw.rect(screen, (120,60,200), rect, 3, border_radius=10)
        draw_text(obj_name, rect.x + 5, rect.y + 5, stat_font)

        # reakce na kliknutí na objekt
        if clicked and rect.collidepoint(click_pos):
            pygame.time.wait(150)
            if current_room == "Obyvak" and obj_name == "Konzole":
                game_state = STATE_MINIGAME_MENU
            elif current_room == "Kuchyn" and obj_name == "Lednice":
                pet_stats["hlad"] = min(100, pet_stats["hlad"] + 20)
            elif current_room == "Koupelna" and obj_name == "Sprcha":
                pet_stats["hygiena"] = min(100, pet_stats["hygiena"] + 30)
            elif current_room == "Loznice" and obj_name == "Postel":
                pet_stats["spanek"] = min(100, pet_stats["spanek"] + 30)

    # -------- Tlačítka místností --------
    for name, rect in room_buttons:
        pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
        pygame.draw.rect(screen, (50,50,200), rect, 3, border_radius=10)
        draw_text(name, rect.x + 10, rect.y + 5)
        if clicked and rect.collidepoint(click_pos):
            current_room = name                        # přepne aktuální místnost
            pygame.time.wait(150)

    # -------- Vykreslení mazlíčka --------
    t += 0.1
    dy = int(math.sin(t) * 5)                          # malý sinusový pohyb nahoru a dolů
    pygame.draw.ellipse(screen, pet_color, (pet_pos[0], pet_pos[1] + dy, pet_size, pet_size))

    # -------- Texty nahoře --------
    draw_text(f"💰 {money}", 20, 20)                   # zobrazí počet peněz
    draw_pet_stats()                                   # vykreslí statistiky

    # -------- Menu miniher --------
    if game_state == STATE_MINIGAME_MENU:
        screen.fill((40, 50, 70))
        draw_text("Vyber minihru:", 300, 150)
        buttons = [
            ("🎾 Ball", (300, 250, 200, 50), "ball.py"),
            ("⚡ Reakce", (300, 320, 200, 50), "reakce.py"),
            ("🐍 Snake", (300, 390, 200, 50), "snake.py"),
            ("⬅️ Zpět", (300, 470, 200, 50), None)
        ]
        for label, rect_data, file_name in buttons:
            rect = pygame.Rect(rect_data)
            pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
            pygame.draw.rect(screen, (50,50,200), rect, 3, border_radius=10)
            draw_text(label, rect.x + 30, rect.y + 10)
            if clicked and rect.collidepoint(click_pos):
                pygame.time.wait(150)
                if file_name:
                    run_minigame(file_name)            # spustí vybranou minihru
                game_state = STATE_MAIN                # vrátí se zpět do hlavní hry

    pygame.display.flip()                             # aktualizuje obraz
    clock.tick(30)                                    # omezuje FPS na 30 snímků za sekundu
