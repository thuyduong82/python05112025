import sqlite3
#vytvoř spojení s databází


#vytvor spojeni s databazi
connection = sqlite3.connect("game.db")

#vytvoreni kurzoru, ktery nam umoznuje navigaco po databazi
cursor = connection.cursor()

#zapis do db

user_input = input("přidej postavičku do databáze:")
user_input2 = input("pridej class:")

cursor.execute("INSERT INTO characters (name,class) VALUES (?,?)",(user_input,user_input2))

cursor.execute("SELECT * FROM characters")
data = cursor.fetchall()


#potvrzeni vlozeni dat do db
connection.commit()

cursor.execute("SELECT * FROM characters")
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()