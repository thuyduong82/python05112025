import datetime as dt

now = dt.datetime.now ()

# print(now)      #printne čas
# print(now.second)#printne jen sekundy
# print(now.minute)#printne jen minuty
# print(now.day)#printne jen den
# print(now.month)#printne jen měsíc
# print(now.year)#printne jen rok

# delta = dt.timedelta() 
# print("delta je", delta)

print("teď je" , now)
minus10 = now - dt.timedelta(minutes=10)#odečte od času 10minut
print(minus10)

new_time = dt.datetime(2024,11,14,14,15,0,0)
how_long_till_break = new_time - now
print("přestávka je za", how_long_till_break)