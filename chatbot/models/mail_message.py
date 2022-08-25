# -*- encoding:utf-8 -*-

from odoo import fields, models


class MailMessage(models.Model):
    
    _inherit = 'mail.message'
    
    body = fields.Html(string='Message')
