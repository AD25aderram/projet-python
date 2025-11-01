# Application de Gestion des Notes

Une application desktop simple pour gérer les notes des étudiants en Python et C.

## Fonctionnalités

-  Authentification sécurisée des professeurs
-  Ajout et modification des notes pour deux modules (Python et C)
-  Export des notes au format CSV
-  Gestion multi-utilisateurs (plusieurs professeurs)

## Prérequis

- Python 3.x
- Bibliothèques Python :
  - tkinter (interface graphique)
  - csv (module standard pour l'export au format CSV)
  - sqlite3 (base de données)

## Installation

1. Clonez ou téléchargez ce dépôt
2. Assurez-vous que Python est installé sur votre système
3. Lancez l'application :
```bash
python main.py
```

## Utilisation

1. **Connexion** :
   - Utilisez vos identifiants professeur pour vous connecter
   - Identifiants par défaut disponibles dans `main.py`

2. **Navigation** :
   - Choisissez le module (Python ou C)
   - Sélectionnez l'action souhaitée (Ajouter/Modifier/Exporter)

3. **Gestion des notes** :
   - Ajout : Entrez les notes pour tous les étudiants
   - Modification : Modifiez une note spécifique
   - Export : Générez un fichier CSV des notes

## Structure du Projet

- `main.py` : Point d'entrée de l'application
- `my_functions.py` : Fonctions principales et interface graphique
- `base_de_donnees.db` : Base de données SQLite (créée automatiquement)
- `exported_notes_*.csv` : Fichiers d'export des notes

## Notes Techniques

- Interface légère et réactive : fenêtres redimensionnables avec dispositions adaptatives et tailles minimales pour conserver une bonne lisibilité
- Base de données SQLite pour le stockage persistant
- Export des données au format CSV
