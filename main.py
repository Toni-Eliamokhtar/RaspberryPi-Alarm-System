from controleur.controleur import Controleur
from vue.interface import Interface
from vue.platine import Platine

if __name__ == "__main__":
    c = Controleur()
    v = Interface(c)
    p = Platine(c)

    c.set_vue(v)
    c.set_platine(p)

    c.init_systeme()

    try:
        v.run()
    finally:
        p.stop()
