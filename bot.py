import os
import telebot
import google_search_py
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot('5113553593:AAFIBZ30ZAqQRfyfTP26uvHnhVZBVEXdzog')


@bot.message_handler(commands='start')
def start(message):
    bot.send_message(message.chat.id, "Напишите название песни или строчки из нее.")


def parse(url):
    api = requests.get(url)
    api_content = api.text
    soup = BeautifulSoup(api_content, 'html.parser')
    text = soup.find_all(class_='b-podbor__text')
    f = open("file.txt", "w")
    for i in range(len(text)):
        f.write(text[i].get_text() + "\n")
    f.close()


@bot.message_handler(content_types='text')
def listener(message):
    try:
        text = message.text
        chat_id = message.chat.id
        search = google_search_py.search(text + " amdm.ru")
        needed_url = search['url']
        parse(needed_url)
        f = open("file.txt")
        read = f.read()
        if len(read) > 4095:
            for x in range(0, len(read), 4095):
                bot.reply_to(message, text=read[x:x + 4095])
        else:
            bot.reply_to(message, text=read)
        f.close()
        os.remove("file.txt")
    except Exception as e:
        bot.send_message(chat_id, "По Вашему запросу ничего не найдено. Попробуйте добавить фамилию автора")
        print(e)


bot.infinity_polling()