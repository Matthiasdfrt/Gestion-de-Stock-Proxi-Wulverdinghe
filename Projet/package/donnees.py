# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 15/05/2023
## Date de dernière modification : 26/05/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import json
from datetime import datetime
import csv
import sqlite3

# ---- Création des listes ---- #
librairie = []
cereales = []
divers = []
fruitleg = []
poisson = []
surgele = []
viandes = []
stocks = []

# ---- Traitement des données pour les mettres dans stock ---- #
def stock():
    l = library()
    c = cereale()
    d = diversins()
    fl = frl()
    p = poissons()
    s = surgeles()
    v = viande()
    for i in range(len(l)):
        liste = [l[i][0],l[i][1],l[i][11],l[i][12]]
        liste.append("A")
        liste.append("stock")
        liste.append("librairie")
        stocks.append(liste)
    for i in range(len(c)):
        del c[i][2]
        c[i].append("B")
        c[i].append("stock")
        c[i].append("cereale")
        stocks.append(c[i])    
    for i in range(len(d)):
        d[i].append("C")
        d[i].append("stock")
        d[i].append("divers")
        stocks.append(d[i])  
    for i in range(len(fl)):
        del fl[i][2]
        del fl[i][3]
        fl[i].append("D")
        fl[i].append("stock")
        fl[i].append("fruits et légumes")
        stocks.append(fl[i])  
    for i in range(len(p)):
        del p[i][2]
        del p[i][2]
        p[i].append("E")
        p[i].append("stock")
        p[i].append("poissons")
        stocks.append(p[i])
    for i in range(len(s)):
        del s[i][2]
        del s[i][2]
        s[i].append("F")
        s[i].append("stock")
        s[i].append("surgelés")
        stocks.append(s[i])
    for i in range(len(v)):
        del v[i][2]
        del v[i][2]
        v[i].append("G")
        v[i].append("stock")
        v[i].append("viandes")
        stocks.append(v[i])
    return stocks

# ---- Traitement du fichier librairie ---- #
def library():
    with open('data/librairie.json') as mon_fichier:
        data = json.load(mon_fichier)
    for i in range(len(data)):
        date = datetime.strptime(data[i]["publishedDate"], "%Y-%m-%dT%H:%M:%S.%f%z")
        datepropre = date.strftime("%Y-%m-%d")
        liste = [data[i]["EAN"],data[i]["title"],data[i]["isbn"],datepropre]
        for j in range(len(data[i]["authors"])):
            liste.append(data[i]["authors"][j])
        if len(data[i]["authors"]) < 7:
            n = 7 - len(data[i]["authors"])
            for k in range(n):
                liste.append("")
        liste.append(data[i]["price"])
        liste.append(data[i]["stock"])
        librairie.append(liste)
    return librairie


# ---- Traitement du fichier cereale ---- #
def cereale():
    with open('data/cereal.json') as mon_fichier:
        data = json.load(mon_fichier)
    for i in range(len(data)):
        liste = [data[i]["EAN"], data[i]["name"], data[i]["date_limite_conso"], data[i]["price"], data[i]["stock"]]
        cereales.append(liste)
    return cereales


# ---- Traitement du fichier divers ---- #
def diversins():
    with open("data/divers.txt", 'r') as file:
        for line in file:
            parsed_data = line.strip().split('|')
            elt = parsed_data.pop()
            parsed_data.insert(0,elt)
            divers.append(parsed_data)
    del divers[0]
    return divers


# ---- Traitement du fichier fruits et légumes ---- #
def frl():
    with open("data/fruits_legumes.txt", 'r') as file:
        for line in file:
            parsed_data = line.strip().split('|') 
            elt = parsed_data.pop()
            parsed_data.insert(0,elt)
            fruitleg.append(parsed_data)
    del fruitleg[0]
    return fruitleg


# ---- Traitement du fichier poissons ---- #
def poissons():
    f = open("data/poisson.csv","r", encoding="utf8")
    reads = csv.reader(f)
    for row in reads:
        elt = row.pop()
        row.insert(0,elt)
        poisson.append(row)
    del poisson[0]
    f.close()
    return poisson


# ---- Traitement du fichier surgeles ---- #
def surgeles():
    f = open("data/surgele.csv","r", encoding="utf8")
    reads = csv.reader(f)
    for row in reads:
        elt = row.pop()
        row.insert(0,elt)
        surgele.append(row)
    del surgele[0]
    f.close()
    return surgele


# ---- Traitement du fichier viande ---- #
def viande():
    f = open("data/viandes.csv","r", encoding="utf8")
    reads = csv.reader(f)
    for row in reads:
        elt = row.pop()
        row.insert(0,elt)
        viandes.append(row)
    del viandes[0]
    f.close()
    return viandes


# ---- Préparation des requêtes préparées pour insérer les données  ---- #
requete =  "INSERT INTO stock(EAN, nom, prix, stock, allée, situation, type) VALUES (?, ?, ?, ?, ?, ?, ?);"
requete1 =  "INSERT INTO surgeles(EAN, nom, date_conso, num_producteur, prix, stock) VALUES (?, ?, ?, ?, ?, ?);"
requete2 =  "INSERT INTO viandes(EAN, nom, date_conso, num_producteur, prix, stock) VALUES (?, ?, ?, ?, ?, ?);"
requete3 =  "INSERT INTO divers(EAN, nom, prix, stock) VALUES (?, ?, ?, ?);"
requete4 =  "INSERT INTO poisson(EAN, nom, date_conso, num_arrivage, prix, stock) VALUES (?, ?, ?, ?, ?, ?);"
requete5 =  "INSERT INTO fruits_legumes(EAN, nom, num_producteur, prix, taille_lot, stock) VALUES (?, ?, ?, ?, ?, ?);"
requete6 =  "INSERT INTO cereale(EAN, nom, date_conso, prix, stock) VALUES (?, ?, ?, ?, ?);"
requete7 =  "INSERT INTO librairies(EAN, titre, isbn, date_publi, auteurA, auteurB, auteurC, auteurD, auteurE, auteurF, auteurG, prix, stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

# ---- Insertion des données ---- #
def insert(sql, data):
    try :
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connexion effected")
        for i in range(len(data)):
            c.execute(sql, data[i])
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


# ---- Appel des fonctions pour insérer les données ---- #
#insert(requete, stock())
#insert(requete1, surgeles())
#insert(requete2, viande())
#insert(requete3, diversins())
#insert(requete4, poissons())
#insert(requete5, frl())
#insert(requete6, cereale())
#insert(requete7, library())