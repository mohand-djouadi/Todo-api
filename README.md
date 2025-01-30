# Mon Projet Django

Un projet Django API Restfull conçu pour la gestion des tâches. Ce projet utilise PostgreSQL comme base de données et suit les meilleures pratiques de sécurité pour le déploiement.

---

## 📂 Applications et Fonctionnalités
### Authentication

- [x] Connexion et inscription, deconnexion
- [x] Changer mot de passe tant que utilisateur
- [x] changee mot de passe apres identifier avec OTP ou reponse de security

### Task
- [x] Création, lecture, mise à jour et suppression (CRUD) des données.
- [x] Requete security en verification authenticite d'utilisateur, validation JWT token 
- [x] Gestion des relations entre les modèles (par exemple, utilisateurs, tâches, commantaires).


---

## 🚀 Technologies Utilisées

- **Backend** : Django 4.x
- **Base de données** : PostgreSQL
- **Langage** : Python 3.x
- **Outils supplémentaires** :
  - `python-decouple` pour la gestion des variables d'environnement.
  - SQLite (pour le développement initial).
  - `PyJWT` pour l'authentification avec des token JWT 

---

## 📦 Installation et Configuration

### Prérequis

1. **Python** (version 3.8 ou supérieure).
2. **PostgreSQL** (installé et configuré).
3. **Pipenv** ou `pip` pour la gestion des dépendances.

---

### Étapes d'installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/mohand-djouadi/Todo-api.git
2. Installer les dependences :
   ```bash
   pip install requirements.txt
