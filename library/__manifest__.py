{
    'name': 'Library',
    'author': 'Shafi Pk',
    'version': '16.0.1.0.0',
    'depends': ['base'],
    'description': 'Information related to book.',
    'category': 'Library',
    'application': True,
    'installable': True,
    'auto_install': False,
    'data': [
        'security/librarian.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_publisher_views.xml',
        'views/library_book_category.xml',
        'views/library_book_menus.xml',
    ],
}
