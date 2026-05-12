from modele.evenement import Evenement


class Controleur:

    def __init__(self):

        # Initialise / fait référence à la VUE et PLATINE
        
        self.vue = None
        self.platine = None


        # État du système

        self.systeme_actif  = False   # système activé ou non
        self.attente_code   = False   # en attente de saisie du code
        self.acces_bloque   = False   # accès bloqué après 3 tentatives


        # Gestion du code
        self.code_saisi    = ""       # touches accumulées du keypad
        self.code_valide   = "1234"   # code d'accès par défaut
        self.tentatives    = 0        # nombre de tentatives échouées
        self.MAX_TENTATIVES = 3       # maximum de tentatives permises


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
