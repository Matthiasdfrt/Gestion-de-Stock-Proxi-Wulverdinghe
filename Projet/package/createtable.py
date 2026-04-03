# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 15/05/2023
## Date de dernière modification : 10/06/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import sqlite3


# ---- Création des tables ---- #

requetes = ["DROP TABLE IF EXISTS stock;",
            "CREATE TABLE stock(EAN INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(500), prix FLOAT, stock INT, allée VARCHAR(50), situation VARCHAR(50), type VARCHAR(50));",
            "DROP TABLE IF EXISTS surgeles;",
            "CREATE TABLE surgeles(EAN INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(500), date_conso DATE, num_producteur VARCHAR(50), prix FLOAT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS viandes;",
            "CREATE TABLE viandes(EAN INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(500), date_conso DATE, num_producteur VARCHAR(50), prix FLOAT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS divers;",
            "CREATE TABLE divers(EAN INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(500), prix FLOAT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS poisson;",
            "CREATE TABLE poisson(EAN INTEGER PRIMARY KEY, nom VARCHAR(500), date_conso DATE, num_arrivage VARCHAR(25), prix FLOAT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS fruits_legumes;",
            "CREATE TABLE fruits_legumes(EAN INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(500), num_producteur VARCHAR(50), prix FLOAT, taille_lot INT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS cereale;",
            "CREATE TABLE cereale(EAN INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(500), date_conso DATE, prix FLOAT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS librairies;",
            "CREATE TABLE librairies(EAN INTEGER PRIMARY KEY NOT NULL, titre VARCHAR(500), isbn VARCHAR(50), date_publi DATE, auteurA VARCHAR(100), auteurB VARCHAR(100), auteurC VARCHAR(100), auteurD VARCHAR(100), auteurE VARCHAR(100), auteurF VARCHAR(100), auteurG VARCHAR(100), prix FLOAT, stock INT, FOREIGN KEY (EAN) REFERENCES stock(EAN) ON DELETE CASCADE ON UPDATE CASCADE);",
            "DROP TABLE IF EXISTS ticket;",
            "CREATE TABLE ticket(id_ticket INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nbr_prod_achete INT, prix tot FLOAT, jour VARCHAR(50), mois VARCHAR(50), heure VARCHAR(50));"]

# ---- Fonction de créations des tables ---- #
def create_table():
    try :
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connexion effected")
        for i in range(len(requetes)):
            c.execute(requetes[i])
        c.execute("PRAGMA foreign_keys = ON;") # Cette requête active les contraintes sur les clés étrangères
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


create_table()