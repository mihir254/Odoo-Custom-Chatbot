# -*- encoding:utf-8 -*-

{
    'name': 'Customizable Chatbot',
    'version': '1.1',
    'summary': 'One For All Chabtbot - Complete Customization',
    'description': """
        task_id: 2884834
        The chatbot is created using RASA (open source machine learning framework).
        This AI-based bot uses previous chat logs as well as new inputs to learn.
        As the BOT answers all the commonly asked questions it ultimately decreases the response time,
        increases customer engagement and meets customer expectations.
        The chatbot can be trained on new data, and can be made to work on previously trained models as well.
    """,
    'author': 'Odoo Inc.',
    'website': 'https://www.odoo.com',
    'category': 'Website',
    'depends': ['website', 'mail', 'im_livechat'],
    'data': [
        'security/ir.model.access.csv',
        'views/chatbot_data_view.xml',
        'views/chatbot_load_view.xml',
        'views/chatbot_menus.xml',
        'views/chatbot_story_view.xml',
        'views/custom_intent_view.xml',
        'views/mail_message_view.xml',
        'views/res_config_settings_view.xml',
        'data/res_partner.xml',
        'data/im_livechat_channel_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'chatbot/static/**/*',
            'chatbot/static/src/js/odoo_bot.js',
            'im_livechat/static/src/legacy/public_livechat.js',
            'im_livechat/static/src/legacy/public_livechat.scss',
        ],
        'web.assets_frontend':[
            'chatbot/static/src/js/odoo_bot.js',
            'im_livechat/static/src/legacy/public_livechat.js',
            'im_livechat/static/src/legacy/public_livechat.scss',
        ],
        'website.assets_editor': [
            'chatbot/static/src/js/**/*',
        ],
    },
    'license': 'OPL-1',
}
