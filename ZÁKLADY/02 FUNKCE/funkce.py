def ukazka():
    print("ahoj")

ukazka()#bez parametru

def pozdrav(n):#s parametrem
    print(n)

pozdrav(17)

def funkce_animal(n):
    n = int(n)
    for ovce in range(n):
        print(ovce,"ovce")
    print("pes")

x = input("Kolik ovci:")
funkce_animal(x)




def hej_rup(m):
    for x in range(m):
        print(x,"hejrup")
        print("rup")
hej_rup(7)



def vypis_cisla(n):
    n = int(n)
    for cislo in range(n):
        if cislo == 13:
            continue
        print(cislo)
        
b = input("do kolika:")
vypis_cisla(b)




def zigzag(n):
    for cislo in range(n):
        if cislo%2:
            print(" ",cislo)

x = input("kolik zigzag?")
zigzag(x)
    

