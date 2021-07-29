# -*- coding: utf-8 -*-
__author__ = "SirHades696"
__email__ = "djnonasrm@gmail.com"

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove
import telegram
import logging
import os
import sys
#for web scrapping
from web_scraping.search import search_packages
#Languages
import lang.data_spa as data_spa
import lang.data_en as data_en
#Emojis
import lang.emojis as emojis
# Translate from googletrans
from googletrans import Translator
#Url shorter 
import pyshorteners

class bot_telegram:
    
    def __init__(self):
        #States for Bot
        self._state_one, self._state_two, self._state_three, self._state_four = range(4)
        self._TOKEN = os.getenv('TOKEN')
        self._mod = os.getenv("MODE")
        self._emojis = emojis.emojis
        self._start_logger()
        self._start_bot()
    
    def _start_logger(self):
        """
        Set logger
        """
        #Logging, display the process in console
        logging.basicConfig(
            level=logging.INFO, 
            format="%(asctime)s | %(message)s")
        self.logger = logging.getLogger()

    def _name_welcome(self,update, context): 
        """
        Get user data

        Returns:
            [string]: username
        """
        username = update.effective_user['username']
        user_id = update.effective_user['id'] 
        f_name = update.effective_user['first_name'] 
        l_name = update.effective_user['last_name']
        # print in console
        self.logger.info(f"El usuario {username}/{user_id}, ha inicializado el bot con un lenguaje...")
        
        if username != None and f_name != None and l_name != None:
            full_name = f_name + " " + l_name
            cadena = full_name + "/" + username
        elif username != None and f_name != None:
            cadena = f_name + "/" + username
        elif username == None and  f_name != None:
            cadena = f_name
                
        return cadena
                    
    def _welcome(self,user):
        """
        Returns:
            [string]: Welcome message
        """
        cadena = (
            f"<b>{self.lang['welcome'][0]} {self._emojis['smile']} {self._emojis['smile2']}"
            f"\n\n{self.lang['welcome'][1]}"
            f"\n\n<i>{self._emojis['fire']}{user}</i>{self._emojis['hand']}"
            f"\n\n{self.lang['welcome'][2]} {self._emojis['robot']} {self._emojis['robot2']}"
            f"\n\n{self.lang['welcome'][3]}"
            f"\n{self.lang['welcome'][4]}"
            f"\n{self.lang['welcome'][5]} {self._emojis['paper']}"
            f"\n\n<i>{self._emojis['check']} {self.lang['welcome'][6]}"
            f"\n{self._emojis['check']} {self.lang['welcome'][7]}"
            f"\n{self._emojis['check']} {self.lang['welcome'][8]}"
            f"\n{self._emojis['check']} {self.lang['welcome'][9]}"
            f"\n{self._emojis['check']} {self.lang['welcome'][10]}</i></b>")
        
        return cadena
        
    def _search_message(self,update, context):
        """
        send message requesting the package 
        
        Returns:
            [int]: return state two
        """
        username = update.effective_user['username']
        user_id = update.effective_user['id'] 
        self.logger.info(f"El usuario {username}/{user_id}, ha creado una solicitud de búsqueda...")
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None) 
        cadena = f"<b>{self.lang['search_package']}</b>{self._emojis['magnifying_glass']}{self._emojis['magnifying_glass']}"
        context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=cadena)
        
        return self._state_two
    
    def _search_results(self,update, context):
        """Display results for the first page of pypi
        
        Returns:
            [int]: Return state three 
        """
        username = update.effective_user['username']
        user_id = update.effective_user['id']
         
        self.package_raw = update.message.text
        pck = self.package_raw.replace("\n", " ")
        self.package = pck if not ' ' in pck else pck.replace(' ', '+')
        self.logger.info(f"El usuario {username}/{user_id}, ha introducido una búsqueda...")
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None) 
        cadena = f"<b>{self.lang['searching_package']}\n<i><u>{self.package_raw}</u></i></b> {self._emojis['monocle']} {self._emojis['magnifying_glass']}"
        context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=cadena)
        #start o restart in 1 
        page = 0
        self.page = page + 1
        #Web scrapping
        search = search_packages(self.package, page=self.page)
        values = search.get_values()
        
        #set api for translate
        translator = Translator()   
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None) 
        self.logger.info(f"El usuario {username}/{user_id}, esta recibiendo los resultados de la búsqueda...")
    
        tam = len(values)
        for i, result in enumerate(values):
            try:
                values[result]['Project_name']
                if i == 0:
                    cadena2 = (f"<b>{self._emojis['magnifying_glass']}{self._emojis['smile']}{self.lang['results'][0]}"
                               f"\n{self.lang['results'][1]}{self.page} {self._emojis['paper']}</b>")
                               
                    context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=cadena2) 
                
                # Translate for spanish 
                if self.lang_var == "SPA":
                    summary = translator.translate(str(values[result]['Summary']), dest='es').text
                    
                    if "Author" in values[result]['Author']:
                        author = translator.translate(values[result]['Author'], dest='es').text
                    else:
                        author = values[result]['Author']
                        
                    if "No Python" in values[result]['Requires']:
                        requires = translator.translate(values[result]['Requires'], dest='es').text
                    else:
                        requires = values[result]['Requires']
                    
                    if "No official" in values[result]['Homepage']:
                        homepage = translator.translate(values[result]['Homepage'], dest='es').text
                    else:
                        homepage = values[result]['Homepage']
                        
                else: 
                    summary = values[result]['Summary']
                    homepage = values[result]['Homepage']
                    requires = values[result]['Requires']
                    author = values[result]['Author']
                    
                txt = ( f"<b>{self.lang['data_package']['results']} {str(i+1)}</b> {self._emojis['index']}"
                        f"\n<b>{self.lang['data_package']['page']}<u><i>{self.page}</i></u></b>"
                        f"\n<b>{self.lang['data_package']['package']}</b> <i><u>{values[result]['Project_name']}</u></i>"
                        f"\n<b>{self.lang['data_package']['version']}</b><i>{values[result]['Version']}</i>"
                        f"\n<b>{self.lang['data_package']['released']}</b><i>{values[result]['Released']}</i>"
                        f"\n<b>{self.lang['data_package']['summary']}</b><i>{summary}</i>"
                        f"\n<b>{self.lang['data_package']['pypi_link']}</b><i>{values[result]['PyPi_link']}</i>"
                        f"\n<b>{self.lang['data_package']['author']}</b><i>{author}</i>"
                        f"\n<b>{self.lang['data_package']['requires']}</b><i>{requires}</i>"
                        f"\n<b>{self.lang['data_package']['pip']}</b><i><u>{values[result]['PIP']}</u></i>"
                        f"\n<b>{self.lang['data_package']['homepage']}</b><i>{homepage}</i>")
                #Typing 
                update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)       
                context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=txt)
                #last value 
                if i+1 == tam:
                    #Typing 
                    update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
                    cadena4 = f"<b>{self._emojis['smile2']}{self._emojis['smile']}{self.lang['with_last_package']}{self._emojis['hand']}{self._emojis['hand']}</b>"
                    context.bot.sendMessage(chat_id=user_id, 
                                            parse_mode="HTML", 
                                            text=cadena4, 
                                            reply_markup=self._btns_second_menu())
            except KeyError:
                #Typing 
                update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
                cadena3 = f"<b>{self._emojis['sad']}{self.lang['unkown_package']}\n{self._emojis['cross_mark']} <i><u>{self.package}</u></i> {self._emojis['cross_mark']}</b>"
                context.bot.sendMessage(chat_id=user_id, 
                                        parse_mode="HTML", 
                                        text=cadena3,
                                        reply_markup=self._btns_main_menu())
                
                self.logger.info(f"El usuario {username}/{user_id}, no recibio resultados, el package no fue encontrado...")
                
        self.logger.info(f"El usuario {username}/{user_id}, ha recibido los resultados de la búsqueda...")
        
        return self._state_three

    def _search_more_results(self, update, context):
        """Display more results for the search

        Returns:
            [int]: Return state three
        """
        #Auto incremental for more results 
        self.page = self.page + 1

        username = update.effective_user['username']
        user_id = update.effective_user['id']
        
        self.logger.info(f"El usuario {username}/{user_id}, ha solicitado más resultados...")
        
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)  
        text_more = f"<b>{self._emojis['magnifying_glass']}{self.lang['more_results']}<i><u>{self.page}</u></i>{self._emojis['paper']}</b>"     
        context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=text_more) 
        
        #Web scrapping
        search = search_packages(self.package, page=self.page)
        values = search.get_values()
        
        #set api for translate
        translator = Translator()   
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None) 
        self.logger.info(f"El usuario {username}/{user_id}, esta recibiendo los nuevos resultados de la búsqueda...")
    
        tam = len(values)
        for i, result in enumerate(values):
            if i == 0:
                cadena2 = (f"<b>{self._emojis['magnifying_glass']}{self._emojis['smile']}{self.lang['results'][0]}"
                            f"\n{self.lang['results'][1]}{self.page} {self._emojis['paper']}</b>")
                            
                context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=cadena2) 
            # Translate for spanish 
            if self.lang_var == "SPA":
                summary = translator.translate(str(values[result]['Summary']), dest='es').text
                
                if "Author" in values[result]['Author']:
                    author = translator.translate(values[result]['Author'], dest='es').text
                else:
                    author = values[result]['Author']
                    
                if "No Python" in values[result]['Requires']:
                    requires = translator.translate(values[result]['Requires'], dest='es').text
                else:
                    requires = values[result]['Requires']
                
                if "No official" in values[result]['Homepage']:
                    homepage = translator.translate(values[result]['Homepage'], dest='es').text
                else:
                    homepage = values[result]['Homepage']
                    
                if "No PIP" in values[result]['PIP']:
                    pip = translator.translate(values[result]['PIP'], dest='es').text
                else:
                    pip = values[result]['PIP']
                    
            else: 
                summary = values[result]['Summary']
                homepage = values[result]['Homepage']
                requires = values[result]['Requires']
                author = values[result]['Author']
                pip = values[result]['PIP']
                
            txt = (
                    f"<b>{self.lang['data_package']['results']} {str(i+1)}</b> {self._emojis['index']}"
                    f"\n<b>{self.lang['data_package']['page']}<u><i>{self.page}</i></u></b>"
                    f"\n<b>{self.lang['data_package']['package']}</b> <i><u>{values[result]['Project_name']}</u></i>"
                    f"\n<b>{self.lang['data_package']['version']}</b><i>{values[result]['Version']}</i>"
                    f"\n<b>{self.lang['data_package']['released']}</b><i>{values[result]['Released']}</i>"
                    f"\n<b>{self.lang['data_package']['summary']}</b><i>{summary}</i>"
                    f"\n<b>{self.lang['data_package']['pypi_link']}</b><i>{values[result]['PyPi_link']}</i>"
                    f"\n<b>{self.lang['data_package']['author']}</b><i>{author}</i>"
                    f"\n<b>{self.lang['data_package']['requires']}</b><i>{requires}</i>"
                    f"\n<b>{self.lang['data_package']['pip']}</b><i><u>{pip}</u></i>"
                    f"\n<b>{self.lang['data_package']['homepage']}</b><i>{homepage}</i>")
            #Typing 
            update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)       
            context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=txt)
            #last value 
            if i+1 == tam:
                #Typing 
                update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
                cadena4 = f"<b>{self._emojis['smile2']}{self._emojis['smile']}{self.lang['with_last_package']}{self._emojis['hand']}{self._emojis['hand']}</b>"
                context.bot.sendMessage(chat_id=user_id, 
                                        parse_mode="HTML", 
                                        text=cadena4, 
                                        reply_markup=self._btns_second_menu())
       
        self.logger.info(f"El usuario {username}/{user_id}, ha recibido los resultados de la búsqueda...")
        
        return self._state_three
    
    def _about_message(self, update, context):
        """Display about message 
        Returns:
            [int]: return state one
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        s = pyshorteners.Shortener()
        short = s.chilpit.short(self.lang['about'][5])
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None) 
        txt = ( f"<b>{self.lang['about'][0]} {self._emojis['smile']}{self._emojis['smile2']}"
                f"\n{self.lang['about'][1]}{self._emojis['hand']}"
                f"\n{self.lang['about'][2]} {self._emojis['paper']}"
                f"\n{self._emojis['trex']} <i><u>{self.lang['about'][3]}</u></i> {self._emojis['alien']}"
                f"\n\n{self._emojis['smile']}{self.lang['about'][4]}{short}</b>")
        
        context.bot.sendMessage(
                                chat_id=user_id,
                                text=txt,
                                reply_markup=self._btns_main_menu(), 
                                parse_mode="HTML")
        self.logger.info(f"El usuario {username}/{user_id}, ha seleccionado about...")
        
        return self._state_one
    
    def _set_lang(self, lang):
        """Set lang for all UI of Telegram
        Args:
            lang ([String]): SPA = Spanish, EN = English

        Returns:
            [lang]: Dict with translates
        """
        #get lang and set all bot 
        if lang == 'SPA':
            lang = data_spa.data
        elif lang == 'EN':
            lang = data_en.data
        return lang
    
    def _btns_second_menu(self):
        """display second Menu when has state three for bot

        Returns:
            [ReplyKeyboardMarkup]: Three buttons, More results, new search and lang
        """
        if self.lang['btns']['btn_lang'] == 'Spanish':
            txt = f"{self.lang['btns']['btn_lang_txt']}: {self._emojis['mexa']}"
        elif self.lang['btns']['btn_lang'] == 'English':
            txt = f"{self.lang['btns']['btn_lang_txt']}: {self._emojis['usa']}"
            
        reply_keyboard = [[f"{self.lang['btns']['btn_more_results']}{self._emojis['plus']}", 
                           f"{self.lang['btns']['btn_new_search']}{self._emojis['new']}"],
                          [f"{self.lang['help']['btn_help']}{self._emojis['help']}",
                           f"{self.lang['stop']['btn_stop']}{self._emojis['stop']}"],
                          [f"{txt}"]
                          ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        return markup  
    
    def _btns_main_menu(self):
        """display Main Menu when has state one for bot

        Returns:
            [ReplyKeyboardMarkup]: Three buttons, Search, About, LANG 
        """
        if self.lang['btns']['btn_lang'] == 'Spanish':
            txt = f"{self.lang['btns']['btn_lang_txt']}: {self._emojis['mexa']}"
        elif self.lang['btns']['btn_lang'] == 'English':
            txt = f"{self.lang['btns']['btn_lang_txt']}: {self._emojis['usa']}"
            
        reply_keyboard = [
            [f"{self._emojis['monocle']}{self.lang['btns']['btn_search']}{self._emojis['magnifying_glass']}", 
            f"{self._emojis['alien']}{self.lang['btns']['btn_about']}{self._emojis['robot']}"],
            [f"{self.lang['help']['btn_help']}{self._emojis['help']}",
              f"{self.lang['stop']['btn_stop']}{self._emojis['stop']}"],
            [f"{txt}"]]
        
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        return markup     
    
    def _btns_lang_menu(self):
        """display first Menu when starting the bot 

        Returns:
            [ReplyKeyboardMarkup]: Two buttons, spanish and english
        """
        reply_keyboard = [[f'Spanish{self._emojis["mexa"]}', 
                           f'English{self._emojis["usa"]}']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        return markup   
    
    def _start_message_lang(self, update, context):
        """Set lang and display the message with the selected lang 
        Other option: Restart bot with other lang [spanish/english]
        Returns:
            [int]: Return state one
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        text = update.message.text
        #Checking words in text from user 
        if "Spanish" in text or "Change" in text:
            self.lang_var = "SPA"
        elif "English" in text or "Cambiar" in text:
            self.lang_var = "EN"
        #set lang
        self.lang = self._set_lang(self.lang_var)
        user = self._name_welcome(update,context)
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None) 
        context.bot.sendMessage(chat_id=user_id,
                            text = self._welcome(user),
                            reply_markup = self._btns_main_menu(), 
                            parse_mode="HTML")
        self.logger.info(f"El usuario {username}/{user_id}, selecciono un idioma...") 
        
        return self._state_one
                
    def _start_select_lang(self, update,context):
        """
        Send sticker and display the first buttons Spanish and English
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self._emojis['bot'],
                                reply_markup=self._btns_lang_menu())
        
        self.logger.info(f"El usuario {username}/{user_id}, va a seleccionar un lang...")
        
        return self._state_one
    
    def _stop_message(self, update, context):
        """Confirm end bot and send cuestion with sticker
        
        Returns:
            [int]: return state four
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        self.logger.info(f"El usuario {username}/{user_id}, confirmará si termina el bot...")
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
        
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self._emojis['finish_him'])
        
        reply_keyboard = [[f"{self.lang['btns']['btn_yes']}{self._emojis['sad']}", 
                           f"{self.lang['btns']['btn_no']}{self._emojis['smile']}"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        
        context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", 
                                text=f"<b>{self.lang['stop']['stop_txt']}{self._emojis['thinking']}</b>",
                                reply_markup=markup)
        return self._state_four
    
    def _stop(self, update, context):
        """End the bot with select choice "YES" and send sticker

        Returns:
            [Object]: End bot
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
        
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self._emojis['stop_yes'],
                                reply_markup=ReplyKeyboardRemove())
        self.logger.info(f"El usuario {username}/{user_id}, ha terminado el bot ...")
        
        return ConversationHandler.END
             
    def _stop_no_message(self, update, context):
        """If the user select the choice "NO" send this message

        Returns:
            [int]: Return the state one of the bot 
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
        
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self._emojis['stop_no'],
                                reply_markup=self._btns_main_menu())
        self.logger.info(f"El usuario {username}/{user_id},no termino  el bot...")
        
        return self._state_one
   
    def _help_message(self, update, context):
        """
        Send help message for the user
        Returns:
            [int]: Return the state one of the bot 
        """
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        
        txt = (f"<b>{self.lang['help']['help_txt'][0]}{self._emojis['smile']}{self._emojis['smile2']}"
               f"\n\n{self.lang['help']['help_txt'][1]}{self._emojis['index']}"
               f"\n\n{self.lang['help']['help_txt'][2]}{self._emojis['paper']}</b>")
        #Typing 
        update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
        
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self._emojis['help_s'])
        
        context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", 
                                text=txt,
                                reply_markup=self._btns_main_menu())
        
        self.logger.info(f"El usuario {username}/{user_id}, solicito ayuda...")
        return self._state_one
    
    def _start_bot(self):
        """
        Start telegram bot
        Start updater, dispatcher and handlers
        """
        #get data bot  
        bot_pypi = telegram.Bot(token = self._TOKEN)
        #link between updater and bot 
        updater = Updater(bot_pypi.token, use_context=True)
        # dispatcher 
        dp = updater.dispatcher
        #Conversition handler and states
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self._start_select_lang)],
            states = {
                self._state_one : 
                    [
                        MessageHandler(
                        Filters.regex(f'^(Spanish{self._emojis["mexa"]}|English{self._emojis["usa"]})$'),
                        self._start_message_lang),
                        
                        MessageHandler(
                        Filters.regex(f'^({self._emojis["alien"]}About...{self._emojis["robot"]}|{self._emojis["alien"]}Acerca de...{self._emojis["robot"]})$'), 
                            self._about_message),
                        
                        MessageHandler(
                        Filters.regex(f"^(Change Lang and Restart: {self._emojis['mexa']}|Cambiar Idioma y Reiniciar: {self._emojis['usa']})$"),
                        self._start_message_lang),
                        
                        MessageHandler(
                        Filters.regex(f"^({self._emojis['monocle']}Buscar Package{self._emojis['magnifying_glass']}|{self._emojis['monocle']}Search Package{self._emojis['magnifying_glass']})$"),
                        self._search_message),
                        
                        MessageHandler(
                        Filters.regex(f"^(Detener Bot{self._emojis['stop']}|Stop Bot{self._emojis['stop']})$"),
                        self._stop_message
                        ),
                        
                        MessageHandler(
                        Filters.regex(f"^(Ayuda{self._emojis['help']}|Help{self._emojis['help']})$"),
                        self._help_message
                        )
                        
                     ],
                    
                self._state_two: 
                    [
                        MessageHandler(Filters.text, self._search_results)
                    ],
                
                self._state_three: 
                    [
                        MessageHandler(
                        Filters.regex(f"^(Más Resultados{self._emojis['plus']}|More Results{self._emojis['plus']})$"), 
                        self._search_more_results),
                        
                        MessageHandler(
                        Filters.regex(f"^(Nueva Búsqueda{self._emojis['new']}|New Search{self._emojis['new']})$"),
                        self._search_message),
                        
                        MessageHandler(
                        Filters.regex(f"^(Change Lang and Restart: {self._emojis['mexa']}|Cambiar Idioma y Reiniciar: {self._emojis['usa']})$"),
                        self._start_message_lang),
                        
                        MessageHandler(
                        Filters.regex(f"^(Detener Bot{self._emojis['stop']}|Stop Bot{self._emojis['stop']})$"),
                        self._stop_message
                        ),
                        
                        MessageHandler(
                        Filters.regex(f"^(Ayuda{self._emojis['help']}|Help{self._emojis['help']})$"),
                        self._help_message
                        )
                    ],
                    
                self._state_four : 
                    [
                        MessageHandler(
                        Filters.regex(f"^(Si{self._emojis['sad']}|Yes{self._emojis['sad']})$"),
                        self._stop
                        ),
                        
                        MessageHandler(
                        Filters.regex(f"^(No{self._emojis['smile']})$"),
                        self._stop_no_message
                        ),
                    ]
                
                    },
            fallbacks = [CommandHandler("start", self._start_select_lang)]
        )
        #Switch events 
        dp.add_handler(conv_handler)
        #start mode
        if self._mod == "dev":
            #get request from telegram 
            updater.start_polling()
            print("::::::::::::::::::::::::::::::::::::Starting BOT::::::::::::::::::::::::::::::::::::::")
            #close with CTRL + C
            updater.idle()
            
        elif self._mod == "prod": 
            _HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
            PORT = int(os.environ.get('PORT', '8443'))
            
            updater.start_webhook(
                listen="0.0.0.0",
                port = PORT, 
                url_path = self._TOKEN,
                webhook_url=f"https://{_HEROKU_APP_NAME}.herokuapp.com/{self._TOKEN}"
            )
            print("::::::::::::::::::::::::::::::::::::Starting BOT::::::::::::::::::::::::::::::::::::::")
            updater.idle()
        else:
            self.logger.info("No se especificó ningún modo de trabajo")
            sys.exit()

if __name__ == "__main__":
    """
        Start the bot just by typing  > python bot_telegram.py
    """
    bot_telegram()      
