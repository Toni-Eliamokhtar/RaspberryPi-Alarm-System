import tkinter as tk


class Interface:

    def __init__(self, controleur):
        self.c = controleur

        self.root = tk.Tk()
        self.root.title("Système d'alarme")

        width = 600
        height = 400

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.label = tk.Label(self.root, text="Système désactivé", bg="red", width=30)
        self.label.pack(pady=20)

    def update_etat(self, actif):
        self.label.config(
            text="Système ACTIVÉ" if actif else "Système DÉSACTIVÉ",
            bg="green" if actif else "red",
        )

    def run(self):
        self.root.mainloop()
