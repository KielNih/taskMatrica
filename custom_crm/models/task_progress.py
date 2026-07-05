from odoo import models, fields

class TaskProgress(models.Model):
    _name = 'task.progress'
    lead_id = fields.Many2one('crm.lead', string='Lead/Opportunity', required=True, ondelete='cascade')
    
    name = fields.Char(string='Task', required=True)
    deadline_date = fields.Date(string='Deadline')
    state = fields.Selection([
        ('todo', 'To do'),
        ('progress', 'Progress'),
        ('done', 'Done')
    ], string='Status', default='todo', required=True)