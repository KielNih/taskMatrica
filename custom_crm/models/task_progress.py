# models/task_progress.py
from odoo import models, fields

class TaskProgress(models.Model):
    _name = 'task.progress'
    _description = 'Task Progress for CRM Pipeline'
    lead_id = fields.Many2one('crm.lead', string='Lead/Opportunity', required=True, ondelete='cascade')
    
    name = fields.Char(string='Task', required=True)
    deadline_date = fields.Date(string='Deadline')
    state = fields.Selection([
        ('todo', 'To do'),
        ('progress', 'Progress'),
        ('done', 'Done')
    ], string='Status', default='todo', required=True)