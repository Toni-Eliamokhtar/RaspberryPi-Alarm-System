import sqlite3
import os


class GestionnaireBD:
    def __init__(self):
        # Chemin relatif vers le dossier fichiersBD
        self.dossier = "fichiersBD"
        self.nomBD = os.path.join(self.dossier, "alarme.db")
        self.tableEvenement = "evenements"
        self.connexion = None

        # Crée le dossier s'il n'existe pas
        if not os.path.exists(self.dossier):
            os.makedirs(self.dossier)

        # Crée la table au démarrage si elle n'existe pas
        self.creationTable()

    # Connexion à la base de données

    def connexionBD(self):
        try:
            print("Chemin BD :", os.path.abspath(self.nomBD))
            self.connexion = sqlite3.connect(self.nomBD)
        except sqlite3.Error as error:
            print("Erreur de connexion à la base de données", error)

    # Fermeture de la base de données
    def fermetureDB(self):
        if self.connexion:
            self.connexion.close()
            self.connexion = None
        else:
            print("Erreur de connexion à la base de données")

    # Vérifier si la table existe dans la BD
    def verifierExisteTable(self, table):
        existe = False
        cur = self.connexion.cursor()
        sql_tableExiste = (
            "SELECT count(name) "
            "FROM sqlite_master "
            "WHERE type='table' AND name='" + table + "'"
        )
        try:
            cur.execute(sql_tableExiste)
            if cur.fetchone()[0] == 1:
                existe = True
            else:
                existe = False
        except sqlite3.Error as error:
            print("Erreur lors d'une opération sur la base de données", error)
        return existe

    # Création de la table des événements
    def creationTable(self):
        tableEvenements = (
            "CREATE TABLE " + self.tableEvenement + " ( "
            "id            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "dateHeure     TEXT NOT NULL, "
            "typeEvenement TEXT NOT NULL, "
            "valeurCapteur TEXT, "
            "codeSaisi     TEXT);"
        )

        self.connexionBD()

        if self.verifierExisteTable(self.tableEvenement):
            print("La table existe déjà")
        else:
            try:
                self.connexion.execute(tableEvenements)
                print("Création de la table")
            except sqlite3.Error as error:
                print("Erreur lors d'une opération sur la base de données", error)

        self.fermetureDB()

    # Ajouter une liste d'événements dans la BD
    def ajouterEvenements(self, evenements):
        sql_insert = (
            "INSERT INTO "
            + self.tableEvenement
            + " (dateHeure, typeEvenement, valeurCapteur, codeSaisi) VALUES (?, ?, ?, ?);"
        )

        self.connexionBD()

        try:
            cur_insert = self.connexion.cursor()
            for e in evenements:
                donnees_param = (
                    e.dateHeureEvenement.strftime("%Y-%m-%d %H:%M:%S"),
                    e.typeEvenement,
                    e.donneeEvenement.get("capteur", ""),
                    e.donneeEvenement.get("code", ""),
                )

                print("INSERT :", donnees_param)

                cur_insert.execute(sql_insert, donnees_param)
            # Sauvegarde des données
            self.connexion.commit()
            print("Enregistrements ajoutés dans la table")
            cur_insert.close()
        except sqlite3.Error as error:
            print("Erreur lors d'une opération sur la base de données", error)
        finally:
            self.fermetureDB()
