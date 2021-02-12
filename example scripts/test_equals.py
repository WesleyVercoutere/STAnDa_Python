

string1 = "test"
string2 = "test"
string3 = "Test"

stringArray = [string1, string2, string3]

print(string1 == string2)
print(string1 is string2)

print(string1 == string3)
print(string1 is string3)

print(string1 == stringArray[0])
print(string1 is stringArray[0])

print(string1 == stringArray[1])
print(string1 is stringArray[1])