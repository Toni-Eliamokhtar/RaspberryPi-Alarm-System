# main.py
from controleur.controleur import Controleur
from vue.interface import Interface
from vue.platine import Platine
import signal

if __name__ == "__main__":
    # Création des objets
    c = Controleur()
    v = Interface(c)
    p = Platine(c)

    # Liaison des objets 
    c.set_vue(v)
    c.set_platine(p)

    # État initial (LED rouge ON, LCD vide)
    c.init_systeme()

    # Capture CTRL+C
    signal.signal(signal.SIGINT, v.quitter_proprement)

    # Lancement de l'interface et arrêt propre
    try:
        v.run()
    finally:          # finally s'exécute même après root.quit()
        p.stop()