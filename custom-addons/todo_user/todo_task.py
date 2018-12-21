#-*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task','mail.thread']
    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')
    name = fields.Char(help="What needs to be done?")
    @api.multi
    def do_clear_done(self):
        domain = [('is_done', '=', True), '|', ('user_id', '=', self.env.uid), ('user_id', '=', False)]
        done_recs = self.search(domain)
        done_recs.write({'active': False})
        return True
    @api.one
    def do_toggle_done(self):
        if self.user_id != self.env.user:
            raise Exception('Only the responsible can do this!')
        else:
            return super(TodoTask, self).do_toggle_done()

    @api.model 
    def create(self, vals):
        _logger.info("entra en create todoTask")
        # Code before create
        # Can use the `vals
        return super(TodoTask, self).create(vals)
        # Code after create
        # Can use the `new` record created