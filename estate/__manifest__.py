{
    'name': 'Real estate',
    'summary': 'Manage real estate properties and listings.',
    'description': ''' Manage real estate properties and listings''',
    'version': '16.0.1.0.0',
    'author': 'shafi pk',
    'category': 'Real estate',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag.xml',
        'views/res_users_form.xml',
        'views/estate_menu.xml',
        'views/estate_property_offer.xml'
    ],
    'images': ['static/description/icon.png'],
}
