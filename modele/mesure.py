# modele/mesure.py
from datetime import datetime

class Mesure:
    def __init__(self, valeurCapteur):

        # valeurCapteur : bool/int — valeur lue du capteur PIR (1 = mouvement, 0 = rien)
        
        self.dateHeureMesure = datetime.now()
        self.valeurCapteur   = valeurCapteur

    def __repr__(self):
        date_str = self.dateHeureMesure.strftime("%Y-%m-%d %H:%M:%S")
        return f"{date_str} - PIR: {self.valeurCapteur}"