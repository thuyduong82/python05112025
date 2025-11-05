import csv

path = "data.csv"

seznam = ["Amísek", "Dumit", "Adam"]

# with open(path, "w", encoding="utf-8") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(seznam)

# with open(path, "r", encoding="utf-8") as file:
#     reader = csv.reader(file, delimiter=";")
#     for row in reader:
#         print(row)

students = [  
    {"Name": "Amísek","School": "Třebešín","Fav_color": "blue"},
     {"Name": "Dumit","School": "Oxford","Fav_color": "green"}
]


with open(path, "w", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "School", "Fav_color"], delimiter=";")

    writer.writeheader()

    writer.writerows(students)
