{
    'name': 'Custom Attendance API',
    'version': '19.0.1.0.0',
    'summary': 'API endpoint for custom attendance check in/out',
    'description': 'Provide GET and POST API for custom attendance records.',
    'category': 'Customizations',
    'author': 'Hezkiel Chris T',
    'depends': ['base'], 
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
}