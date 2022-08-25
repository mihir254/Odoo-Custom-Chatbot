# -*- encoding:utf-8 -*-

from odoo import fields, models


class CustomIntent(models.Model):

    _name = 'custom.intent'
    _description = 'storing the custom intent message for a defined intent'

    name = fields.Char(string='Message', required=True, help='Custom intent message for the bot')
