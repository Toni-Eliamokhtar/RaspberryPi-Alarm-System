from modele.evenement import Evenement


class Controleur:

    def __init__(self):
        self.systeme_actif = False
        self.vue = None
        self.platine = None

    def set_vue(self, v):
        self.vue = v

    def set_platine(self, p):
        self.platine = p

    def init_systeme(self):
        # état initial
        self.platine.set_led(False)
        self.vue.update_etat(False)
        self.vue.update_message("")

    def toggle_systeme(self):
        self.systeme_actif = not self.systeme_actif

        self.platine.set_led(self.systeme_actif)

        if self.systeme_actif:
            self.vue.update_message("Système activé")
            e = Evenement("Activation", {})
        else:
            self.vue.update_message("Système désactivé")
            e = Evenement("Désactivation", {})

        self.vue.ajouter_event(e)
        self.vue.update_etat(self.systeme_actif)

    def mouvement(self):
        self.vue.update_message("MOUVEMENT DETECTÉ")
        e = Evenement("Mouvement détecté", {})
        self.vue.ajouter_event(e)
        self.platine.bip(0.3)
