
from odoo import models, fields

class SegmentProduct(models.Model):
    _name = 'segment.product'
    
    name = fields.Char(string='Product Segment Name', required=True)
    active = fields.Boolean(default=True)