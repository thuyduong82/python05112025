import pygame
import sys
import subprocess
import os
import json
import time
import math

# ---------------- Inicializace ----------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Virtuální mazlíček")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
stat_font = pygame.font.Font(None, 28)

# ---------------- Herní stavy ----------------
STATE_MAIN = "main"
STATE_MINIGAME_MENU = "minigame_menu"
game_state = STATE_MAIN

# ---------------- Trvalé penízky ----------------
SAVE_FILE = "save.json"

def load_money():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            return data.get("money", 0)
        except:
            return 0
    return 0

def save_money(amount):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"money": amount}, f)
    except Exception as e:
        print("Chyba při ukládání penízků:", e)

money = load_money()

# ---------------- Pokoje a objekty ----------------
rooms = {
    "Obývák": {"color": (150, 200, 255), "objects": {"Konzole": (600, 300, 120, 70)}},
    "Kuchyň": {"color": (200, 180, 150), "objects": {"Lednice": (100, 200, 80, 120)}},
    "Ložnice": {"color": (180, 150, 200), "objects": {"Postel": (300, 350, 200, 100)}},
    "Koupelna": {"color": (150, 220, 220), "objects": {"Sprcha": (350, 200, 80, 120)}}
}
current_room = "Obývák"

room_buttons = []
x, y = 20, 500
for room_name in rooms:
    room_buttons.append((room_name, pygame.Rect(x, y, 150, 40)))
    x += 160

# ---------------- Vlastnosti mazlíčka ----------------
pet_stats = {
    "hlad": 100,
    "zabava": 100,
    "hygiena": 100,
    "spanek": 100
}
DECAY_RATE = 0.05
last_update = time.time()

# ---------------- Animovaný mazlíček ----------------
pet_size = 80
pet_pos = (screen.get_width()//2 - pet_size//2, screen.get_height()//2 - pet_size//2)
pet_color = (255, 200, 0)
t = 0  # čas pro animaci

# ---------------- Pomocné funkce ----------------
def draw_text(text, x, y, fnt=font):
    screen.blit(fnt.render(text, True, (255, 255, 255)), (x, y))

def draw_pet_stats():
    x = 150
    y = 20
    for stat, value in pet_stats.items():
        # pozadí pruhu
        pygame.draw.rect(screen, (50,50,50), (x, y+20, 100, 10), border_radius=5)
        # aktuální stav
        pygame.draw.rect(screen, (0,200,0), (x, y+20, int(value), 10), border_radius=5)
        screen.blit(stat_font.render(f"{stat.capitalize()}", True, (255,255,255)), (x, y))
        x += 150

def run_minigame(file_name):
    global money
    try:
        subprocess.run(["python", file_name])
        reward_file = "reward.json"
        if os.path.exists(reward_file):
            with open(reward_file, "r") as f:
                data = json.load(f)
            reward = 0
            if "snake" in file_name:
                reward = data.get("snake", 0)
            elif "ball" in file_name:
                reward = data.get("ball", 0)
            elif "reakce" in file_name:
                reward = data.get("reaction", 0)
            money += reward
            save_money(money)
            with open(reward_file, "w") as f:
                json.dump({}, f)
    except Exception as e:
        print("Chyba při spouštění hry:", e)

# ---------------- Hlavní smyčka ----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_money(money)
            pygame.quit()
            sys.exit()

    # --- Pokles vlastností mazlíčka ---
    now = time.time()
    delta = now - last_update
    if delta > 1:
        pet_stats["hlad"] = max(0, pet_stats["hlad"] - DECAY_RATE * 10)
        pet_stats["zabava"] = max(0, pet_stats["zabava"] - DECAY_RATE * 5)
        pet_stats["hygiena"] = max(0, pet_stats["hygiena"] - DECAY_RATE * 3)
        pet_stats["spanek"] = max(0, pet_stats["spanek"] - DECAY_RATE * 2)
        last_update = now

    # --- Vykreslení aktuálního pokoje ---
    screen.fill(rooms[current_room]["color"])

    # objekty
    for obj_name, rect_data in rooms[current_room]["objects"].items():
        rect = pygame.Rect(rect_data)
        pygame.draw.rect(screen, (180, 100, 250), rect, border_radius=10)
        pygame.draw.rect(screen, (120,60,200), rect, 3, border_radius=10)
        draw_text(obj_name, rect.x + 5, rect.y + 5, stat_font)

        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if rect.collidepoint(mx, my):
                pygame.time.wait(150)
                if current_room == "Obývák" and obj_name == "Konzole":
                    game_state = STATE_MINIGAME_MENU
                elif current_room == "Kuchyň" and obj_name == "Lednice":
                    pet_stats["hlad"] = min(100, pet_stats["hlad"] + 20)
                elif current_room == "Koupelna" and obj_name == "Sprcha":
                    pet_stats["hygiena"] = min(100, pet_stats["hygiena"] + 30)
                elif current_room == "Ložnice" and obj_name == "Postel":
                    pet_stats["spanek"] = min(100, pet_stats["spanek"] + 30)

    # tlačítka na přepínání pokojů
    for name, rect in room_buttons:
        pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
        pygame.draw.rect(screen, (50,50,200), rect, 3, border_radius=10)
        draw_text(name, rect.x + 10, rect.y + 5)
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if rect.collidepoint(mx, my):
                current_room = name
                pygame.time.wait(150)

    # --- Penízky ---
    draw_text(f"💰 {money}", 20, 20)

    # --- Vlastnosti mazlíčka ---
    draw_pet_stats()

    # --- Animovaný mazlíček ---
    t += 0.1
    dy = int(math.sin(t) * 5)
    pygame.draw.ellipse(screen, pet_color, (pet_pos[0], pet_pos[1] + dy, pet_size, pet_size))

    # --- Menu miniher ---
    if game_state == "minigame_menu":
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
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()):
                pygame.time.wait(150)
                if file_name:
                    run_minigame(file_name)
                game_state = STATE_MAIN

    pygame.display.flip()
    clock.tick(30)
