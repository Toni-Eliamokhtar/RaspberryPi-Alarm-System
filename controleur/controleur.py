class Controleur:
    def __init__(self):
        self.systeme_actif = False
        self.vue = None
        self.platine = None

    def set_vue(self, v):
        self.vue = v

    def set_platine(self, p):
        self.platine = p

    def toggle(self):
        self.systeme_actif = not self.systeme_actif
        self.vue.update_etat(self.systeme_actif)
        self.platine.set_led(self.systeme_actif)
