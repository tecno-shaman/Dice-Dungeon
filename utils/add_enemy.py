import json

LOCATION = "spritesheets/"
EXTENSION = ".png"
enemies = {
    "rat": ("Крыса", LOCATION + "rat" + EXTENSION, [1], 2),
    "snake": ("Змея", LOCATION + "snake" + EXTENSION, [3, 4, 6], 5),
    "wasp": ("Оса", LOCATION + "wasp" + EXTENSION, [2, 5, 6], 7),
    "thing": ("Нечто", LOCATION + "thing" + EXTENSION, [5, 6, 6], 10),
    "dog": ("Гончая", LOCATION + "dog" + EXTENSION, [1, 2, 3], 4),
    "bat": ("Летучая мышь", LOCATION + "bat" + EXTENSION, [2, 2], 2),
    "golem": ("Голем", LOCATION + "golem" + EXTENSION, [4, 5], 4),
    "ghost": ("Призрак", LOCATION + "ghost" + EXTENSION, [1, 2], 2),
    "bug": ("Жук", LOCATION + "bug" + EXTENSION, [3], 2),
    "hourse": ("Огненная кобыла", LOCATION + "hourse" + EXTENSION, [4, 5], 5),
}

with open('../enemies.json', 'w') as f:
    json.dump(enemies, f)
