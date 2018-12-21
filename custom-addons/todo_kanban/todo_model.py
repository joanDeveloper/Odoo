#-*- coding: utf-8 -*-
from openerp import models, fields

class TodoTask(models.Model):
    _inherit = 'todo.task'
    priority = fields.Selection([
        ('0','Low'),
        ('1','Normal'),
        ('2','High')],
        'Priority',default='1')

    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Ready for next stage')],
        'Kanban State', default='normal')