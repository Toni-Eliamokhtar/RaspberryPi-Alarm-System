import tkinter as tk
from tkinter import messagebox


class Interface:

    def __init__(self, controleur):
        self.c = controleur

        self.root = tk.Tk()
        self.root.title("Système d'alarme")


        # Taille + Centrage de la fenêtre

        width  = 600
        height = 600
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")


        # État en temps réel (label)

        self.label_etat = tk.Label(
            self.root,
            text="Système désactivé",
            bg="red",
            fg="white",
            font=("Arial", 14, "bold"),
            width=30
        )
        self.label_etat.pack(pady=10)


        # Configuration code

        frame_config = tk.LabelFrame(
            self.root,
            text="Configuration du code d'accès",
            padx=10,
            pady=10
        )
        frame_config.pack(fill="x", padx=10, pady=5)
        

        # Affichage du code actuel

        tk.Label(frame_config, text="Code actuel :").grid(row=0, column=0, sticky="w")
        self.label_code_actuel = tk.Label(frame_config, text=self.c.code_valide)
        self.label_code_actuel.grid(row=0, column=1, sticky="w", padx=5)


        # Champ nouveau code

        tk.Label(frame_config, text="Nouveau code :").grid(row=1, column=0, sticky="w")
        self.entry_code = tk.Entry(frame_config, show="*")
        self.entry_code.grid(row=1, column=1, padx=5, pady=5)


        # Boutons ajouter/modifier et supprimer

        self.btn_modifier = tk.Button(
            frame_config,
            text="Ajouter / Modifier",
            command=self.modifier_code
        )
        self.btn_modifier.grid(row=1, column=2, padx=5)

        self.btn_supprimer = tk.Button(
            frame_config,
            text="Supprimer code",
            command=self.supprimer_code
        )
        self.btn_supprimer.grid(row=1, column=3, padx=5)


        # Journalisation
        frame_journal = tk.LabelFrame(
            self.root,
            text="Journal des événements",
            padx=10,
            pady=10
        )
        frame_journal.pack(fill="both", expand=True, padx=10, pady=5)

        # Listbox avec barre de défilement
        scrollbar = tk.Scrollbar(frame_journal)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            frame_journal,
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Bouton sauvegarde Base de Données
        self.btn_sauvegarder = tk.Button(
            self.root,
            text="Sauvegarder BD",
            command=self.sauvegarder_bd
        )
        self.btn_sauvegarder.pack(pady=10)



    # MÉTHODES

    def update_etat(self, actif):
        # Met à jour l'étiquette d'état avec la bonne couleur
        if actif:
            self.label_etat.config(
                text="Système ACTIVÉ",
                bg="green"
            )
        else:
            self.label_etat.config(
                text="Système DÉSACTIVÉ",
                bg="red"
            )


    def ajouter_event(self, e):
        # Ajoute un événement dans la listbox et défile vers le bas
        self.listbox.insert(tk.END, str(e))
        self.listbox.yview(tk.END)  # défile automatiquement vers le dernier événement


    def run(self):
        self.root.mainloop()
