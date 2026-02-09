# Application de Gestion de Stock – Structure Solidaire

## Contexte du projet

Une structure solidaire (type Simplon) gère un stock important de matériel informatique.  
Elle doit pouvoir :

- Connaître l’état actuel de son stock
- Suivre précisément chaque entrée et sortie de matériel
- Éviter les pertes, erreurs ou vols grâce à une historisation fiable

Ce projet a pour objectif de concevoir une application back-end capable de manipuler des données structurées, d’appliquer une logique métier cohérente et d’assurer la persistance des données via une base de données relationnelle MySQL.

---

## Objectifs pédagogiques

- Concevoir une base de données relationnelle normalisée (3FN)
- Mettre en place une intégrité référentielle
- Implémenter une logique métier de gestion de stock
- Historiser les mouvements de stock
- Gérer proprement les erreurs de connexion à la base de données
- Utiliser Python pour interagir avec MySQL

---

## Technologies utilisées

- **Python 3**
- **MySQL**
- **mysql-connector-python**
- **Git / GitHub**

---

## Modélisation de la base de données

### Schéma logique (MLD)

La base de données est composée de **3 tables principales** :

### `categories`
- `id_categorie` (PK)
- `nom_categorie`

### `produits`
- `id_produit` (PK)
- `designation`
- `prix_unitaire`
- `quantite_stock`
- `en_rupture`
- `id_categorie` (FK)

### `mouvements`
- `id_mouvement` (PK)
- `id_produit` (FK)
- `type_mouvement` (ENTREE / SORTIE)
- `quantite`
- `date_mouvement`

La table `mouvements` joue le rôle de **table d’historisation** des entrées et sorties de stock.

---

## Intégrité référentielle

- Un produit doit obligatoirement être rattaché à une catégorie existante
- Il est impossible de supprimer une catégorie si elle contient des produits
- Les mouvements sont toujours liés à un produit existant

---

## Fonctionnalités implémentées

### Gestion des catégories
- Ajouter une catégorie
- Lister les catégories existantes

### Gestion des produits
- Ajouter un produit en l’associant à une catégorie
- Calcul automatique du statut `en_rupture` si le stock est inférieur à 5

### Gestion des mouvements de stock
- Ajouter une entrée ou une sortie de stock
- Création automatique d’une ligne dans la table `mouvements`
- Mise à jour du stock en temps réel
- Vérification du stock avant une sortie

### Consultation
- Afficher la liste des produits avec leur catégorie
- Afficher les produits dont le stock est inférieur à 5 (alerte)

---

## Logique métier

- Le stock courant est stocké dans la table `produits`
- L’historique des opérations est stocké dans la table `mouvements`
- Toute modification du stock passe obligatoirement par un mouvement
- La date du mouvement est automatiquement enregistrée

---

## Gestion des erreurs

- Gestion des erreurs de connexion MySQL via `try/except`
- Messages explicites en cas de problème (connexion, stock insuffisant, etc.)

---

## Lancement du projet

1. Créer la base de données MySQL
2. Exécuter le script SQL de création des tables
3. Installer la dépendance :
   ```bash
   pip install mysql-connector-python
