# Mon Projet Django

Un projet Django conçu pour la gestion des tâches. Ce projet utilise PostgreSQL comme base de données et suit les meilleures pratiques de sécurité pour le déploiement.

---

## 📂 Fonctionnalités

- [x] Création, lecture, mise à jour et suppression (CRUD) des données.
- [x] Authentification des utilisateurs (connexion et inscription).
- [x] Gestion des relations entre les modèles (par exemple, utilisateurs, tâches).
- [x] Migration automatique de SQLite vers PostgreSQL.
- [x] Séparation des secrets avec un fichier `.env`.

---

## 🚀 Technologies Utilisées

- **Backend** : Django 4.x
- **Base de données** : PostgreSQL
- **Langage** : Python 3.x
- **Outils supplémentaires** :
  - `python-decouple` pour la gestion des variables d'environnement.
  - SQLite (pour le développement initial).

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
