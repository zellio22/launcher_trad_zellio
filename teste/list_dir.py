import os
def path_check_geng(chemin):

    if not os.path.exists(chemin):
   
        os.makedirs(chemin)
        print(f"Le dossier {chemin} a été créé.")
    else:
        print(f"Le dossier {chemin} existe déjà.")
