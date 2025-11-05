import json

path = "data.json"

animal = {
    "Name":"Hugo",
    "Type": "elephant",
    "Height": "tall"
}

with open(path, mode="w") as file:
    json.dump(animal, file, indent=2) #indent -> odsazení 


with open(path, mode="r") as file:
     data = json.load(file)

print(data)