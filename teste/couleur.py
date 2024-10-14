import pyautogui
from PIL import ImageGrab
import time

def get_pixel_color():
    try:
        while True:
            # Récupérer la position actuelle de la souris
            x, y = pyautogui.position()
            
            # Prendre une capture d'écran
            screenshot = ImageGrab.grab()
            
            # Obtenir la couleur du pixel à la position de la souris
            pixel_color = screenshot.getpixel((x, y))
            
            # Afficher la couleur en RGB
            print(f"Position: ({x}, {y}), Couleur: RGB{pixel_color}")
            
            # Attendre un peu avant de mettre à jour
            time.sleep(1)

    except KeyboardInterrupt:
        print("Arrêt du programme.")

if __name__ == "__main__":
    print("Appuyez sur Ctrl+C pour arrêter le programme.")
    get_pixel_color()