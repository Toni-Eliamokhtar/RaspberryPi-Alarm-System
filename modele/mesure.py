from datetime import datetime

class Mesure:
    def __init__(self, valeurCapteur):
        self.dateHeureMesure  = datetime.now()
        self.donneeEvenement  = {"capteur": str(valeurCapteur), "code": ""}

    def __repr__(self):
        date_str = self.dateHeureMesure.strftime("%Y-%m-%d %H:%M:%S")
        return f"{date_str} - PIR: {self.donneeEvenement.get('capteur')}"