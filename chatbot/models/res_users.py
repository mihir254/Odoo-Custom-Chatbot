# -*- encoding: utf-8 -*-

from odoo import api, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def get_company_id(self):
        company_id = self.env['res.users'].search([('id', '=', self._uid)]).company_id.id
        return company_id
