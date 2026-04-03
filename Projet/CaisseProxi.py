# ============================================================================= #
## Auteur : Matthias Defretin
## Projet : SAE Conception et implémentation d'une base de données 
## Date : 01/06/2023
## Date de dernière modification : 07/06/2023
# ============================================================================= #

# ---- Importation des packages ---- #
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QFrame, QApplication, QMessageBox, QInputDialog
import sqlite3
import datetime
import os

# ---- code de l'interface ---- #
class VenteGUI(QMainWindow):
    def __init__(self, parent=None):
        super(VenteGUI, self).__init__(parent)
        self.setWindowTitle("Vente GUI")
        # INFO
        self.info = QLabel()
        self.info.setText("Caisse Proxi")
        # ZONE DE SAISIE
        self.entryfield = QLineEdit()
        self.valid = QPushButton("Valid")
        self.valid.clicked.connect(self.validation_article)
        self.valid.setShortcut('Return')
        self.validticket = QPushButton("END")
        self.validticket.clicked.connect(self.validation_ticket)
        # LOG de SAISIE
        self.scrollA = QScrollArea()
        self.scrollA.setWidgetResizable(True)
        self.scrollA.setFrameShape(QFrame.NoFrame)
        self.ticket = QLabel()
        self.scrollA.setWidget(self.ticket)
        self.ticket.setWordWrap(True)
        # LAYOUT
        layout = QGridLayout()
        layout.addWidget(self.info, 0, 0)
        layout.addWidget(QLabel("Entrez l'EAN du produit"), 1, 0, 1, 3)
        layout.addWidget(self.entryfield, 1, 3)
        layout.addWidget(self.valid, 1, 4)
        layout.addWidget(self.validticket, 1, 5)
        layout.addWidget(self.scrollA, 2, 0, 4, 6)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout)
        self.resize(1000, 500)
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.caissier = ""

    def validation_article(self): #Fonction pour récupérer à partir de l'EAN donc comme un scanner de caisse le nom du produit et le prix de ce dernier dans la base de données
        ean = self.entryfield.text()
        article = self.get_article_info(ean)
        if article:
            nom, prix, stock = article
            if stock > 0:
                quantite, ok = QInputDialog.getInt(self, "Quantité", "Quantité :", min=1, max=stock)
                if ok:
                    if quantite <= stock:
                        self.update_stock(ean, stock - quantite)
                        prix_total = prix * quantite  # Calcul du prix total
                        self.add_to_ticket(nom, quantite, prix_total)
                        self.entryfield.setText("")
                    else:
                        QMessageBox.warning(self, "Stock insuffisant", "Il n'y a pas suffisamment de stock pour ce produit.")
            else:
                QMessageBox.warning(self, "Stock épuisé", "Cet article est actuellement en rupture de stock.")
        else:
            QMessageBox.warning(self, "Produit introuvable", "Ce produit n'existe pas dans la base de données.")

    def validation_ticket(self): # Cette fonction est l'appel d'autres fonction pour générer le texte et insérer les données relative au ticket dans la base de données
        self.generate_ticket_file()
        self.insert_ticket_info()
        msgbox_valid = QMessageBox()
        msgbox_valid.setText(self.ticket.text())
        self.ticket.setText("")
        msgbox_valid.exec()

    def get_article_info(self, ean): #Focntion utilisée précédement dans valid article pour chercher les données d'un produit
        self.cursor.execute("SELECT nom, prix, stock FROM stock WHERE EAN=?", (ean,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def update_stock(self, ean, new_stock): #Update les stocks en focntion de la quantité acheté
        self.cursor.execute("UPDATE stock SET stock=? WHERE EAN=?", (new_stock, ean))
        self.conn.commit()

    def add_to_ticket(self, nom, quantite, prix_total): #ajoite au ticket les lignes d'article
        ticket_temp = self.ticket.text() + f"\n{nom} - Quantité: {quantite} - Prix total: {prix_total}"
        self.ticket.setText(ticket_temp)

    def generate_ticket_file(self): #Toutes la fonctions de génération du ticket en fichier txt
        ticket_info = self.ticket.text()
        filename = "dossierticket/ticket.txt"
        counter = 1

        while os.path.exists(filename):
            filename = f"dossierticket/ticket{counter}.txt" # vérifie si le fichier ticketn.txt existe et si c'est le cas vérif si ticketn+1.txt existe
            counter += 1

        with open(filename, "w") as f:
            f.write("Proxi Wulverdinghe\n")
            f.write(f"Caissier : {self.caissier}\n")
            f.write("\nArticles :\n")
            f.write(ticket_info)
            f.write("\n\n")
            prix_ht = self.calculate_total_ht()
            f.write(f"Prix total HT : {round(prix_ht, 2)}\n")
            prix_ttc = self.calculate_total_ttc(prix_ht)
            f.write(f"TVA (20%) : {round(prix_ttc - prix_ht, 2)}\n")
            f.write(f"Prix total TTC : {round(prix_ttc, 2)}\n")

    def calculate_total_ht(self): #Total HT
        # Calcul du prix total HT en parcourant les articles du ticket
        total_ht = 0
        lines = self.ticket.text().split('\n')
        for line in lines[1:]:
            if line:
                _, _, prix_total = line.split('-')
                prix_total = prix_total.strip().split(':')[1].strip()  # Extraction de la valeur numérique
                total_ht += float(prix_total)
        return total_ht

    def calculate_total_ttc(self, total_ht): #Total TTC
        # Calcul du prix total TTC en ajoutant la TVA (20%)
        tva = 0.2
        total_ttc = total_ht + (total_ht * tva)
        return total_ttc

    def insert_ticket_info(self):
        ticket_info = self.ticket.text()
        nbr_prod_achete = self.calculate_total_quantity()# Récupérer le nombre total d'articles achetés
        prix_ht = self.calculate_total_ht()# Récupérer le prix total HT arrondi à deux décimales
        prix_ht = round(prix_ht, 2)
        current_datetime = datetime.datetime.now()# Récupérer la date et l'heure de l'achat
        jour = current_datetime.strftime("%A")  # Nom du jour de la semaine (ex : lundi, mardi, ...)
        mois = current_datetime.strftime("%B")  # Nom du mois (ex : janvier, février, ...)
        heure = current_datetime.strftime("%H:%M")  # Heure au format 24h (ex : 15:22)

        self.cursor.execute("INSERT INTO ticket(nbr_prod_achete, prix, jour, mois, heure) VALUES (?, ?, ?, ?, ?)",(nbr_prod_achete, prix_ht, jour, mois, heure))# Insert les informations du ticket dans la table ticket
        self.conn.commit()

    def calculate_total_quantity(self):
        # Calculer le nombre total d'articles achetés en parcourant les lignes du ticket
        total_quantity = 0
        lines = self.ticket.text().split('\n')
        for line in lines[1:]:
            if line:
                quantity = line.split('-')[1].strip().split(':')[1].strip()  # Extraire la quantité de chaque ligne
                total_quantity += int(quantity)
        return total_quantity

    def closeEvent(self, event):#Ferme la connexion à la base de données après fermeture de l'app
        self.conn.close()
        event.accept()

    def set_caissier(self, caissier):
        self.caissier = caissier

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    fen = VenteGUI()
    fen.show()
    caissier, ok = QInputDialog.getText(fen, "Caissier", "Entrez votre nom :") # Demander le nom du caissier
    if ok:
        fen.set_caissier(caissier)
    app.exec_()

