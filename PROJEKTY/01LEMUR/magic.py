import sys
import datetime as dt
import json
import tkinter as tk

def load_game():#stahnout data
    global lemur
    global path
    load_data = {}#stahnou data do prazdneho dictionary#
    with open(path, mode="r") as file: #čteme json file a z něj všechno stahujem do prazdneho dictionary#
        load_data = json.load(file)#chci kontrolovat jestli jsou data v slovniku,protoze jsem mohl udelat chybu a nesavenout nic do dat, proto tam je ta funkce-> nactu data a zkontroluju jestli data jsou prazdny #
    if len(load_data) != 0:#if len je jako lenght funkce, jestli se nerovna lenght nule muzeme do muzeme hodit z load_data do promeny lemur#
        lemur = load_data
    else: #v pripade ze json soubor je prazny, dáváme základní hodnoty samy#
        lemur = { 
            'name': "Mortimer The III.",
            "color": "purpleblack",
            'health': 100,
            'hunger': 50,
            'thirst': 0,
            'cleanliness': 100,
            'energy': 90,
            'happiness': True,
            'alive': True,
        }



def check_time():
    global original_time

    # TODO: finish instructions,(jsou videt poznamky)
original_time = dt.datetime.now()

def check_time():
    global original_time
    current_time = dt.datetime.now()
    if current_time > original_time + dt.timedelta(minutes=30):
        lemur['hunger'] += 10
        print(f"{lemur['name']} is getting hungry...")
        original_time = current_time


def feeding():
    print()

    lemur['hunger'] -= 30 #-=odecita
    if lemur['hunger'] < 0:
         lemur['alive'] = False

def display_lemur_status():
    print()
    print("How is lemur doing? Press H to know: ")

    for key, value in lemur.items():
        print(f"{key}: {value}")


def display_attribute(attribute): #parametr
    if attribute not in lemur:
        print(f"Lemur doesn't have {attribute}")
    else:
        print(f"Current {attribute} is: {lemur[attribute]}")

def game():
    print()#prazdny radek
    print(f"you've played fetch with {lemur['name']}. {lemur['name']} looks happy.")
    # wanna_game.lower() == "g"

    lemur['energy'] -= 25
    lemur['hunger'] += 10
    lemur['cleanliness'] -= 25
    if lemur['happiness'] == False:
        lemur['happiness'] = True

    print(f"Happines: {lemur['happiness']}")
    print(f"Energy: {lemur['energy']}")
    
def bathing():
    print(f"{lemur['name']} loves baths. {lemur['name']} is clean now")
    lemur['cleanliness'] = 100


def sleeping():
    print(f"{lemur['name']} has slept for 12 hours.")
    lemur['energy'] = 100
    lemur['happiness'] = True


def check_lemur_conditions():
    if lemur['energy'] < 30:
        print("Go to sleep!")

    if lemur['alive'] == False:
        print("Lemur died")
        sys.exit()
    
    if lemur['cleanliness'] < 30:
        print(f"{lemur['name']} kinda stinks...take a bath!")
path = "lemur.json"     

def save_game():
    with open(path, mode="w") as file:
        json.dump(lemur, file, indent=2) 

lemur = {
    'name': "Mortimer The III.",
    "color": "purpleblack",
    'health': 100,
    'hunger': 50,
    'thirst': 0,
    'cleanliness': 100,
    'energy': 90,
    'happiness': True,
    'alive': True,
}


def main():
    load_game()

    root = tk.Tk()

    root.title("Lemur game")
    root.geometry("1000x1000")

    otazka = tk.Label(root, text="Co chce Lemur dělat?", font=("Arial", 30), bg="pink")
    otazka.grid(row=1, column=2)

    for x in range(5):
        root.grid_rowconfigure(x, weight=1)
        root.grid_columnconfigure(x, weight=1)

    root.mainloop()



            




    


if __name__ == "__main__":
    main()#zde spouštíme hlavní funkci,to je úplně na konci







