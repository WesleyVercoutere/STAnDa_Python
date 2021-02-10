

idSet = set()

prefix = "26134."

for i in range(15):
    machineId = f"{prefix}{i+1}"
    idSet.add(machineId)

print("Set")
for id in idSet:
    print(id)

idSet = sorted(idSet)

print()
print("Ordered list")
for id in idSet:
    print(id)

# print(idSet)