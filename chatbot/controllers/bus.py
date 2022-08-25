# -*- encoding:utf-8 -*-

from odoo import http, tools
from odoo.http import request, route
from odoo.addons.mail.controllers.bus import MailChatController


class MailChatControllerInherit(MailChatController):
    @route('/mail/chat_post', type="json", auth="public", cors="*")
    def mail_chat_post(self, uuid, message_content, **kwargs):

        mail_channel = request.env["mail.channel"].sudo().search([('uuid', '=', uuid)], limit=1)
        if not mail_channel:
            return False
        bot_response = "Bot response"
        if request.session.uid:
            author = request.env['res.users'].sudo().browse(request.session.uid).partner_id
            bot_id = request.env['res.partner'].sudo().search([('name','=','Custom Bot')])
            if bot_response in message_content:
                message_content = message_content[12:]
                author_id = bot_id['id']
            else:
                author_id = author.id
            email_from = author.email_formatted
        else:
            bot_id = request.env['res.partner'].sudo().search([('name','=','Custom Bot')])
            if bot_response in message_content:
                message_content = message_content[12:]
                author_id = bot_id['id']
            else:
                author_id = False
            email_from = mail_channel.anonymous_name or mail_channel.create_uid.company_id.catchall_formatted
        body = tools.plaintext2html(message_content)
        message = mail_channel.with_context(mail_create_nosubscribe=True).message_post(
            author_id=author_id,
            email_from=email_from,
            body=body,
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )
        return message.id if message else False

    @http.route('/custombot/getBotID', type='json', auth="public", cors="*")
    def getBotID(self):
        bot_id = request.env['res.partner'].sudo().search([('name','=','Custom Bot')]).id
        return bot_id
