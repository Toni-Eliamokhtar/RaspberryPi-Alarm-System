import tkinter as tk
from tkinter import messagebox
import sys
import signal


class Interface:

    def __init__(self, controleur):
        self.c = controleur

        self.root = tk.Tk()
        self.root.title("Système d'alarme")

        # Taille + Centrage de la fenêtre

        width = 650
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
            width=30,
        )
        self.label_etat.pack(pady=10)

        # Configuration code

        frame_config = tk.LabelFrame(
            self.root, text="Configuration du code d'accès", padx=10, pady=10
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
            frame_config, text="Ajouter / Modifier", command=self.modifier_code
        )
        self.btn_modifier.grid(row=1, column=2, padx=5)

        self.btn_supprimer = tk.Button(
            frame_config, text="Supprimer code", command=self.supprimer_code
        )
        self.btn_supprimer.grid(row=1, column=3, padx=5)

        # Journalisation
        frame_journal = tk.LabelFrame(
            self.root, text="Journal des événements", padx=10, pady=10
        )
        frame_journal.pack(fill="both", expand=True, padx=10, pady=5)

        # Listbox avec barre de défilement
        scrollbar = tk.Scrollbar(frame_journal)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            frame_journal, yscrollcommand=scrollbar.set, height=10
        )
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Bouton sauvegarde Base de Données
        self.btn_sauvegarder = tk.Button(
            self.root, text="Sauvegarder BD", command=self.sauvegarder_bd
        )
        self.btn_sauvegarder.pack(pady=10)

        # Gestion fermeture par la croix
        self.root.protocol("WM_DELETE_WINDOW", self.quitter_proprement)

        # Écoute le système toutes les 100ms (pour CTRL+C)
        self.interrompre_si_besoin()

    # MÉTHODES

    def update_etat(self, actif):
        # Met à jour l'étiquette d'état avec la bonne couleur
        if actif:
            self.label_etat.config(text="Système ACTIVÉ", bg="green")
        else:
            self.label_etat.config(text="Système DÉSACTIVÉ", bg="red")

    def ajouter_event(self, e):
        # Ajoute un événement dans la listbox et défile vers le bas
        self.listbox.insert(tk.END, str(e))
        self.listbox.yview(tk.END)  # défile automatiquement vers le dernier événement

    def modifier_code(self):
        # Modifie le code d'accès avec le nouveau code saisi
        nouveau = self.entry_code.get().strip()
        if nouveau == "":
            messagebox.showerror("Erreur", "Le code ne peut pas être vide.")
        else:
            self.c.code_valide = nouveau
            self.label_code_actuel.config(text=nouveau)
            self.entry_code.delete(0, tk.END)
            messagebox.showinfo("Succès", f"Code modifié avec succès.")

    def supprimer_code(self):
        # Remet le code par défaut
        self.c.code_valide = "1234"
        self.label_code_actuel.config(text="1234")
        messagebox.showinfo("Succès", "Code remis à la valeur par défaut (1234).")

    def bloquer_bouton_valid(self):
        # Désactive le champ de saisie et les boutons de configuration
        self.entry_code.config(state="disabled")
        self.btn_modifier.config(state="disabled")
        self.btn_supprimer.config(state="disabled")

    def appeler_depuis_thread(self, func, *args):
        self.root.after(0, func, *args)

    def debloquer_bouton_valid(self):
        self.entry_code.config(state="normal")
        self.btn_modifier.config(state="normal")
        self.btn_supprimer.config(state="normal")

    def interrompre_si_besoin(self):
        # Permet à Python de traiter les signaux comme SIGINT (CTRL+C)
        self.root.after(100, self.interrompre_si_besoin)

    def quitter_proprement(self, *args):
        print("\n[INFO] Fermeture en cours...")
        try:
            self.root.quit()  # sort du mainloop → finally dans main s'exécute
        except Exception:
            pass

    def sauvegarder_bd(self):
        # Sauvegarde les nouveaux événements dans la base de données
        self.c.sauvegarder_bd()
        messagebox.showinfo("Succès", "Événements sauvegardés dans la base de données.")

    def run(self):
        self.root.mainloop()
