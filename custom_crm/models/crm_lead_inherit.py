# models/crm_lead.py
from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_new_customer = fields.Boolean(string='Pelanggan Baru')
    customer_segment = fields.Selection([
        ('konstruksi', 'Konstruksi'),
        ('perbankan', 'Perbankan'),
        ('pemerintah', 'Pemerintah'),
        ('bumd_bumn', 'BUMD/BUMN'),
        ('kementrian', 'Kementrian'),
        ('swasta_lainnya', 'Swasta Lainnya')
    ], string='Segment Pelanggan')
    
    other_customer_segment = fields.Char(string='Segment Pelanggan Lainnya')
    segment_product_id = fields.Many2one('segment.product', string='Segment Product')
    task_progress_ids = fields.One2many('task.progress', 'lead_id', string='Task Progress')