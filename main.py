import requests
import os,sys
from PyQt5 import QtWidgets
from main_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore, QtWidgets
import json

repo1_owner = 'Dymerz'
repo1_name = 'StarCitizen-Localization'
repo1_directory_path = 'data/Localization/french_(france)'  # Chemin du répertoire dans le repo

raw_url="https://raw.githubusercontent.com/Dymerz/StarCitizen-Localization/refs/heads/main/data/Localization/french_(france)/global.ini"

nom_fichier_local="global.ini"

#repertoire a ajouter
path_add ="/data/Localization/french_(france)/"

#bordel pour teste
data_repo = {
    "Commit_sha": "Bonjour",
    "Commit_Message": "va1r",
    "Commit_Date": "var2"
}

def get_commits_infos(repo_owner, repo_name, directory_path):
    # API URL
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    params = {'path': directory_path,'per_page': 1}

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            data_repo["Commit_Date"]=commit['commit']['author']['date'] 
            data_repo["Commit_Message"]=commit['commit']['message']
            data_repo["Commit_sha"]=commit['sha']

            return data_repo
    else:
        print(f"Erreur : {response.status_code} - {response.text}")

def dl_file_from_git(raw_url, fichier_local):
    # Envoie la requête pour obtenir le contenu brut du fichier
    response = requests.get(raw_url)
    
    if response.status_code == 200:
        # Ouvre un fichier en mode écriture binaire (wb) et sauvegarde le contenu téléchargé
        print("Telechargement de la Mise à jour")
        with open(fichier_local, 'wb') as file:
            file.write(response.content)
        print(f"Fichier téléchargé et sauvegardé sous : {fichier_local}")
    else:
        print(f"Erreur lors du téléchargement : {response.status_code}")
        

def json_write(path_file,data):#crée le json 

    with open(path_file+"/Version_trad.json", "w") as file:
        json.dump(data, file, indent=4)
        
    with open(path_file+"/user.cfg", "w") as fichier:
        fichier.write("g_language = french_(france)") #ecriture du User.cfg
   
def json_read(path_file):

    with open(path_file+"/Version_trad.json", "r") as file:
        return json.load(file)   
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.Choix_trad.addItems(["Choix 1", "Choix 2", "Choix 3", "Choix 4", "Choix 5"]) #l'objecty est la mais pas implementé
        self.ui.selecte_path.clicked.connect(self.on_selecte_path)
        self.ui.Startinstall.clicked.connect(self.on_start_install)
        self.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("Merci de Choisir le repertoire d'installation de SC /LIVE ou / PTU")))

        #variables local
        self.repertoire="None"
        

    def on_selecte_path(self): # Selection du repertoire d'install de SC 
        
        print("Sélection de répertoire cliquée.")
        # Ouvre la boîte de dialogue pour parcourir les fichiers
 
        self.repertoire = QFileDialog.getExistingDirectory(self, "Sélectionner un répertoire", "") #afficher la windows de selection

        
        if self.repertoire!="":
            _translate = QtCore.QCoreApplication.translate

            self.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format(self.repertoire)))
            
            print("Répertoire sélectionné :", self.repertoire,"|")
        else:
            print("Aucun fichier sélectionné.")

    def on_start_install(self):
        _translate = QtCore.QCoreApplication.translate    
        
        if self.repertoire!="": #verification que l'utilisateur a bien selectionner un repertoire
            install(self.repertoire)
        else:
            print("selectionne le repertoire")
            self.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("!!!! Selectione le repertoire d'installation de SC !!!!")))

def path_check_gen(chemin):

    if not os.path.exists(chemin):
   
        os.makedirs(chemin)

    else:
        print(f"Le dossier {chemin} existe déjà.")

def install(path_sc):
    
    _translate = QtCore.QCoreApplication.translate
    path_check_gen(path_sc+path_add)#Crée les repertoires
    
    if os.path.isfile(path_sc+"/Version_trad.json"):#verification de la presence du Json
        print("le Json est bien la")
        try:
            data_json=json_read(path_sc) #lecture du json Local
        except:
            print("Merci de suprimer les fichier Json dans:", path_sc)#Je json n'est pas lisible
            data_repo=get_commits_infos(repo1_owner, repo1_name, repo1_directory_path)
            #json_write(path_sc,data_repo)#voir pour faire une install en cas d'effacemen du Json
            
        try:
            data_repo=get_commits_infos(repo1_owner, repo1_name, repo1_directory_path) #recuperation des infos du repo
        #print("Data Json :",data_json,"Data Repo :",data_repo)
        except:
            print("Pas de reponce de L'API")
        
        
        if data_repo== data_json: #Verification de la version
            print("pas de MAJ a faire")
            window.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("Version Deja à jour")))
        else:
            
            window.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("Telechargement de la Mise a jour ")))
            dl_file_from_git(raw_url,path_sc+path_add+nom_fichier_local)
            window.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("Mise a jour installer ")))
            json_write(path_sc,data_repo) #save du Json 
        
        
    else:
        print("Il est ou Json ")
        data_repo=get_commits_infos(repo1_owner, repo1_name, repo1_directory_path)
        window.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("Telechargement de la Mise a jour ")))
        dl_file_from_git(raw_url,path_sc+path_add+nom_fichier_local)
        window.ui.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{}</span></p></body></html>".format("Mise a jour installer ")))
        json_write(path_sc,data_repo) #save du Json 


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
    