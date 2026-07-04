# -*- coding: utf-8 -*-
{
    'name': 'School Management',
    'version': '19.0.1.0.0', 
    'summary': 'Sistem Informasi Manajemen Sekolah untuk Odoo 19',
    'description': """
        Modul custom untuk mengelola data Guru, Siswa, Kelas, Mata Pelajaran, dan Jadwal.
        Sesuai dengan blueprint ERD dan arsitektur Odoo 19 modern.
    """,
    'author': 'Hezkiel Chris Tangkilisan',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_menus.xml',
        'views/teacher_views.xml',
        'views/class_views.xml',
        'views/subject_views.xml',
        'views/student_views.xml',
        'views/schedule_views.xml',
        'reports/school_action_report.xml',
        'reports/student_card_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}