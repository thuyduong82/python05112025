path = "data.txt"

# "w" -> write. "a" -> append, "r" -> read
# with open(path, "w") as file:
#     file.writelines("bye")ˇ

with open(path, "r") as file:
    content = file.read()
    print(content)

