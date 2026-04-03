# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 15/05/2023
## Date de dernière modification : 08/06/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import sqlite3
import datetime
import re
import logging

# ---- Settings du log ---- #
logger = logging.getLogger("logs")
if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler('file.log')
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

# ---- Fonctions nécessaires pour le bon fonctionnement du programme global ---- #
def is_valid_date(): #vérifie la validité des dates données
    while True:
        try:
            date_str = input('Entrez la date de publication ou la date de conso (cela dépend du type de produit) : ')
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            logger.error("Date incorrecte entrée")
            print("Format de date incorrect. Veuillez entrer une date au format YYYY-MM-DD.")
    
reqcheck = "SELECT COUNT(*) FROM stock WHERE EAN = ?;"
def check(req, data): #Vérifie si un produit similaire et déjà dans la base
    try :
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connexion effected")
        c.execute(req, data)
        result = c.fetchone()[0]
        connection.close()
        return result > 0
    except Exception as e:
        logger.error("Erreur de la vérification de l'existence de l'EAN dans la base de données")
        print(e)

def question2(): #Test pour choisir un cas
    while True:
        try:
            up = int(input("Voulez-vous modifier la valeur déjà existente ? (0 pour non, 1 pour oui): "))
            if up == 0 or up == 1:
                return up
            else:
                print("Veuillez entrer seulement 0 ou 1.\n")
                logger.error("Mauvais choix de nombre")
        except ValueError:
            logger.error("Problème de valeur entrée")
            print("Veuillez entrer un nombre valide.\n")

def question3(): #Vérification de la validité du prix donné
    while True:
        try:
            prix = float(input("Entrez le prix du produit : "))
            return prix
        except ValueError:
            logger.error("Problème de valeur entrée")
            print("Veuillez entrer un nombre à virgule valide (rappel le système ne prend que les chiffres à virgules séparé par un point).\n")

def question4(): # Vérification qu'une quantité normal est donnée
    while True:
        try:
            stk = int(input("Entrez la quantité de produit : "))
            return stk
        except ValueError:
            logger.error("Problème de valeur entrée")
            print("Veuillez entrer un nombre valide.\n")

def question5(): #Vérification taille du lot
    while True:
        try:
            tl = int(input("Entrez la taille du lot du produit : "))
            return tl
        except ValueError:
            logger.error("Problème de valeur entrée")
            print("Veuillez entrer un nombre valide.\n")

def EAN(): #Verif EAN valide
    while True:
        try:
            ean = input("Donnez l'EAN du produit : ")
            if len(ean) == 10:
                ean = int(ean)
                return ean
            else:
                logger.error("EAN saisit trop petit")
                print("L'EAN doit être compris entre 1000000000 et 9999999999.\n")
        except ValueError:
            logger.error("Problème de valeur entrée")
            print("Veuillez entrer une valeur numérique.\n")

# ---- Fonction qui permet l'insertion sans erreur dans la base de données ---- #
def insert(): 
    try :
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connexion effected")
        while True:
            table_name = input("Entrez le nom de la table du produit que vous voulez insérer : ") 
            c.execute(f"PRAGMA table_info({table_name})")
            table_info = c.fetchall()
            if table_info:
                break
            else:
                print("Nom de table incorrect. Veuillez entrer un nom de table valide.")
                logger.error("Nom de table incorrect")
        columns = [column[1] for column in table_info]
        ean = EAN() #demande l'EAN du produit
        if check(reqcheck,[ean]): #vérification de si l'EAN est déjà dans la base
            print(f"La valeur '{ean}' existe dans la base de données.")
            up = question2() #Question pour savoir si la personne veut modifier la ligner déjà existante
            if up == 1:
                modif = input(f"Quelle valeur de quelle colonne voulez vous modifier {columns}: ")
                if modif == "EAN":
                    eans = EAN()
                    req = f"UPDATE stock SET EAN = ? WHERE EAN = {ean};"
                    c.execute("PRAGMA foreign_keys = ON;")
                    c.execute(req,[eans])
                    logger.info("Modification d'un EAN")
                    print("Changement effectué !")
                elif modif == "nom" or modif == "titre":
                    nom = input("Donnez le nom/titre du produit : ")
                    req = f"UPDATE stock SET nom = ? WHERE EAN = {ean};"
                    req1 = f"UPDATE {table_name} SET {modif} = ? WHERE EAN = {ean};"
                    c.execute(req,[nom])
                    c.execute(req1,[nom])
                    logger.info("Modification d'un nom ou d'un titre de produit")
                    print("Changement effectué !")
                elif modif == "prix":
                    prix = question3()
                    req = f"UPDATE stock SET prix = ? WHERE EAN = {ean};"
                    req1 = f"UPDATE {table_name} SET prix = ? WHERE EAN = {ean};"
                    c.execute(req,[prix])
                    c.execute(req1,[prix])
                    logger.info("Modification d'un prix de produit")
                    print("Changement effectué !")
                elif modif == "stock":
                    stk = question4()
                    req = f"UPDATE stock SET stock = ? WHERE EAN = {ean};"
                    req1 = f"UPDATE {table_name} SET stock = ? WHERE EAN = {ean};"
                    c.execute(req,[stk])
                    c.execute(req1,[stk])
                    logger.info("Modification d'un stock de produit")
                    print("Changement effectué !")
                elif re.search(r'^date\w', modif):
                    date = is_valid_date()
                    req1 = f"UPDATE {table_name} SET {modif} = ? WHERE EAN = {ean};"
                    c.execute(req1,[date])
                    logger.info("Modification d'une date de produit")
                    print("Changement effectué !")
                elif modif == "taille_lot":
                    taille = question5()
                    req1 = f"UPDATE {table_name} SET taille_lot = ? WHERE EAN = {ean};"
                    c.execute(req1,[taille])
                    logger.info("Modification d'une taille de lot de produit")
                    print("Changement effectué !")
                else:
                    other = input(f"Entrez {modif} : ")
                    req1 = f"UPDATE {table_name} SET {modif} = ? WHERE EAN = {ean};"
                    c.execute(req1,[other])
                    logger.info("Modification d'info de produit")
                    print("Changement effectué !")
        else: # Toute la partie pour insérer une ligne
            print(f"La valeur '{ean}' n'existe pas dans la base de données.")
            stock = []
            table = []
            for i in range(len(columns)):
                if columns[i] == "EAN":
                    stock.append(ean)
                    table.append(ean)
                elif columns[i] == "nom" or columns[i] == "titre":
                    nom = input("Donnez le nom/titre du produit : ")
                    stock.append(nom)
                    table.append(nom)
                elif columns[i] == "prix":
                    prix = question3()
                    stock.append(prix)
                    table.append(prix)
                elif columns[i] == "stock":
                    stk = question4()
                    stock.append(stk)
                    table.append(stk)
                elif re.search(r'^date\w', columns[i]):
                    date = is_valid_date()
                    table.append(date)
                elif columns[i] == "taille_lot":
                    taille = question5()
                    table.append(taille)
                else:
                    other = input(f"Entrez {columns[i]} : ")
                    table.append(other)
            allee = input("Donnez la lettre de l'allée dans laquelle est le produit : ")
            stock.append(allee)
            situation = input("Le produit ce trouve en magasin ou en stock ? (entrez stock ou magasin) : ")
            stock.append(situation)
            stock.append(table_name)
            requete =  "INSERT INTO stock(EAN, nom, prix, stock, allée, situation, type) VALUES (?, ?, ?, ?, ?, ?, ?);"
            c.execute(requete, stock)
            logger.info("Insertion d'une ligne dans la table stock")
            if table_name == "surgeles":
                requete1 =  "INSERT INTO surgeles(EAN, nom, date_conso, num_producteur, prix, stock) VALUES (?, ?, ?, ?, ?, ?);"
                c.execute(requete1, table)
                logger.info("Insertion d'une ligne dans la table surgeles")
            elif table_name == "viandes":
                requete2 =  "INSERT INTO viandes(EAN, nom, date_conso, num_producteur, prix, stock) VALUES (?, ?, ?, ?, ?, ?);"
                c.execute(requete2, table)
                logger.info("Insertion d'une ligne dans la table viandes")
            elif table_name == "divers":
                requete3 =  "INSERT INTO divers(EAN, nom, prix, stock) VALUES (?, ?, ?, ?);"
                c.execute(requete3, table)
                logger.info("Insertion d'une ligne dans la table divers")
            elif table_name == "poisson":
                requete4 =  "INSERT INTO poisson(EAN, nom, date_conso, num_arrivage, prix, stock) VALUES (?, ?, ?, ?, ?, ?);"
                c.execute(requete4,table)
                logger.info("Insertion d'une ligne dans la table poisson")
            elif table_name == "fruits_legumes":
                requete5 =  "INSERT INTO fruits_legumes(EAN, nom, num_producteur, prix, taille_lot, stock) VALUES (?, ?, ?, ?, ?, ?);"
                c.execute(requete5, table)
                logger.info("Insertion d'une ligne dans la table fruits et legumes")
            elif table_name == "cereale":
                requete6 =  "INSERT INTO cereale(EAN, nom, date_conso, prix, stock) VALUES (?, ?, ?, ?, ?);"
                c.execute(requete6, table)
                logger.info("Insertion d'une ligne dans la table cereale")
            else:
                requete7 =  "INSERT INTO librairies(EAN, titre, isbn, date_publi, auteurA, auteurB, auteurC, auteurD, auteurE, auteurF, auteurG, prix, stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                c.execute(requete7, table)
                logger.info("Insertion d'une ligne dans la table librairies")
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)