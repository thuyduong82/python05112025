import tkinter as tk

def say_hello(label): #command say hello # label jako placeholder promena
    print("Hello!!!")
    label.config(text="Hello!")

def main():
    root = tk.Tk() #základ,zavoláme tk a má funkci Tk

    root.title("Hello?")#nadpis
    root.geometry("800x600")#ukazuje to velikost formátu

    label_example = tk.Label(root, text="Toto je náhodný text", font=("Consolas", 20))#example je promena ktera ukazuje nadpis
    label_example.grid(row=0, column=1) #nahraje to do gui

    btn_example = tk.Button(root, text="klick", command=lambda: say_hello(label_example)) #command jako funkce lambda
    btn_example.grid(row=0, column=1)

    btn_example2 = tk.Button(root, text="klick", command=lambda: say_hello(label_example)) #command jako funkce
    btn_example2.grid(row=0, column=1)

    root.mainloop() #hlavní cyklus

main()
