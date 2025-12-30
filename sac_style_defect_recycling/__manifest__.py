# -*- coding: utf-8 -*-
{
    'name': "Gestion des sacs et suivi des défauts",
    'summary': "Module complet pour la gestion de l'inventaire des sacs, le suivi des défauts et le recyclage.",
    'description': """
Gestion des Sacs et Recyclage
=============================
Ce module permet une gestion moderne et efficace de votre inventaire de sacs :
- Enregistrement détaillé des sacs (types, matières, dimensions).
- Suivi rigoureux des états (Nouveau, En Stock, Vendu, À Recycler).
- Gestion des défauts et de la qualité.
- Historique complet des mouvements et activités.
- Impression d'étiquettes avec codes-barres.
- Analyses statistiques via vues Graphique et Pivot.
    """,
    'author': "Khadija",
    'website': "https://www.votre-site.com", # Optionnel
    'category': 'Inventory/Inventory',
    'version': '1.1',
    
    # Dépendances indispensables
    # 'mail' est requis pour le chatter et les activités
    # 'account' et 'stock' pourraient être ajoutés si vous utilisez les champs facture/livraison
    'depends': ['base', 'mail'],

    # Fichiers de données à charger
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sac_views.xml',
    ],
    
    # Paramètres d'installation
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    
    # Icône du module (si vous avez le fichier )
    'assets': {
        'web.assets_backend': [
            # Ajoutez ici vos fichiers CSS/JS personnalisés si nécessaire
        ],
    },
}
