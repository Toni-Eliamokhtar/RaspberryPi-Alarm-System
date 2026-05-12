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
        # État initial : LED rouge allumée, LCD vide, système désactivé
        self.platine.set_led(False)
        self.platine.lcd_effacer()
        self.vue.update_etat(False)


    # Méthodes de contrôle du système (Toggle, bouton bleu)

    def toggle_systeme(self):

        # Démarre ou arrête le système selon son état actuel

        if self.acces_bloque:
            # si bloqué, le bouton bleu débloque et désactive
            self.acces_bloque  = False
            self.attente_code  = False
            self.tentatives    = 0
            self.code_saisi    = ""
            self.systeme_actif = False
            self.platine.set_led(False)
            self.platine.lcd_afficher("Systeme", "desactive")
            self.vue.update_etat(False)
            e = Evenement(
                "Désactivation du système d'alarme",
                {"capteur": "N/A", "code": "N/A"}
            )
            self.vue.ajouter_event(e)

        elif self.systeme_actif:
            # arrêt normal du système
            self.systeme_actif = False
            self.attente_code  = False
            self.tentatives    = 0
            self.code_saisi    = ""
            self.platine.set_led(False)
            self.platine.lcd_afficher("Systeme", "desactive")
            self.vue.update_etat(False)
            e = Evenement(
                "Désactivation du système d'alarme",
                {"capteur": "N/A", "code": "N/A"}
            )
            self.vue.ajouter_event(e)

        else:
            # démarrage du système
            self.systeme_actif = True
            self.attente_code  = False
            self.tentatives    = 0
            self.code_saisi    = ""
            self.platine.set_led(True)
            self.platine.lcd_afficher("Systeme", "active")
            self.vue.update_etat(True)
            e = Evenement(
                "Activation du système d'alarme",
                {"capteur": "N/A", "code": "N/A"}
            )
            self.vue.ajouter_event(e)


    # Mouvement

    def mouvement_detecte(self):
        # Réagit à une détection PIR : demande le code d'accès
        if self.systeme_actif and not self.attente_code and not self.acces_bloque:
            self.attente_code = True
            self.code_saisi   = ""
            self.platine.lcd_afficher("Mouvement!", "Entrez code:")
