# -*- encoding: utf-8 -*-

from email.policy import default
from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    
    url = fields.Char(string='URL', config_parameter='chatbot.url', default='localhost')
    port_number = fields.Integer(string='Port Number', config_parameter='chatbot.port_number', default=5005)
    installed_path = fields.Char(string='Installation Path', config_parameter='chatbot.installed_path')
    botToken = fields.Char(string="Chatbot Token", config_parameter='chatbot.token')
