class Car:#nejaky charakter car
    def __init__(self, color, name, wheel_count):#self se vzdycky dava a pak nejke parametry
        self.color = color
        self.name = name
        self.wheel_count = wheel_count #pocet kol auta
        self.has_steering_wheel = True #ma volant
        self.stick = "manual"
    
    def honk(self):#dava do funkce self 
        print(f"{self.name} Tůů tůůt")#svoje jmeno tuu tuut
    
    def open_door(self, door):#vkladam do funkce self a door
        print(f"{door} door is open")


porsche = Car("red", "911", 5)

print(porsche.stick)
porsche.honk()
porsche.open_door("front")

lambo = Car("yellow", "huracan", 4)
lambo.honk()


class Future_car(Car):#trida future_car podtřída car, dědí vlastnosti car
    def __init__(self, color, name, wheel_count, rockets):
        super().__init__(color, name, wheel_count)#Volá konstruktor Car a nastaví základní atributy
        self.rockets = rockets #nový atribut raktey
        self.has_steering_wheel = False #nema volant
        self.stick = "automatic"
    
    def firework(self):
        print(f"{self.name} fires {self.rockets} rockets")

multipla_v2 = Future_car("blue", "Multipla", 7, 12)

print(multipla_v2.color) #printuje barvu multipla
multipla_v2.honk() #dědí funkci honk() z podtřídy car

multipla_v2.firework()