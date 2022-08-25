# -*- encoding:utf-8 -*-

import json
import requests
import yaml

from odoo import api, exceptions, fields, models
from odoo.tools import html2plaintext


class ChatbotLoad(models.Model):

    _name = 'chatbot.load'
    _description = 'Load train data from database to chatbot yamls'

    name = fields.Char(string='Title / Purpose', help='Purpose of the loading event', required=True)
    desc = fields.Char(string='Description', help='Event description')
    create_date = fields.Datetime(string='Trained On')
    model_file_name = fields.Char(string='Model File Name', help='Name of the trained mo`del')
    is_model_loaded = fields.Boolean(string='Loaded Model', default=False, help='Shows if this model is in use or inactive')
    is_data_loaded = fields.Boolean(string='Loaded Data', default=False, help='Checks if the data has been loaded to external files')
    is_model_trained = fields.Boolean(string='Trained Model', default=False, help='Checks ig the model has already been trained')

    @api.model
    def getURL(self):
        url = self.env['ir.config_parameter'].sudo().get_param('chatbot.url')
        if not url:
            raise exceptions.UserError('Please set the chatbot url in Configuration->Settings->Chatbot')
        return url
    
    @api.model
    def getBotID(self):
        botID = self.env['res.partner'].sudo().search([('name', '=', 'Custom Bot')]).id
        if not botID:
            raise exceptions.UserError('Please set the chatbot url in Configuration->Settings->Chatbot')
        return botID
        
    @api.model
    def getPort(self):
        port = self.env['ir.config_parameter'].sudo().get_param('chatbot.port_number')
        if not port:
            raise exceptions.UserError('Please set the chatbot port in Configuration->Settings->Chatbot')
        return port
        
    @api.model
    def getToken(self):
        token = self.env['ir.config_parameter'].sudo().get_param('chatbot.token')
        print("\n\n", token, "\n\n")
        if not token:
            raise exceptions.UserError('Please set the chatbot token in Configuration->Settings->Chatbot')
        return token

    def getPath(self):
        path = self.env['ir.config_parameter'].sudo().get_param('chatbot.installed_path')
        if not path:
            raise exceptions.UserError('Please set the chatbot path in Configuration->Settings->Chatbot')
        return path

    def onChatbotLoadData(self):
        '''Loads existing chatbot data and appends
        the custom data to it.'''
        path = self.getPath()
        if path[0] != '/':
            path = '/' + path
        if path[-1] != '/':
            path += '/'
        try:
            domain = open(path + 'domain.yml', 'r+')
            domain_file_data = yaml.safe_load(domain)
        except:
            raise exceptions.UserError(self.fileLoadError('domain.yml'))
        try:
            nlu = open(path + 'data/nlu.yml', 'r+')
            nlu_file_data = yaml.safe_load(nlu)
        except:
            raise exceptions.UserError(self.fileLoadError('nlu.yml'))
        try:
            stories = open(path + 'data/stories.yml', 'r+')
            stories_file_data = yaml.safe_load(stories)
        except:
            raise exceptions.UserError(self.fileLoadError('stories.yml'))
        try:
            rules = open(path + 'data/rules.yml', 'r+')
            rules_file_data = yaml.safe_load(rules)
        except:
            raise exceptions.UserError(self.fileLoadError('rules.yml'))
        custom_data = self.env['chatbot.data'].search([('is_intent_loaded', '=', False), ('is_response_loaded', '=', False)])
        custom_intent_title = self.env['chatbot.data'].search([('is_intent_loaded', '=', False)])
        custom_intents = self.env['chatbot.data'].search([('is_intent_message_loaded', '=', False)])
        custom_responses = self.env['chatbot.data'].search([('is_response_message_loaded', '=', False)])
        domain_file_data = self.appendToDomain(domain_file_data, custom_intent_title, custom_responses)
        nlu_file_data = self.appendToNLU(nlu_file_data, custom_intents)
        stories_file_data = self.appendToStories(stories_file_data)
        rules_file_data = self.appendToRules(rules_file_data, custom_data)
        files = [(domain, domain_file_data), (nlu, nlu_file_data), (stories, stories_file_data), (rules, rules_file_data)]
        self.onFileCompleteAppend(files)
        self.is_data_loaded = True

    def onChatbotTrain(self):
        '''Trains the chatbot on the newly loaded data'''
        path = self.getPath()
        if path[-1] != '/':
            path += '/'
        domain = yaml.safe_load(open(path + 'domain.yml', 'r'))
        nlu = yaml.safe_load(open(path + 'data/nlu.yml', 'r'))
        stories = yaml.safe_load(open(path + 'data/stories.yml', 'r'))
        rules = yaml.safe_load(open(path + 'data/rules.yml', 'r'))
        nlu = self.checkVersionkey(nlu)
        stories = self.checkVersionkey(stories)
        rules = self.checkVersionkey(rules)
        domain_yaml = yaml.dump(domain, default_flow_style=False)
        nlu_yaml = yaml.dump(nlu, default_flow_style=False)
        stories_yaml = yaml.dump(stories, default_flow_style=False)
        rules_yaml = yaml.dump(rules, default_flow_style=False)
        userURL = self.getURL()
        port = self.getPort()
        payload = domain_yaml + '\n' + nlu_yaml + '\n' + stories_yaml + '\n' + rules_yaml
        url = 'http://'+userURL+':'+port+'/model/train?token='+self.getToken()
        headers = {
        'Content-Type': 'application/x-yaml'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                self.model_file_name = response.headers['filename']
                self.is_model_trained = True
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise exceptions.UserError('Http Error: {}'.format(errh))
        except requests.exceptions.ConnectionError as errc:
            raise exceptions.UserError('Error Connecting: {}'.format(errc))
        except requests.exceptions.Timeout as errt:
            raise exceptions.UserError('Timeout Error: {}'.format(errt))
        except requests.exceptions.RequestException as err:
            raise exceptions.UserError('Oops: Something Else {}'.format(err))


    def onChatbotModelLoad(self):
        '''Loads this model as the chatbot's current model'''
        userURL = self.getURL()
        port = self.getPort()
        url = 'http://'+userURL+':'+port+'/model?token='+self.getToken()
        payload = json.dumps({
        'model_file': './models/'+self.model_file_name
        })
        headers = {
        'Content-Type': 'application/json'
        }
        try:
            response = requests.put(url, headers=headers, data=payload)
            if response.status_code == 204:
                rec = self.env['chatbot.load'].search([('is_model_loaded', '=', True)])
                rec.update({
                    'is_model_loaded': False
                })
                self.is_model_loaded = True
                response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise exceptions.UserError('Http Error: {}'.format(errh))
        except requests.exceptions.ConnectionError as errc:
            raise exceptions.UserError('Error Connecting: {}'.format(errc))
        except requests.exceptions.Timeout as errt:
            raise exceptions.UserError('Timeout Error: {}'.format(errt))
        except requests.exceptions.RequestException as err:
            raise exceptions.UserError('OOps: Something Else {}'.format(err))

    def fileLoadError(self, filename):
        return 'Something went wrong. Maybe the file path is incorrect. Could not load the ' + filename + ' file.'

    def appendToDomain(self, filedata, custom_intent_title, custom_responses):
        intent_names, responses = [], []
        for rec in custom_intent_title:
            intent_names.append('_'.join(rec['int_name'].split(' ')))
            rec.update({
                'is_intent_loaded': True
            })
        for rec in custom_responses:
            responses.append(['utter_' + '_'.join(rec['res_name'].split(' ')), rec['res_message']])
            rec.update({
                'is_response_loaded': True,
                'is_response_message_loaded': True
            })
        for intent in intent_names:
            filedata['intents'].append(str(intent))
        for response in responses:
            filedata['responses'][response[0]] = [{ 'text': response[1] }]
        return filedata

    def appendToNLU(self, filedata, custom_intents):
        for rec in custom_intents:
            intents_messages = ''
            int_name = '_'.join(rec['int_name'].split(' '))
            custom_int = self.env['custom.intent'].search([('id','in',rec['int_custom_message'].ids)])
            loaded_int = self.env['mail.message'].search([('id','in',rec['int_previous_message_ids'].ids)])
            for cus_int in custom_int:
                intents_messages += '- ' + cus_int['name'] + '\n'
            for load_int in loaded_int:
                if len(html2plaintext(load_int['body']).strip()) > 0:
                    intents_messages += '- ' + html2plaintext(load_int['body']) + '\n'
            rec.update({
                'is_intent_message_loaded': True
            })
            intent_found = 0
            for intent in filedata['nlu']:
                if intent['intent'] == int_name:
                    intent['examples'] = intents_messages
                    intent_found = 1
                    break
            if intent_found == 0:
                filedata['nlu'].append({
                    'intent': int_name,
                    'examples': intents_messages
                })
        return filedata

    def appendToStories(self, filedata):
        story_data = self.env['chatbot.story'].search([('is_story_loaded', '=', False)])
        for rec in story_data:
            story_name = rec['name']
            cus_data = self.env['chatbot.data'].search([('id','in',rec['chatbot_data_ids'].ids)])
            story_steps = []
            for ir in cus_data:
                story_steps.append({
                    'intent': '_'.join(ir['int_name'].split(' '))
                })
                story_steps.append({
                    'action': 'utter_' + '_'.join(ir['res_name'].split(' '))
                })
            filedata['stories'].append({
                'story': story_name,
                'steps': story_steps
            })
            rec.update({
                'is_story_loaded': True
            })
        return filedata
    
    def appendToRules(self, filedata, custom_data):
        for rec in custom_data:
            filedata['rules'].append({
                'rule': rec['rule_message'],
                'steps': [{'intent': '_'.join(rec['int_name'].split(' '))}, {'action': 'utter_' + '_'.join(rec['res_name'].split(' '))}]
            })
        return filedata

    def onFileCompleteAppend(self, files):
        for eachFile in files:
            eachFile[0].seek(0)
            yaml.dump(eachFile[1], eachFile[0])
            eachFile[0].truncate()
            eachFile[0].close()

    def checkVersionkey(self, filename):
        try:
            del filename['version']
        except KeyError:
            pass
        return filename
