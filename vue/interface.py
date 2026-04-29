import tkinter as tk


class Interface:

    def __init__(self, controleur):
        self.root = tk.Tk()
        self.root.title("Système d'alarme")

        self.label = tk.Label(self.root, text="Système désactivé", bg="red", width=30)
        self.label.pack(pady=20)

    def run(self):
        self.root.mainloop()
