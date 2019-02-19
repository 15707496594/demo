# -*- coding: utf-8 -*-
{
    'name': "Demo Account",

    'summary': """Demo Account""",

    'description': """
        Demo Account
    """,

    'author': "ZYH",
    'website': "http://www.demo.com",

    "category": "account",
    "installable": True,
    'version': '0.1',
    'depends': ["demo_base"],
    'qweb': [
    ],
    'data': [
        "security/res_group.xml",
        "security/ir.model.access.csv",
        "data/action.xml",
        "data/menu.xml",
        "views/demo_account_journal.xml"
    ],
    'demo': [
    ]
}
