# -*- coding: utf-8 -*-
{
    'name': "Demo Base",

    'summary': """Demo Base""",

    'description': """
        Demo Base
    """,

    'author': "ZYH",
    'website': "http://www.demo.com",

    "category": "sys",
    "installable": True,
    'version': '0.1',
    'depends': ["base"],
    'qweb': [
    ],
    'data': [
        'security/ir.model.access.csv',
        "data/action.xml",
        "data/menu.xml",
        "views/demo_lookup.xml"
    ],
    'demo': [
    ]
}
