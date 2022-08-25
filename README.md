# Topics

## 1. Introduction / Background
We have developed a customizable chatbot which can be used anywhere and can address literally any type of question it is trained for.
With this chatbot, you have the power to create new data, new stories for the bot to learn from and rules to enhance bot performance.
An operator can interfere wherever required, making the bot conversations safe and controllable.
The main purpose behind developing the customizable chatbot is to speed up the customer response time and improve the customer experience.
Along with that, we added modifications and customizations for the chatbot, making it completely flexible for any use case.
We have made use of an open source machine learning framework called RASA, to develop the chatbot. In order to customize the chatbot data,
we are reading from and writing to .yml files using python.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/1.openModule.gif)
## 2. Technologies
- Python - Built custom module to enable customization of the chatbot and allow users to configure the chatbot
- JavaScript - Used to integrate the chatbot with the already existing Website and Discuss module
- SQL - Created new tables and queried the existing ones in order to fetch important data
- Machine Learning
- Natural Language Processing
## 3. Chatbot and Different Chatbot dev options
For developing the chatbot we explored different options like creating a machine learning model using Neural Networks,
a Natural language processing model using NLTK, creating a bot using existing machine learning libraries like chatterbot. 
We explored other options which employed creating the chatbot using Bot development frameworks. Creating a natural language processing
model from scratch demanded a huge amount of training data and the model may take hours to train.
Moreover, not every client can have a huge amounts of data to make sure of a heavily trained model.
Thus, we felt that creating a model from scratch was not the best option.
Dialogflow doesn’t allow any customizations on its code but you can only customize in fulfilments.
On the other hand, Rasa, an open source chatbot framework, gives complete freedom to configure NLU, Core, Integration, Deployment, etc.
## 4. RASA and Why RASA?
After analyzing, we realized that RASA offers the most suitable, easy-to-understand and customize conversational AI. The chatbot that we have,
understands user intents (input), generates required outputs (responses), and learns from a bunch of intent-response pairs (stories).
We can also define a Rule for the bot to adhere to. Besides the current implementation, RASA provides a bunch of other APIs which can help us scale the bot if required.
Therefore, we have used the RASA framework for our chatbot development.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/15.RasaServer.gif)
## 5. Features
### a. Deliverables
| Objectives|Description|Status|
|------|------|------|
|Use previous chat logs to learn|Provides accessibility to the session history included in the live chat application and allows the bot to train on that data|:heavy_check_mark:|
|Allow the manager to check responses|The chatbot conversation are visible to the operators in Discuss application and hence they can keep a check on how the bot is performing|:heavy_check_mark:|
|Allow humans to jump in and replace the bot as needed|The chatbot allows a human representative / operator to interfere and jump in the conversation wherever required. The bot will bring in the operator on customer request as well|:heavy_check_mark:|
### b. Custom Module
- Load New Data: The chatbot learns from the data that it is provided. Our module allows the user to create new data values and load them to the chatbot's training files.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/2.CreateIntent.gif)
- Load Data from previous logs: In addition to creating new data, the chatbot can also be loaded with the data from session histories.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/4.PreviousSession.gif)
- Create Custom stories: Stories help the chatbot understand the flow of the conversation and help the bot predict the next response. We can create customized stories
and give a direction to the conversation.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/6.Story.gif)
- Train Chatbot Models: Once we have loaded data into the chatbot, we can train the chatbot on the loaded data. Here, we make an API call to the /model/train and the
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/9.TrainBot.gif)
trained model is saved in the /models folder in the RASA directory.
- Switch between trained models: If we have multiple models trained and we need to use a previously trained model or if we need to switch back to the latest model,
we can simply click on the model name and load it.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/10.switchModel.gif)
- Configure chatbot setup: The user can host the chatbot wherever required and for that purpose, we have created a configuration where the user can give information
about the server URL, port and the RASA directory.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/11.Config.gif)
### c. Chat Window
- Chatbot Support: The chatbot will welcome any customer who is in need of support or assistance and try to resolve their issue.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/13.connectOperator.gif)
- Can call for an Operator: The customer can call for a live operator at any point during the conversation with the chatbot.
- Operator Can Jump In: An operator can jump in at any moment and continue the chat from there.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/14.OperatorConnected.gif)
## 7. Integration
For integrating our chatbot with Odoo, we have created a new module in Odoo and inherited the existing Livechat module. We made necessary changes to the Python,
Javascript and XML files while working on this project. We have used the HTTP API to interact with a running Rasa Open Source server.
With the API, we can train models, send messages, run tests, and more.
## 8. Performance
The bot gives an appropriate response to the user query. Thus, the bot is capable of resolving most of the queries which are asked by the user. The bot also redirects to a customer support team member if the user asks for it. In this way, it is ensured that all the customer queries are answered in a minimal amount of time and the user experience is greatly enhanced.
![](https://github.com/mihir254/Odoo-Custom-Chatbot/blob/main/assets/12.Chat.gif)
## 9. Conclusion
The chatbot is perfectly capable of providing support to the users/customers. We can scale the chatbot to answer queries in any domain.
This gives clients full power over what the chatbot is capable of achieving. The bot also allows an operator to jump in whenever the user/customer asks for it
or if the operator feels the need for it. This makes sure that every conversation can be monitored if necessary. With the help of a chatbot, we can make sure that
customer support teams / other related teams are concentrating on resolving the more important problems while the chatbot is breaking down the problem for them.
Also, not all complaints/requests are required to have human intervention, some can have pre-existing answers or can be answered using some easy data fetching 
from the database. With the help of this chatbot, we can make sure that such problems are solved on the fly and the users are getting answered quicker than before.
## 10. Future Scope
This chatbot is a conversational artificial intelligence. It is capable of capturing user responses and assigning values to those
responses. For example, if the bot prompts you to type your name, it can capture and remember your name throughout. This property of our chabtot can be used
to address many problems such as ticket generation. In Odoo's Helpdesk module, we can generate a ticket by taking user information such as name, email,
phone number, subject of ticket, tags, etc. Also, because the bot is completely customizable, it has applications beyond customer support. It can be used at
any such place where the client needs to interact and needs to replace a human. The bot can be trained to respond like a human representative in such cases.

