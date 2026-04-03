# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 10/06/2023
## Date de dernière modification : 10/06/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import random
import sqlite3
from datetime import datetime

# ---- Génération des données aléatoires ---- #
rdm = []
for _ in range(100):
    nbr_prod_achete = random.randint(1, 10)
    prix = round(random.uniform(10.0, 100.0), 2)
    jour = random.choice(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
    mois = random.choice(["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
    heure = datetime.strptime(f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}", "%H:%M").strftime("%H:%M")
    rdm.append([nbr_prod_achete, prix, jour, mois, str(heure)])

# ---- Insertion des valeurs aléatoires ---- #
req = "INSERT INTO ticket (nbr_prod_achete, prix, jour, mois, heure) VALUES (?, ?, ?, ?, ?)"

def inserttest(sql, data):
    try :
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connexion effected")
        for i in range(len(data)):
            c.execute(sql,data[i]) 
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


inserttest(req, rdm)