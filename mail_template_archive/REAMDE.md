# Mail Template Archive

Ce module ajoute la possibilité d'archiver des modèles de courriel dans Odoo 12.0, en ajoutant un champ "Actif/Inactif" sur le modèle `mail.template`.

## Table des matières
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Contributeurs](#contributeurs)
- [Licence](#licence)

## Fonctionnalités

- Ajoute un champ "Actif" aux modèles de courriel
- Permet d'archiver des modèles de courriel sans les supprimer
- Filtre pour afficher/masquer les modèles archivés

## Installation

1. Clonez ce dépôt dans votre répertoire d'addons Odoo:
```bash
cd /path/to/odoo/addons
git clone [URL_DU_DEPOT] mail_template_archive
```

2. Mettez à jour la liste des modules dans Odoo:
   - Activez le mode développeur
   - Allez dans Applications > Mettre à jour la liste des applications

3. Recherchez "Mail Template Archive" et installez le module

## Configuration

Aucune configuration spécifique n'est nécessaire après l'installation du module.

## Utilisation

### Archiver un modèle de courriel

1. Allez dans **Paramètres > Technique > Email > Modèles d'email**
2. Dans la liste des modèles, utilisez le bouton bascule dans la colonne "Actif" pour archiver un modèle (désactivé) ou le restaurer (activé)
3. Dans le formulaire du modèle, vous pouvez également utiliser le bouton bascule "Actif" en haut du formulaire

### Afficher les modèles archivés

1. Allez dans **Paramètres > Technique > Email > Modèles d'email**
2. Utilisez le filtre "Archivés" dans la barre de recherche pour afficher uniquement les modèles archivés

## Contributeurs

* Votre Entreprise <contact@yourcompany.com>

## Licence

Ce module est sous licence LGPL-3.0 (http://www.gnu.org/licenses/lgpl).
