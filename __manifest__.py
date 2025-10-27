{
    'name': 'PLM Production Status',
    'version': '1.0',
    'summary': 'Module to List all Merchant transaction of sale orders',
    'author': 'Akash Sagar',
    'category': 'Shipping',
    'depends': ['sale_management','product','inspection','contacts','base', 'sale', 'product','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
         'views/production.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
}
