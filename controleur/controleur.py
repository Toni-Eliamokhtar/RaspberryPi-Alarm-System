from modele.evenement import Evenement
from modele.mesure import Mesure
from modele.gestionnaireBD import GestionnaireBD


class Controleur:

    def __init__(self):

        # Initialise / fait référence à la VUE et PLATINE

        self.vue = None
        self.platine = None

        # Gestionnaire de base de données
        self.bd = GestionnaireBD()

        # État du système

        self.systeme_actif = False  # système activé ou non
        self.attente_code = False  # en attente de saisie du code
        self.acces_bloque = False  # accès bloqué après 3 tentatives

        # Gestion du code
        self.code_saisi = ""  # touches accumulées du keypad
        self.code_valide = "1234"  # code d'accès par défaut
        self.tentatives = 0  # nombre de tentatives échouées
        self.MAX_TENTATIVES = 3  # maximum de tentatives permises

        # Liste des nouveaux événements non encore sauvegardés
        self.nouveaux_evenements = []

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
            self.acces_bloque = False
            self.attente_code = False
            self.tentatives = 0
            self.code_saisi = ""
            self.systeme_actif = False
            self.platine.set_led(False)
            self.platine.lcd_afficher("Systeme", "desactive")
            self.vue.update_etat(False)
            e = Evenement(
                "Désactivation du système d'alarme", {"capteur": "N/A", "code": "N/A"}
            )
            self.nouveaux_evenements.append(e)
            self.vue.ajouter_event(e)

        elif self.systeme_actif:
            # arrêt normal du système
            self.systeme_actif = False
            self.attente_code = False
            self.tentatives = 0
            self.code_saisi = ""
            self.platine.set_led(False)
            self.platine.lcd_afficher("Systeme", "desactive")
            self.vue.update_etat(False)
            e = Evenement(
                "Désactivation du système d'alarme", {"capteur": "N/A", "code": "N/A"}
            )
            self.nouveaux_evenements.append(e)
            self.vue.ajouter_event(e)

        else:
            # démarrage du système
            self.systeme_actif = True
            self.attente_code = False
            self.tentatives = 0
            self.code_saisi = ""
            self.platine.set_led(True)
            self.platine.lcd_afficher("Systeme", "active")
            self.vue.update_etat(True)
            e = Evenement(
                "Activation du système d'alarme", {"capteur": "N/A", "code": "N/A"}
            )
            self.nouveaux_evenements.append(e)
            self.vue.ajouter_event(e)

    # Mouvement

    def mouvement_detecte(self):
        # Réagit à une détection PIR : demande le code d'accès
        if self.systeme_actif and not self.attente_code and not self.acces_bloque:
            mesure = Mesure(self.platine.pir.value)
            self.attente_code = True
            self.code_saisi = ""
            self.platine.lcd_afficher("Mouvement!", "Entrez code:")

    # Keypad

    def ajouter_touche(self, touche):
        # Accumule les touches saisies sur le keypad et les affiche sur le LCD
        if self.attente_code and not self.acces_bloque:
            self.code_saisi += touche
            # affiche les étoiles pour cacher le code
            self.platine.lcd_afficher("Entrez code:", "*" * len(self.code_saisi))

    # VALIDATION

    def valider_code(self):
        # Valide le code saisi - gère les tentatives et le blocage
        if not self.attente_code or self.acces_bloque:
            return
        # DEBUG temporaire
        print(
            f"Code saisi: '{self.code_saisi}' | Code valide: '{self.code_valide}' | Longueur saisi: {len(self.code_saisi)} | Longueur valide: {len(self.code_valide)}"
        )

        if self.code_saisi == self.code_valide:
            # Accès valide
            code_log = self.code_saisi
            self.attente_code = False
            self.tentatives = 0
            self.code_saisi = ""
            self.platine.lcd_afficher("Acces", "autorise!")
            self.platine.clignoter_verte()
            e = Evenement(
                "Accès valide du système d'alarme",
                {"capteur": str(self.platine.pir.value), "code": code_log},
            )
            self.nouveaux_evenements.append(e)
            self.vue.ajouter_event(e)

        else:
            # Accès invalide
            self.tentatives += 1
            e = Evenement(
                "Accès invalide du système d'alarme",
                {"capteur": str(self.platine.pir.value), "code": self.code_saisi},
            )
            self.nouveaux_evenements.append(e)
            self.vue.ajouter_event(e)
            self.code_saisi = ""

            if self.tentatives >= self.MAX_TENTATIVES:
                # Accès bloqué
                self.acces_bloque = True
                self.attente_code = False
                self.platine.led_verte.off()
                self.platine.lcd_afficher("Acces", "bloque!")
                self.platine.clignoter_rouge_infini()
                self.platine.bip(10)
                self.vue.update_etat(False)
                self.vue.bloquer_bouton_valid()
            else:
                # Mauvais code, réessayer
                restantes = self.MAX_TENTATIVES - self.tentatives
                self.platine.lcd_afficher("Code invalide", f"Reste: {restantes}")
                self.platine.clignoter_rouge()
                self.platine.bip(1)

    # Sauvegarde BD

    def sauvegarder_bd(self):
        # Sauvegarde les nouveaux événements dans la base de données
        if len(self.nouveaux_evenements) > 0:
            self.bd.ajouterEvenements(self.nouveaux_evenements)
            self.nouveaux_evenements = []
            print("Événements sauvegardés dans la BD")
        else:
            print("Aucun nouvel événement à sauvegarder")
