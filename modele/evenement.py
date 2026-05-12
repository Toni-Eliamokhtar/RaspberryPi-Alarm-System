# modele/evenement.py
from datetime import datetime

class Evenement:
    def __init__(self, typeEvenement, donneeEvenement):
        """
        typeEvenement  : str  — l'un des 4 types définis dans l'énoncé ->
            Activation du système d’alarme, Désactivation du système d’alarme, Accès
            valide du système d’alarme, Accès invalide du système d’alarme
        
        donneeEvenement: doit être un dictionnaire — ex: {"capteur": "Mouvement détecté", "code": "1234"}
        """
        self.dateHeureEvenement = datetime.now()
        self.typeEvenement      = typeEvenement
        self.donneeEvenement    = donneeEvenement  # doit être un dictionnaire

    def __repr__(self):
        date_str = self.dateHeureEvenement.strftime("%Y-%m-%d %H:%M:%S")
        return f"{date_str} - {self.typeEvenement}"