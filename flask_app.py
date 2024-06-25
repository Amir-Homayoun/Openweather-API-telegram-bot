import os
import mtranslate

import token_telegram
import Openweather_apiPart
from ORL_for_sqlit_3 import ORL
import essential_dictionaries
my_data=ORL('Users_Info')
my_data.create_table('Users','chat_id name telegram_text telegram_json telegram_xml email_id email_text email_json email_xml language')

import sqlite3
con = sqlite3.connect('Users_Info.db')
cur = con.cursor()


from flask import Flask, request
import telepot
import urllib3


proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "Bot"
bot = telepot.Bot(token_telegram.my_token)
# user_name='your_username'
user_name='AmirHomayounsalehi87'
bot.setWebhook(f"https://{user_name}.pythonanywhere.com/{secret}", max_connections=1)

app = Flask(__name__)




flow_append=['weather-forecast']
flow_manager=['weather-forecast']

def flow_appender(key_word):
    flow_append.clear()
    flow_append.append(key_word)

def flow_manager_control(key_word,chat_id):
    bot.sendMessage(chat_id, key_word)
    flow_manager.clear()
    flow_manager.append(key_word)

all_chat_id=[]
def chat_id_finder():
    all_chat_id.clear()
    rec = my_data.select('Users', 'chat_id','yes')
    for i in rec:
        all_chat_id.append(i[0])


# # DB_File.create_table('Users', 'chat_id name telegram_text telegram_json telegram_xml email_id email_text email_json email_xml language')
# # DB_File.insert('information', f"{chat_id} {name[0]} ok ok ok not_given dw dw dw en")

def able_OR_disable(selected_setting,chat_id):
    def finding_respondes(position):
        main_text = essential_dictionaries.change_settings_responds
        for i in main_text.items():
            if selected_setting==i[0]:
                if position=='dw':
                    return i[1].split(',')[0]
                if position=='ok':
                    return i[1].split(',')[1]

    database = my_data.select('Users', f'chat_id {selected_setting}', 'yes')
    for i in database:
        if i[0] == str(chat_id):
            if i[1] == 'dw':
                my_data.update(selected_setting, 'ok', str(chat_id))
                main=finding_respondes('ok')
                return  main
            elif i[1] == 'ok':
                my_data.update(selected_setting, 'dw', str(chat_id))
                main = finding_respondes('dw')
                return main

def email_checker(chat_id):
    database = my_data.select('Users', f'chat_id email_id', 'yes')
    for i in database:
        if i[0]==str(chat_id):
            if i[1]=='not_given':
                return '⚠️Firstly you must enter your email by sending /Email-ID then you can able or disable the'
            else:
                    return i[1]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    def Languge_identifyier():
        users_info = my_data.select('Users', 'chat_id language', 'yes')
        for i in users_info:
            if str(chat_id) == str(i[0]):
                return str(i[1])

    def translator(key_word):
        return mtranslate.translate(key_word, Languge_identifyier(), 'auto')


    if content_type == 'text':
        # /start---------------------------------------------------
        if msg['text']=='/start':
            chat_id_finder()
            if str(chat_id) in all_chat_id:
                main = translator('Welcome again to my bot\nEnter name of any city or country!🌏🗺')
                bot.sendMessage(chat_id, main)
                flow_appender('weather-forecast')
            else:
                # my_data.create_table('Users', 'chat_id language')
                # my_data.insert('Users', f"{chat_id} en")
                main = translator('Welcome to my bot\nHere you get weather situation of any country or city🌎👍\nFor start please enter your name!😃')
                bot.sendMessage(chat_id, main)
                flow_appender('enter_name')
        elif msg['text']=='/back':
            flow_appender('weather-forecast')

        elif flow_manager[0]=='enter_name':
            checking_number_in_name = ''
            name = msg['text'].split(' ')
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if str(i) in name[0]:
                    bot.sendMessage(chat_id,f"How you have number ('{i}') in your name⚠️\nPlease enter your name again?")
                    checking_number_in_name += 'problem'

            if bool(checking_number_in_name) == False:
                my_data.insert('Users', f"{chat_id} {name[0]} ok ok ok not_given dw dw dw en")
                main=translator(f'Welcome to my bot {name[0].capitalize()}\nEnter name of any city or country!🌏🗺')
                bot.sendMessage(chat_id, main)
                flow_appender('weather-forecast')
        # /start---------------------------------------------------

        elif msg['text']=='/help':
            main = translator("It's very simple just enter name of any country or city😊")
            bot.sendMessage(chat_id, main)
            flow_appender('weather-forecast')






        elif msg['text'] == '/setting':
            def setting_finder(given_setting):
                # # DB_File.create_table('Users', 'chat_id name telegram_text telegram_json telegram_xml email_id email_text email_json email_xml language')
                # # DB_File.insert('information', f"{chat_id} {name[0]} ok ok ok not_given dw dw dw en")
                #
                database = my_data.select('Users', f'chat_id {given_setting}', 'yes')
                for i in database:
                    if i[0] == str(chat_id):
                        if given_setting == 'email_id':
                            if i[1] == 'not_given':
                                return """'You didn't enter your email!	❌ /Email-ID'"""
                            elif i[1] == 'given':
                                return i[1] + '📩 /Email-ID'
                        else:
                            if i[1] == 'dw':
                                return '❌'
                            elif i[1] == 'ok':
                                return '✅'
                            else:
                                return i[1]

            message= f"""
            🌏Here is your setting for my weather forcast 🌏!
📎Just by entering the blue words you can disable/able or change  settings📎

⚡Changing Language: /language 📚 {setting_finder('language')}

⚡Sending weather forcast data with Telegram !
Text: /TelegramText 📝 {setting_finder('telegram_text')}
Json file: /TelegramJson {setting_finder('telegram_json')}
Xml file: /TelegramXml {setting_finder('telegram_xml')}

⚡Sending weather forcast data with Email 📧 !
Your Email: {setting_finder('email_id')}

Text: /EmailText 📝 {setting_finder('email_text')}
Json file: /EmailJson {setting_finder('email_json')}
Xml file: /EmailXml {setting_finder('email_xml')}

Back:/back 🔙
            """
            main = translator(message)
            bot.sendMessage(chat_id, main)
            flow_appender('weather-forecast')

        # setting parts------------------------------------------------------------
        elif msg['text']=='/language':
            data=Languge_identifyier()
            if data=='en':
                my_data.update('language','fa',str(chat_id))
                main_message='🇮🇷حله الان تمام مسیج هارو به زبان فارسی می فرستم 🇮🇷'
                bot.sendMessage(chat_id, main_message)
            elif data == 'fa':
                my_data.update('language', 'en', str(chat_id))
                main_message = '🇺🇸🇬🇧Ok I right now will send all the texts in English🇺🇸🇬🇧'
                bot.sendMessage(chat_id, main_message)
            flow_appender('weather-forecast')

        elif msg['text']=='/TelegramText':
            get_data=able_OR_disable('telegram_text',str(chat_id))
            main=translator(get_data)
            bot.sendMessage(chat_id, main)
        elif msg['text']=='/TelegramJson':
            get_data = able_OR_disable('telegram_json', str(chat_id))
            main = translator(get_data)
            bot.sendMessage(chat_id, main)
        elif msg['text'] == '/TelegramXml':
            get_data = able_OR_disable('telegram_xml', str(chat_id))
            main = translator(get_data)
            bot.sendMessage(chat_id, main)

        # entering or changing email id-----------
        # elif msg['text']=='/Email-ID':
        #     email_situation=email_checker(str(chat_id))
        #     if '️Firstly' in email_situation:
        #         main = translator(f"Ok could you please enter your email-ID📧?")
        #         bot.sendMessage(chat_id, main)
        #     else:
        #         main = translator(f"""You had enter your email ("{email_situation}")\nPlease enter your new emai-ID📧?\nback=/back🔙""")
        #         bot.sendMessage(chat_id, main)
        #     flow_appender('entering_the_email')
        # elif flow_manager[0]=='entering_the_email':
        #     last_email=email_checker(str(chat_id))
        #     text=msg['text']
        #     if '@' not in text or '.com' not in text:
        #         main = translator(f"You must enter your email-id completely📧!\n❗'Don't forget '@'❗")
        #         bot.sendMessage(chat_id, main)
        #     elif last_email==text:
        #         main = translator(f"❗This email-id is your last email-id that you entered❗\nback=/back🔙")
        #         bot.sendMessage(chat_id, main)
        #     # else:













        elif msg['text'][0] == '/':
            main = translator(f'⚠️Unknown command⚠️\n please try again!')
            bot.sendMessage(chat_id, main)

        elif flow_manager[0]=='weather-forecast':
            def send_or_not(selected_setting):
                database = my_data.select('Users', f'chat_id {selected_setting}', 'yes')
                for i in database:
                    if i[0]==str(chat_id):
                        if i[1]=='dw':
                            return 'no'
                        elif i[1]=='ok':
                            return 'ok'

            database = my_data.select('Users', f'chat_id name', 'yes')
            for i in database:
                if i[0]==str(chat_id):
                    name=i[1]

            output_openweather_api = Openweather_apiPart.telegram_weather_sender(msg['text'],name)
            weather_message =[]
            if type(output_openweather_api)==list:
                append_message=[]
                append_message.append(translator(output_openweather_api[0]))
                append_message.append(output_openweather_api[1])
                append_message.append(translator(output_openweather_api[2]))
                weather_message.append(''.join(append_message))
            else:
                main=send_or_not('telegram_text')
                if main=='no':
                    weather_message.append('dont send')
                else:
                    weather_message.append(output_openweather_api)
            if weather_message[0]!='dont send':
                main_message=translator(weather_message[0])
                bot.sendMessage(chat_id, main_message)

            main_json = send_or_not('telegram_json')
            if main_json == 'ok':
                bot.sendDocument(chat_id, open(''.join(Openweather_apiPart.main_file_name_json), 'rb'))

            main_xml = send_or_not('telegram_xml')
            if main_xml == 'ok':
                print(main_xml,'in to ife')
                bot.sendDocument(chat_id, open(''.join(Openweather_apiPart.main_file_name_xml), 'rb'))


            try:
                os.remove(''.join(Openweather_apiPart.main_file_name_xml))
                os.remove(''.join(Openweather_apiPart.main_file_name_json))
            except FileNotFoundError:
                None

    else:
        main=translator(f'⚠️Please just send me text not {content_type} and else!⚠️')
        bot.sendMessage(chat_id, main)
        flow_appender('weather-forecast')


    flow_manager_control(flow_append[0],str(chat_id))
@app.route(f'/{secret}', methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        handle(update['message'])
    return "OK"






