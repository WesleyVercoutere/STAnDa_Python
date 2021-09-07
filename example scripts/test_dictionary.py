data = dict()

data["Turtle"] = dict()
data["Turtle"]["total"] = 200
data["Turtle"][10] = 150
data["Turtle"][20] = 100



print(data)

for i in data:

    for j in data[i]:

        print(i, j, data[i][j])