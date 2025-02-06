import json

LOCATION = "enemies/"
enemies = {
    "rat":("Крыса", LOCATION+"rat.gif", [1], 3),
    "snake":("Змея", LOCATION+"snake.gif", [3, 4, 6], 5),
    "wasp":("Оса", LOCATION+"wasp.gif", [2, 5, 6], 8),
    "thing":("Нечто", LOCATION+"thing.gif", [5, 6, 6], 12),
    "ork":("Орк", LOCATION+"ork.png", [3, 4], 6),
    "dog":("Гончая", LOCATION+'dog.gif', [1, 2, 3], 3),
    "bat":("Летучая мышь", LOCATION+"bat.gif", [2], 2),
    "golem":("Голем", LOCATION+"golem.gif", [4, 5], 4),
    "ghost":("Призрак", LOCATION+"ghost.gif", [1, 1], 2),
    "bug":("Жук", LOCATION+"bug.gif", [3], 3),
    "hourse":("Огненная кобыла", LOCATION+"hourse.gif", [4, 5], 5),

}

with open('../enemies.json', 'w') as f:
    json.dump(enemies, f)
