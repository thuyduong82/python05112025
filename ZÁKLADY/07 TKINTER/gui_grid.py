import tkinter as tk

root = tk.Tk()

for x in range(3):
    root.grid_rowconfigure(x, weight=1)
    root.grid_columnconfigure(x, weight=1)

label = tk.Label(root, text="Down right", bg="green")
label.grid(row=1, column=1)

root.mainloop()