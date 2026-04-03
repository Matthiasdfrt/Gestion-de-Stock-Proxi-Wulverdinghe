README
auteur : Matthias Defretin
# --------------------------------------------------------------------------------- #
Voici le projet pour la supêrete proxi de Wulverdinghe.

1. Si jamais vous voulez lancer le système de gestion des stocks (Partie B) il faut lancer le script stockage.py. Une fois fait il y a juste à faire ce que demande le programme.
   Un fichier de log sera créé automatiquement au premier lancement du programme ensuite le programme mettera à jour le fichier déjà existant
   Pour le couper il faut appuyer sur Ctrl + C

2. Si jamais vous voulez utiliser la caisse (Partie C) lancez le script CaisseProxi.py une fois cela fait rentrer votre nom (Prénom du caissier utilisant la caisse)
   Quand un client achète quelque chose entrez l'EAN des produits acheté et choisissez la quantité acheté et pour finir presser Valid.
   Quand le ticket est fini presser END ce la créera le ticket dans le dossier dossierticket

3. Si jamais vous voulu le compte rendu des ventes lancez le script compterendu.py (partie D) une fois cela fait un dashboard apparaitra tout seul.

# --------------------------------------------------------------------------------- #

Si il y a un problème avec les valeurs de la bdd lancer le script createtable?py dans le dossier package et ensuite insérez les données avec le script donnees.py.
ATTENTION a bien lancer les fonctions appelées en bas du script une par une (cause conflit non expliqué quand tout est lancé en même temp)

Si jamais vous voulez faire un test du dashboard avec beaucoup de valeurs lancez le script valeur.py il inserera 100 lignes aléatoires dans la table ticket pour le test du dashboard

# --------------------------------------------------------------------------------- #
Groupe : DEFRETIN Matthias, DUPUI Thibaut
Société Cliente = proxi
Société = IUT GRAND OUEST NORMANDIE