# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 15/05/2023
## Date de dernière modification : 08/06/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import sqlite3
import signal
from package.packagestock import insert
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
def question(): #Question pour déterminer l'action
    try:
        act = int(input("Que voulez-vous faire :\n1. Rentrer un produit dans le stock\n2. Ranger un produit\n3. Retirer un produit du stock\n4. Rechercher un produit dans le stock\n\nTapez le chiffre de l'action de votre choix : ")) 
        return act
    except ValueError:
        logger.error("Problème de valeur entrée")
        print("Veuillez entrer un nombre valide.\n")

#################### Plusieurs test EAN car la phrase n'est pas la même ####################  
def checkean():
    try:
        act = int(input("Donnez l'EAN du produit que vous voulez ranger : ")) 
        return act
    except ValueError:
        logger.error("Problème de valeur entrée")
        print("Veuillez entrer un nombre valide.\n")

def checkean2():
    try:
        act = int(input("Donnez l'EAN du produit que vous voulez supprimer : ")) 
        return act
    except ValueError:
        logger.error("Problème de valeur entrée")
        print("Veuillez entrer un nombre valide.\n")

def checkean3():
    try:
        act = int(input("Donnez l'EAN du produit que vous voulez chercher : ")) 
        return act
    except ValueError:
        logger.error("Problème de valeur entrée")
        print("Veuillez entrer un nombre valide.\n")

# ---- Fonctions pour la gestion totale de la base du magasin ---- #
def gestion():
    try :
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connexion effected")
        while True:
            signal.signal(signal.SIGINT, signal.SIG_DFL) #capte le signal du clavier pour l'interompre si le USER appuie sur ctrl+C
            try:
                a = question() #Pour savoir quelle action veut faire le USER
                if a == 1:
                    insert() #Appel de la fonction du package packagestock
                elif a == 2: #partie pour le rangement
                    iden = checkean()
                    c.execute("SELECT situation FROM stock WHERE EAN = ?;",(iden,))
                    verif = c.fetchall()
                    print(f"Le produit est actuellement en {verif}.\n") 
                    change = input("Voulez vous le mettre en stock ou en magasin (0 pour stock, 1 pour magasin et 2 ne rien faire) : ")
                    if change == "0":
                        c.execute("UPDATE stock SET situation = 'stock' WHERE EAN = ?;", (iden,))
                        print("L'article sera mis en stock.\n")
                        logger.info(f"Le produit avec l'EAN {iden} a été mis en stock")
                        connection.commit()
                        connection.close()
                    elif change == "1":
                        c.execute("UPDATE stock SET situation = 'magasin' WHERE EAN = ?;", (iden,))
                        print("L'article sera mis en magasin. \n")
                        logger.info(f"Le produit avec l'EAN {iden} a été mis en magasin")
                        connection.commit()
                        connection.close()
                    elif change == "2":
                        print("Aucune action ne sera effectuée.")
                        connection.close()
                    else:
                        print("Valeur incorrecte. Veuillez saisir 0, 1 ou 2.")
                elif a == 3: #partie pour la suppresion de ligne
                    sup = checkean2()
                    c.execute("PRAGMA foreign_keys = ON;")
                    c.execute("DELETE FROM stock WHERE EAN = ?;", (sup,))
                    logger.info(f"Le produit avec l'EAN {sup} a été supprimé")
                    connection.commit()
                    connection.close()
                else: #partie pour la recherche
                    search = checkean3()
                    c.execute("SELECT * FROM stock WHERE EAN = ?;",(search,))
                    logger.info(f"L'objet avec l'EAN {search} a été recherché.")
                    result = c.fetchall()
                    print(result)
                    connection.close()
            except KeyboardInterrupt:
                connection.close()
                logger.info("Système de gestion arrêté")
                print("Boucle interrompue.")
                break
    except Exception as e:
        logger.error("Problème lié à la base de données")
        print(e)

gestion()