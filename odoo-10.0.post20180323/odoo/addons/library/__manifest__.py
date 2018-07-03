# -*- coding: utf-8 -*-
{
    'name': "library",

    'summary': """
        Odoo module for a library""",

    'description': """
        Odoo module for a library
        by Mikel López
    """,

    'author': "Mikel López",
    'website': "http://github.com/mlvillarroya",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/message_wizard.xml',
        'wizard/return_loan.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}