
from odoo import models, fields

class SegmentProduct(models.Model):
    _name = 'segment.product'
    _description = 'Master Data Segment Product'
    
    name = fields.Char(string='Product Segment Name', required=True)
    active = fields.Boolean(default=True)