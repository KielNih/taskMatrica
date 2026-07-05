from odoo import models, fields

class CustomAttendance(models.Model):
    _name = 'custom.attendance' 
    _description = 'Custom Attendance Record'

    name = fields.Char(string='Nama', required=True)
    date = fields.Datetime(string='Tanggal', required=True)
    type = fields.Selection([
        ('Check In', 'Check In'),
        ('Check Out', 'Check Out')
    ], string='Tipe', required=True)
    longitude = fields.Float(string='Longitude', digits=(10, 7))
    latitude = fields.Float(string='Latitude', digits=(10, 7))