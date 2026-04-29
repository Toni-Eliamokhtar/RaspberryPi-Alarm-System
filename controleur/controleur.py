class Controleur:
    def __init__(self):
        self.systeme_actif = False
        self.vue = None

    def set_vue(self, v):
        self.vue = v

    def toggle(self):
        self.systeme_actif = not self.systeme_actif
        self.vue.update_etat(self.systeme_actif)
