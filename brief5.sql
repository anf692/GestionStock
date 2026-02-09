create database gestion_stock;
use gestion_stock;


CREATE TABLE categories (
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE produits (
    id_produit INT AUTO_INCREMENT PRIMARY KEY,
    designation VARCHAR(150) NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    quantite_stock INT NOT NULL DEFAULT 0,
    en_rupture BOOLEAN NOT NULL DEFAULT FALSE,
    id_categorie INT NOT NULL,

    CONSTRAINT fk_produit_categorie
        FOREIGN KEY (id_categorie)
        REFERENCES categories(id_categorie)
);


CREATE TABLE mouvements (
    id_mouvement INT AUTO_INCREMENT PRIMARY KEY,
    id_produit INT NOT NULL,
    type_mouvement ENUM('ENTREE', 'SORTIE') NOT NULL,
    quantite INT NOT NULL,
    date_mouvement DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_mouvement_produit
        FOREIGN KEY (id_produit)
        REFERENCES produits(id_produit)
);

select * from mouvements;


ALTER TABLE produits
DROP COLUMN en_rupture;
