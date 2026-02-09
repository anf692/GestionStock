import mysql.connector

# Connexion à MySQL
connexion = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="tresbienmerci",
    database="gestion_stock"
)

# Vérifiez si la connexion est réussie
if connexion.is_connected():    
    print("Connecté à la base de données MySQL")
else:    
    print("Échec de la connexion à la base de données MySQL")

curseur = connexion.cursor()



#fonction pour ajouter un categorie
def ajouter_categorie():
    while True:
        nom = input("Entrer le nom de la categorie : ").strip()
        if nom.replace(" ","").isalpha():
            break
        else:
            print("Incorrect ! le nom de la categorie (seulement des lettres).")

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
   


#fonction pour fermer la base de donnnees
def fermeture():
    if connexion.is_connected():
        connexion.close()
        print("Connexion à la base de données MySQL fermée.")


#fonction principal
def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Ajouter un categorie")
        print("2. Lister categorie")
        print("3. Afficher présents")
        print("4. Rechercher apprenant")
        print("5. Supprimer un apprenant")
        print("6. Quitter")
        choix = input("Votre choix : ")
        if choix == "1":
            ajouter_categorie()
        elif choix == "2":
            lister_categories()
        elif choix == "6":
            fermeture()
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide, réessayez.")

menu()