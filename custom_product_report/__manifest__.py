{
    'name': 'Custom Product Sales & Purchase Report',
    'version': '19.0.1.0.0',
    'summary': 'Generate Excel report for product sales and purchases within a date range.',
    'category': 'Sales/Reporting',
    'author': 'Hezkiel Chris Tangkilisan',
    'depends': [
        'base',
        'sale',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_report_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}