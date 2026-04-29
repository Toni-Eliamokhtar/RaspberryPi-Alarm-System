from controleur.controleur import Controleur
from vue.interface import Interface
from vue.platine import Platine
import time

if __name__ == "__main__":
    c = Controleur()
    v = Interface(c)
    p = Platine(c)

    c.set_vue(v)
    c.set_platine(p)

    p.set_led(False)

    try:
        while True:
            if p.bouton_presse():
                c.toggle()
                time.sleep(0.3)

            v.root.update()

    except KeyboardInterrupt:
        p.stop()
