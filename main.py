import mysql.connector

# Connexion à MySQL
connexion = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="tresbienmerci",
    database="GestionStock"
)

# Vérifiez si la connexion est réussie
if connexion.is_connected():    
    print("Connecté à la base de données MySQL")
else:    
    print("Échec de la connexion à la base de données MySQL")

curseur = connexion.cursor()



#fonction pour ajouter un categorie
def ajouter_categorie():
    nom= input("Entrer votre nom: ")
    sql = "INSERT INTO categories (nom_categorie) VALUES (%s)"
    curseur.execute(sql, (nom,))
    connexion.commit()
    print(f"Catégorie '{nom}' ajoutée avec succès.")


#fonction pour les categories
def lister_categories():
    sql = "SELECT id_categorie, nom_categorie FROM categories"
    curseur.execute(sql)
    for id_cat, nom in curseur.fetchall():
        print(f"{id_cat} - {nom}")
   