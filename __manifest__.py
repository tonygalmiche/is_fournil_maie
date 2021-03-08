# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo 14 pour Fournil & Maie',
    'version'  : '14.0.0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo 14 pour Fournil & Maie
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'purchase',
        'account',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': True,
}
