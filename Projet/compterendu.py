# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 10/06/2023
## Date de dernière modification : 10/06/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---- Création du dashboard de compte rendu ---- #
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM ticket")# Récupération des données de la table "ticket"
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=["id_ticket", "nbr_prod_achete", "prix", "jour", "mois", "heure"])
df["heure"] = pd.to_datetime(df["heure"]).dt.hour# Conversion de la colonne "heure" en datetime et extraction de l'heure
df["prix_tot"] = df["nbr_prod_achete"] * df["prix"]
colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
sns.set(style="darkgrid", palette=colors)# Création du dashboard avec Seaborn et Matplotlib
plt.figure(figsize=(12, 8))

# Graphique 1 : Total des ventes par jour (Diagramme à barres)
plt.subplot(2, 2, 1)
sns.barplot(data=df, x="jour", y="prix_tot")
plt.title("Total des ventes par jour")
plt.xlabel("Jour")
plt.ylabel("Prix total")
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Graphique 2 : Nombre moyen de produits achetés par jour (Boxplot)
plt.subplot(2, 2, 2)
sns.boxplot(data=df, x="jour", y="nbr_prod_achete")
plt.title("Nombre moyen de produits achetés par jour")
plt.xlabel("Jour")
plt.ylabel("Nombre moyen de produits")
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Graphique 3 : Répartition des ventes par heure (Histogramme)
plt.subplot(2, 2, 3)
sns.histplot(data=df, x="heure", bins=24)
plt.title("Répartition des ventes par heure")
plt.xlabel("Heure")
plt.ylabel("Nombre de ventes")
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Graphique 4 : Montant moyen des ventes par mois (Diagramme à barres)
plt.subplot(2, 2, 4)
sns.barplot(data=df, x="mois", y="prix_tot")
plt.title("Montant moyen des ventes par mois")
plt.xlabel("Mois")
plt.ylabel("Montant moyen des ventes")
plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=8)

plt.tight_layout()
plt.show()
conn.close()


