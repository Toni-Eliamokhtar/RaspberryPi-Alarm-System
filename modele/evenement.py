from datetime import datetime


class Evenement:
    def __init__(self, type_evenement, donnee):
        self.dateHeureEvenement = datetime.now()
        self.typeEvenement = type_evenement
        self.donneeEvenement = donnee

    def __repr__(self):
        return f"{self.dateHeureEvenement.strftime('%H:%M:%S')} - {self.typeEvenement}"
