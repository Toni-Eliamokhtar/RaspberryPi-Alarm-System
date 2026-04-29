import tkinter as tk


class Interface:

    def __init__(self, controleur):
        self.c = controleur

        self.root = tk.Tk()
        self.root.title("Système d'alarme")

        self.label = tk.Label(self.root, text="Système désactivé", bg="red", width=30)
        self.label.pack(pady=10)

        self.btn = tk.Button(self.root, text="Toggle", command=self.c.toggle)
        self.btn.pack(pady=10)

    def update_etat(self, actif):
        self.label.config(
            text="Système ACTIVÉ" if actif else "Système DÉSACTIVÉ",
            bg="green" if actif else "red",
        )

    def run(self):
        self.root.mainloop()
