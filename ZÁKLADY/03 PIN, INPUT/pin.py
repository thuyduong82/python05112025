#pin = int(input("zadeej pin:"))
pokus = 0

#while pin != 1234 or pokus < 2 :#!= znamená nerovná se
#    pin = int(input("zadej pin:"))
#    pokus += 1

#print("správný pin")


while True:
    pin = int(input("Zadej pin:"))
    if pin == 1234:
        print("spravne")
        break
    elif pokus > 1:
        print("moc pokusu")
        break
    print("spatne")
    pokus += 1



