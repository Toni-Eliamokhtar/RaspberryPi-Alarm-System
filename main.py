from controleur.controleur import Controleur
from vue.interface import Interface

if __name__ == "__main__":
    c = Controleur()
    v = Interface(c)
    c.set_vue(v)

    v.run()
