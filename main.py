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



# Fonction pour effectuer un mouvement de stock
def mouvement_stock():
    try:
        # Lister les produits disponibles
        curseur.execute("SELECT id_produit, designation, quantite_stock FROM produits")
        produits = curseur.fetchall()
        if not produits:
            print("Aucun produit trouvé.")
            return
        
        print("\n--- Liste des produits ---")
        for pid, nom, stock in produits:
            print(f"{pid} - {nom} (Stock: {stock})")
        
        # Choix du produit
        while True:
            try:
                id_produit = int(input("Entrez l'ID du produit : "))
                curseur.execute("SELECT id_produit FROM produits WHERE id_produit = %s", (id_produit,))
                if curseur.fetchone():
                    break
                else:
                    print("Produit inexistant, réessayez.")
            except ValueError:
                print("Veuillez entrer un nombre entier pour l'ID.")
        
        # Choix du type de mouvement
        while True:
            type_mouvement = input("Type de mouvement (ENTREE / SORTIE) : ").strip().upper()
            if type_mouvement in ["ENTREE", "SORTIE"]:
                break
            else:
                print("Choix invalide. Tapez 'ENTREE' ou 'SORTIE'.")
        
        # Quantité
        while True:
            try:
                quantite = int(input("Entrez la quantité : "))
                if quantite > 0:
                    break
                else:
                    print("La quantité doit être positive.")
            except ValueError:
                print("Veuillez entrer un nombre entier pour la quantité.")
        
        # Vérifier stock pour une sortie
        if type_mouvement == "SORTIE":
            curseur.execute("SELECT quantite_stock FROM produits WHERE id_produit = %s", (id_produit,))
            stock = curseur.fetchone()[0]
            if stock < quantite:
                print("Stock insuffisant ! Mouvement annulé.")
                return
        
        # Ajouter le mouvement
        curseur.execute(
            "INSERT INTO mouvements (id_produit, type_mouvement, quantite) VALUES (%s, %s, %s)",
            (id_produit, type_mouvement, quantite)
        )
        
        # Mettre à jour le stock
        if type_mouvement == "ENTREE":
            curseur.execute(
                "UPDATE produits SET quantite_stock = quantite_stock + %s WHERE id_produit = %s",
                (quantite, id_produit)
            )
        else:
            curseur.execute(
                "UPDATE produits SET quantite_stock = quantite_stock - %s WHERE id_produit = %s",
                (quantite, id_produit)
            )
        
        # Mettre à jour en_rupture
        curseur.execute(
            "UPDATE produits SET en_rupture = quantite_stock < 5 WHERE id_produit = %s",
            (id_produit,)
        )
        
        # Valider la transaction
        connexion.commit()
        print(f"Mouvement '{type_mouvement}' de {quantite} unités effectué pour le produit {id_produit}.")
    
    except Exception as e:
        print("Erreur MySQL :", e)



# Lister tous les produits avec leur catégorie
def lister_produits():
    try:
        sql = """
        SELECT p.designation, p.prix_unitaire, p.quantite_stock, c.nom_categorie
        FROM produits p
        JOIN categories c ON p.id_categorie = c.id_categorie
        """
        curseur.execute(sql)
        produits = curseur.fetchall()
        
        if not produits:
            print("Aucun produit trouvé.")
            return
        
        print("\n--- Liste des produits ---")
        for nom, prix, stock, cat in produits:
            print(f"{nom} - Prix: {prix:.2f} - Stock: {stock} - Catégorie: {cat}")
    
    except Exception as e:
        print("Erreur MySQL :", e)


# Lister les produits en alerte (stock < 5)
def produits_en_alerte():
    try:
        sql = "SELECT designation, quantite_stock FROM produits WHERE quantite_stock < 5"
        curseur.execute(sql)
        alertes = curseur.fetchall()
        
        if not alertes:
            print("Aucun produit en rupture ou en faible stock.")
            return
        
        print("\n--- Produits en alerte (stock < 5) ---")
        for nom, stock in alertes:
            print(f" {nom} - Stock = {stock}")
    
    except Exception as e:
        print(" Erreur MySQL :", e)

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
        print("4. Effectuer un mouvement")
        print("5. Lister les produits")
        print("6. Produits en alerte")
        print("7. Quitter")
        choix = input("Votre choix : ")
        if choix == "1":
            ajouter_categorie()
        elif choix == "2":
            lister_categories()
        elif choix == "3":
            ajouter_produit()
        elif choix == "4":
            mouvement_stock()
        elif choix == "5":
            lister_produits()
        elif choix == "6":
            produits_en_alerte()
        elif choix == "7":
            fermeture()
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide, réessayez.")

menu()