odoo.define('odoo_bot', function (require) {
    "use strict";
    var abstract_window_thread = require('im_livechat.legacy.mail.AbstractThreadWindow');
    var WebsiteLivechatMessage = require('im_livechat.legacy.im_livechat.model.WebsiteLivechatMessage');
    var im_livechat_button = require('im_livechat.legacy.im_livechat.im_livechat').LivechatButton;
    var WebsiteLivechat = require('im_livechat.legacy.im_livechat.model.WebsiteLivechat');
    var session = require('web.session');
    var rpc = require('web.rpc');
    var utils = require('web.utils');
    var url;
    var port_number;
    var req_url;
    var enableBot = true;
    var botID;
    var botToken;
    var isServerRunning;

    rpc.query({
        model: 'chatbot.load',
        method: 'getURL',
        args: [],
    }).then(function (result) {
        url = result;
    });
    rpc.query({
        model: 'chatbot.load',
        method: 'getPort',
        args: [],
    }).then(function (result) {
        port_number = result;
    });
    rpc.query({
        model: 'chatbot.load',
        method: 'getToken',
        args: [],
    }).then(function (result) {
        botToken = result;
    });
    rpc.query({
        model: 'chatbot.load',
        method: 'getBotID',
        args: [],
    }).then(function (result) {
        botID = result;
    });



    abstract_window_thread.include({
        _onKeydown: function (ev) {
            ev.stopPropagation();
            if (ev.which === 13) {
                var content = _.str.trim(this.$input.val());
                var messageData = {
                    content: content,
                    attachment_ids: [],
                    partner_ids: [],
                };
                this.$input.val('');
                if (content) {
                    this._postMessage(messageData);
                }
                if (content && enableBot) {
                    if (!url) {
                        url = 'localhost';
                    }
                    if (!port_number) {
                        port_number = 5005;

                    }
                    req_url = 'http://' + url + ':' + port_number;
                    fetch(`${req_url}/`, {
                            method: "GET"
                        })
                        .then(data => {
                            var message = {
                                "message": content,
                            }
                            fetch(`${req_url}/webhooks/rest/webhook?token=` + botToken, {
                                    method: "POST",
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'Accept': 'application/json'
                                    },
                                    body: JSON.stringify(message)
                                })
                                .then(data => {
                                    data.json()
                                        .then(res => {
                                            console.log(res)
                                            if (res.length == 0) {
                                                var messageData = {
                                                    content: 'Bot responseSorry I didn\'t get you',
                                                    attachment_ids: [],
                                                    partner_ids: [],
                                                };
                                                this._postMessage(messageData);

                                            } else {
                                                var messageData = {
                                                    content: "Bot response" + res[0].text,
                                                    attachment_ids: [],
                                                    partner_ids: [],
                                                };
                                                if (res[0].text == "Connecting you to our Customer Support Team!") {
                                                    enableBot = false;
                                                }
                                                this._postMessage(messageData);
                                            }
                                        })
                                })
                                .catch(err => {
                                    console.log(err)
                                });
                        })
                        .catch(err => {
                            var messageData = {
                                content: "Bot responseI am unable to assist you at this moment, Connecting you to an operator",
                                attachment_ids: [],
                                partner_ids: [],
                            };
                            this._postMessage(messageData);
                        })
                }
            }
        },
        _getHeaderRenderingOptions: function () {
            return {
                status: this.getThreadStatus(),
                thread: this.getThread(),
                title: 'Chat Window',
                unreadCounter: this.getUnreadCounter(),
                widget: this,
            };
        },
    });
    var v = 0
    const checker = async function () {
        let checkedID = await session.rpc(window.location.href + '/custombot/getBotID');
        v = checkedID
    }
    checker()
    WebsiteLivechatMessage.include({
        getAvatarSource: function () {
            var source = this._serverURL;
            if (this.hasAuthor()) {
                if (this.getAuthorID() == v) {
                    source += '/chatbot/static/description/icon.png'
                } else {
                    source += '/web/image/res.partner/' + this.getAuthorID() + '/avatar_128';
                }
                return source
            } else {
                source += '/mail/static/src/img/smiley/avatar.jpg';
                console.log(source)
                return source
            }
        }
    });
    WebsiteLivechat.include({
        _onTypingMessageAdded: function (message) {
            var operatorID = this.getOperatorPID()[0];
            if (message.hasAuthor() && message.getAuthorID() === operatorID) {
                this.unregisterTyping({
                    partnerID: operatorID
                });
            }
        }
    });
    im_livechat_button.include({
        _openChat: _.debounce(function () {
            if (this._openingChat) {
                return;
            }
            var self = this;
            var cookie = utils.get_cookie('im_livechat_session');
            var def;
            this._openingChat = true;
            clearTimeout(this._autoPopupTimeout);
            if (cookie) {
                def = Promise.resolve(JSON.parse(cookie));
            } else {
                this._messages = [];
                def = session.rpc('/im_livechat/get_session', {
                    channel_id: this.options.channel_id,
                    anonymous_name: this.options.default_username,
                    previous_operator_id: this._get_previous_operator_id(),
                }, {
                    shadow: true
                });
            }
            def.then(function (livechatData) {
                if (!livechatData || !livechatData.operator_pid) {
                    try {
                        self.displayNotification({
                            message: _t("No available collaborator, please try again later."),
                            sticky: true,
                        });
                    } catch (err) {
                        console.warn(_t("No available collaborator, please try again later."));
                    }
                } else {
                    livechatData.operator_pid[0] = botID;
                    self._livechat = new WebsiteLivechat({
                        parent: self,
                        data: livechatData
                    });
                    return self._openChatWindow().then(function () {
                        if (!self._history) {
                            self._sendWelcomeMessage();
                        }
                        self._renderMessages();
                        self.call('bus_service', 'addChannel', self._livechat.getUUID());
                        self.call('bus_service', 'startPolling');

                        utils.set_cookie('im_livechat_session', utils.unaccent(JSON.stringify(self._livechat.toData()), true), 60 * 60);
                        utils.set_cookie('im_livechat_auto_popup', JSON.stringify(false), 60 * 60);
                        if (livechatData.operator_pid[0]) {
                            var operatorPidId = livechatData.operator_pid[0];
                            var oneWeek = 7 * 24 * 60 * 60;
                            utils.set_cookie('im_livechat_previous_operator_pid', operatorPidId, oneWeek);
                        }
                    });
                }
            }).then(function () {
                self._openingChat = false;
            }).guardedCatch(function () {
                self._openingChat = false;
            });
        }, 200, true),
    });
});