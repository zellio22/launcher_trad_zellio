import json

# Variables à sauvegarder
var1 = "Bonjour"
var2 = 42
var3 = "hello"

# Dictionnaire contenant les variables
data = {
    "variable_1": var1,
    "variable_2": var2,
    "variable_3": var3
}

# Sauvegarde des données dans un fichier JSON avec une indentation de 4 espaces
with open("variables.json", "w") as file:
    json.dump(data, file, indent=4)

print("Variables sauvegardées avec succès dans variables.json")


# Chargement des données depuis le fichier JSON
with open("variables.json", "r") as file:
    data = json.load(file)

# Accéder aux variables
var1 = data["variable_1"]
var2 = data["variable_2"]
var3 = data["variable_3"]

print("Variables chargées :", var1, var2, var3)


