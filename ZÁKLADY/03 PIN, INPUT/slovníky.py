#..student" (key jako cislo v array) alice (value)
#neco jako array seznam ale misto cislo hotnboty je nejake slovo

ukazka = {
    "student":"Alice",
    "učitel":"Bob",
    "školník":"Charlie"
}

#print(ukazka["učitel"])

cat = {
    "name":"Mikesh",
    "age":"7",
    "color":"purpleblack",
    "fav_food":"lasagna",
    "alive":True,
    "friends":["Dragon", "Jerry"],
}



print(cat["friends"][1])

leva_cast = "TOHLE JE ZPUSOB JAK VYPSAT LEVOU CAST KEY"

for key in cat:
    print(key)#vypise key coz je leva cast

prava_cast1 = "PRVNI ZPUSOB JAK VYPSAT PRAVOU CAST VALUE"

print(prava_cast1)

for key in cat:#vypise pravou cast value
    print(cat[key])#1.kolo cat["name"] 2.kolo cat["age"]

prava_cast2 = "DRUHY ZPUSOB JAK VYPSAT PRAVOU CAST VALUE"

print(prava_cast2)

#2. zpusob jak napsat pravou cast 
for value in cat.values():
    print(value)#tohle vypise pravou cast coz je ten value

prava_cast3 = "TRETI ZPUSOB JAK VYPSAT PRAVOU CAST VALUE"

print(prava_cast3)

#3. cast pro vypsani value
for key, value in cat.items():
    print(f"tohle je {key}, tohle je {value}")



for friend in cat["friends"]:
    print(friend)


cat["fav_food"] = "mouse"#prepsali jsme mikeshovo oblibeny jidlo

print(cat)

if "fav_food" in cat:
    print(cat["fav_food"])#tady kontrolujeme jestli nse tam ten key nachazi

cat["number of legs"] = 4 #pripsali jsme hodnotu do seznamu

print(cat)