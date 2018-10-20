# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Database Description',
    'author': 'Soltani charif',
    'version' : '1.0',
    'summary': 'Add description to database',
    'sequence': 30,
    'description': """
Database Description
====================
Odoo is a multi database application, When you create more than one database Odoo automatically redirect to you to database selecting page
The list of database will be in english without spacing. This module allow you when you create a database to add a readable name for your
application in any laguage like Arabic, chines ..etc. 
    """,
    'category': 'Web',
    'website': '',
    'depends': ['web'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
