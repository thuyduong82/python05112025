krestni_jmeno = "Hugo" #nemusíme mít let pro proměnou,snakecase

cislo = 5

pravda = True #velký písmeno true

seznam_studentu = ["Emil","Emilie","Jarmila","Jarmil","Hvězdoň"]

print(krestni_jmeno)#místo console.log máme print

def nahodna_funkce ():#funkce je def
    print("funguje")#v pythonu musíme pouivat spravne odsazeni rika to ze to co je odsazeny patri do te funkce

nahodna_funkce()

if cislo < 0:#důležité správně odsazovat
    print("číslo je záporné")
elif cislo > 0:
    print("číslo je kladné")    
else:
    print("číslo je 0")

pocitadlo = 1

while pocitadlo < 11:
    print(pocitadlo)
    pocitadlo+=1#v javascript máme pocitadlo++, ale v pythonu musíme mít pocitadlo+=


for x in range(0, 11, 1):#od kolika,do kolika,po kolika viz 1 2 3 4...
    print(x)

for student in seznam_studentu:
    print(student)