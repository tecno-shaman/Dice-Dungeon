import json

with open("enemies.json", 'r') as file:
    dict = json.load(file)
    print(dict)