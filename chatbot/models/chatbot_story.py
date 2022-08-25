# -*- encoding:utf-8 -*-

from odoo import fields, models


class ChatbotStory(models.Model):

    _name = 'chatbot.story'
    _description = 'Stories Based on Intents and Responses'

    name = fields.Char(string='Name of the Story', required=True, help='Name of the story')
    chatbot_data_ids = fields.Many2many(comodel_name='chatbot.data', string='Custom Chatbot Data', required=True, help='Intent Response Message combinations to prepare a bot story')
    is_story_loaded = fields.Boolean(string='Loaded', help='Checks if this story has already been loaded on the chatbot')
