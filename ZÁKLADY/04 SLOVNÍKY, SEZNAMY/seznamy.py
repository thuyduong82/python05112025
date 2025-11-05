names = [ #list of names
    "Alice", "Bob", "Charlie", "Diana", "Ethan",
    "Fiona", "George", "Hannah", "Isaac", "Julia",
    "Kevin", "Laura", "Mike", "Nina", "Oliver",
    "Paula", "Quincy", "Rachel", "Sam", "Tina"
]

print(names[3])#vypis jmeno dianu

#for name in names:
#    print(name)#vypis seznam


for i, name in enumerate(names):#enumarate rika pridat si cislo, i index
    print(f"{i+1}. {name}")#do slozenych zavorek se dat i matematicka operace