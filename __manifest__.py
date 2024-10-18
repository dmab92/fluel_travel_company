# -*- coding: utf-8 -*-
{
    'name': "Transport Fluel App",

    'summary': "Module de gestion d'une entreprise de transport de produits petrolier",

    'description': """
    Module de gestion de flotte et des documents admiratifs
    Module de gestion des chauffeurs
    Module de gestion de la maintenance des véhicules
    Module des rapports, des statistiques et du tableau de bord
    
    This application enables the management of any transport company, with a specialization in fuel transportation.
It allows the management of pickup orders, reception reports, as well as handling all expenses related to a trip.
The module also automatically manages reminders for the renewal of each vehicle's administrative documents, 
after sending automatic SMS notifications as the expiration date approaches, along with many other features.
    
    
    """,

    'author': "MT CONSULTING SARL",
    'website': "https://www.mtconsultinng.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'data/data.xml',
        'views/livre_voyage.xml',
        'views/config.xml',
        'menu.xml'
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

