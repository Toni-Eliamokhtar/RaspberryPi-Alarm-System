import tkinter as tk


class Interface:

    def __init__(self, controleur):
        self.c = controleur

        self.root = tk.Tk()
        self.root.title("Système d'alarme")

        # taille + centrage
        width = 600
        height = 400

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.label_etat = tk.Label(
            self.root, text="Système désactivé", bg="red", width=30
        )
        self.label_etat.pack(pady=10)

        self.label_message = tk.Label(self.root, text="")
        self.label_message.pack(pady=10)

        self.listbox = tk.Listbox(self.root, height=10)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def update_etat(self, actif):
        self.label_etat.config(
            text="Système ACTIVÉ" if actif else "Système DÉSACTIVÉ",
            bg="green" if actif else "red",
        )

    def update_message(self, msg):
        self.label_message.config(text=msg)

    def ajouter_event(self, e):
        self.listbox.insert(tk.END, str(e))

    def run(self):
        self.root.mainloop()
