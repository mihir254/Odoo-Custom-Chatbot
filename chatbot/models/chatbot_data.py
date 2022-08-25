# -*- encoding:utf-8 -*-

from odoo import fields, models


class ChatbotData(models.Model):

    _name = 'chatbot.data'
    _description = 'Chatbot Data consisting of Rules, Intents and Responses'

    name = fields.Char(string='Title', required=True, help='Name of the event of data loading', label='example')
    int_name = fields.Char(string='Intent Title', required=True, help='Name of the set of user intent messages')
    int_custom_message = fields.Many2many(comodel_name='custom.intent', string='Custom Intent Messages', help='Add custom messages to user intent messages')
    int_previous_message_ids = fields.Many2many(comodel_name='mail.message', string='Previous Session Messages', domain=([('model','=','mail.channel')]), help='Add messages from previous session data')
    res_name = fields.Char(string='Response Title', required=True, help='Title for the response triggered on the mentioned intent')
    res_message = fields.Char(string='Response Message',  required=True, help='Response message for the mentioned intent')
    rule_message = fields.Char(string='Rule', required=True, help='A rule for the chatbot to follow, like, Say goodbye anytime the user says goodbye')
    is_intent_loaded = fields.Boolean(string='Intent Loaded', help='Checks if this intent title has already been loaded on the chatbot')
    is_response_loaded = fields.Boolean(string='Response Loaded', help='Checks if this response title has already been loaded on the chatbot')
    is_intent_message_loaded = fields.Boolean(string='Intent Message Loaded', help='Checks if intent messages have already been loaded on the chatbot')
    is_response_message_loaded = fields.Boolean(string='Response Message Loaded', help='Checks if response message has already been loaded on the chatbot')


    def write(self, vals):
        if 'int_custom_message' in vals or 'int_previous_message_ids' in vals:
            vals['is_intent_message_loaded'] = False
        if 'res_message' in vals:
            vals['is_response_message_loaded'] = False
        return super().write(vals)
