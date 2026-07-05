{
    'name': 'Custom CRM ',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Modifikasi form Pipeline CRM untuk assessment',
    'description': """
        Module ini menambahkan custom fields pada form Pipeline (crm.lead),
        menambahkan master data Segment Product, dan Task Progress.
    """,
    'author': 'Hezkiel Chris Tangkilisan',
    'depends': ['crm'], 
    'data': [
        'security/ir.model.access.csv',
        'views/segment_product_views.xml',
        'views/crm_lead_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}