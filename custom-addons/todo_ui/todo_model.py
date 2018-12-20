#-*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons.base.res import res_request
from openerp.exceptions import ValidationError

def referencable_models(self):
    return res_request.referencable_models(self, self.env.cr, self.env.uid, context=self.env.context)

class Tag(models.Model):
    _name = 'todo.task.tag'
    name = fields.Char('Name', size=40, translate=True)
    #Tag class relación a Tasks:
    task_ids = fields.Many2many( 'todo.task', string='Tasks')
    
    _parent_store = True #soporte busquedas jerarquicas
    parent_id     = fields.Many2one('todo.task.tag','Parent Tag', ondelete='restrict')
    parent_left   = fields.Integer('Parent Left', index=True)
    parent_right  = fields.Integer('Parent  Right', index=True)
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')

class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'
    # Campos de cadena de caracteres:
    name  = fields.Char('Name',size=40)
    desc  = fields.Text('Description')
    state = fields.Selection([('draft','New'),('open','Started'), ('done','Closed')],'State')
    docs  = fields.Html('Documentation')

    # Campos numéricos:
    sequence      = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete',(3,2))

    # Campos de fecha:
    date_effective = fields.Date('Effective Date')
    date_changed   = fields.Datetime('Last Changed')

    # Otros campos:
    fold  = fields.Boolean('Folded?')
    image = fields.Binary('Image')

    task_ids = fields.One2many('todo.task', 'stage_id', 'Tasks')

class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', 'todo_task_tag_rel','task_id','tag_id', string='Tags')
    refers_to = fields.Reference(referencable_models,'Refers to')
    stage_fold = fields.Boolean('Stage Folded?', compute='_compute_stage_fold', search='_search_stage_fold', inverse ='_write_stage_fold')
    stage_state = fields.Selection(related='stage_id.state', string='Stage State')

    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
    	self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    _sql_constraints = [
    	('todo_task_name_uniq',
         'UNIQUE (name, user_id, active)',
         'Task title must be unique!')]

    @api.constrains('name')
    def _check_name_size(self):
    	if len(self.name) < 5:
        	raise ValidationError('Must have 5 chars!')



