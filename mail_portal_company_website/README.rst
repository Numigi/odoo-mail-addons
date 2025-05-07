==========================
Mail Portal Company Website
==========================

Ce module permet de gérer le contexte multi-sociétés et multi-websites pour les liens vers le portail 
qui sont envoyés par courriel, par exemple pour un bon de commande ou une facture.

Le lien dans le courriel prendra en compte le site web lié à la société active au lieu d'utiliser
le paramètre système web.base.url comme c'est le cas en standard.

Configuration
============

Pour chaque société:

1. Allez dans Paramètres > Utilisateurs & Sociétés > Sociétés
2. Éditez la société concernée
3. Dans la section "Emails du portail", cochez l'option "Utiliser l'URL du site web pour les liens du portail"

Comportement
===========

Lorsque l'option est activée pour une société, tous les liens vers le portail inclus dans les courriels
utilisent l'URL du site web associé à cette société au lieu du paramètre système web.base.url.

Le système suit cette logique pour déterminer l'URL à utiliser:

1. Cherche un site web (website) lié directement à la société (même company_id)
2. Si aucun site web n'est trouvé mais que la société a un champ website rempli, utilise cette valeur
3. En dernier recours, utilise le paramètre système web.base.url

Contributeurs
============

* Numigi (tm) et ses contributeurs

Plus d'information
=================

* Rencontrez-nous sur https://bit.ly/numigi-com