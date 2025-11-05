def hello():
    print("Hello!")

def plus10(x):
    print(x+10)

a = lambda x : x+10 #anonymni funkce lambda a tu ulozime pod nejakou promenou
b = lambda : print("hello")

print(a(20))

b()