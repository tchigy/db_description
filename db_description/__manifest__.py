# -*- coding: utf-8 -*-
{
    'name' : 'Database Description',
    'author': 'Soltani charif',
    'version' : '1.0',
    'summary': 'Add description to database',
    'sequence': 30,
    'description': """
Database Description
====================
Odoo is a multti database application, When you create more than one database Odoo automatically redirect to you to database selecting page
The list of database will be in english without spacing. This module allow you when you create a database to add a readable name for your
application in any laguage like Arabic, chines ..etc. 
    """,
    'category': 'Web',
    'website': '',
    'depends': ['web'],
    'images': [
        'static/src/img/main_screenshot.png'
    ],
    'data': [
        'views/webclient_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
