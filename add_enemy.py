import json

LOCATION = "enemies/"
enemies = {
    "rat":("Rat", LOCATION+"rat.png", [5], 3),
    "snake":("Snake", LOCATION+"arbok.png", [3, 4, 6], 5),
    "wasp":("Wasp", LOCATION+"beedrill.png", [2, 5, 6], 8),
    "thing":("Thing", LOCATION+"starmie.png", [5, 6, 6], 12),

}

with open('enemies.json', 'w') as f:
    json.dump(enemies, f)
