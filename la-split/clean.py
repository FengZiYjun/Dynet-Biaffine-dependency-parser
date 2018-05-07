
filename = "la-ud-dev.conllu"

with open(filename, "r") as f:
    lines = f.readlines()

string = ""
for line in lines:
    if line[0] == "#":
        continue
    string += line

with open(filename+".cl", "w") as f:
    f.write(string)
