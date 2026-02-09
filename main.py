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
   

#fonction pour ajouter un produit
def ajouter_produit():
    try:
        designation = input("Entrez le nom du produit : ").strip()
        
        while True:
            try:
                prix = float(input("Entrez le prix unitaire : "))
                if prix >= 0:
                    break
                else:
                    print("Le prix doit être positif.")
            except ValueError:
                print("Veuillez entrer un nombre valide pour le prix.")
        
        while True:
            try:
                quantite = int(input("Entrez la quantité en stock : "))
                if quantite >= 0:
                    break
                else:
                    print("La quantité doit être positive.")
            except ValueError:
                print("Veuillez entrer un nombre entier pour la quantité.")
        
        # Choix de la catégorie
        lister_categories()
        while True:
            try:
                id_categorie = int(input("Entrez l'ID de la catégorie : "))
                curseur.execute("SELECT id_categorie FROM categories WHERE id_categorie = %s", (id_categorie,))
                if curseur.fetchone():
                    break
                else:
                    print("Catégorie inexistante. Réessayez.")
            except ValueError:
                print("Veuillez entrer un nombre entier pour l'ID.")
        
        en_rupture = quantite < 5
        
        sql = """
        INSERT INTO produits (designation, prix_unitaire, quantite_stock, en_rupture, id_categorie)
        VALUES (%s, %s, %s, %s, %s)
        """
        curseur.execute(sql, (designation, prix, quantite, en_rupture, id_categorie))
        connexion.commit()
        print(f"Produit '{designation}' ajouté avec succès.")
    
    except Exception as e:
        print("Erreur lors de l'ajout du produit :", e)

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
        print("3. Ajouter un produit")
        print("4. Rechercher apprenant")
        print("5. Supprimer un apprenant")
        print("6. Quitter")
        choix = input("Votre choix : ")
        if choix == "1":
            ajouter_categorie()
        elif choix == "2":
            lister_categories()
        elif choix == "3":
            ajouter_produit()
        elif choix == "6":
            fermeture()
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide, réessayez.")

menu()