import telebot
from urllib.parse import quote
import requests
import threading

API_TOKEN = 'свой токен'
bot = telebot.TeleBot(API_TOKEN)

# Создаем блокировку
lock = threading.Lock()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Введите поисковый запрос: ")


@bot.message_handler(func=lambda message: True)
def search_product(message):
    query = message.text
    bot.reply_to(message, "Введите артикул товара:")
    bot.register_next_step_handler(message, process_articul, query)


def process_articul(message, query):
    articul = message.text
    encoded_query = quote(query, encoding='utf-8')
    num_page = 1
    found = False

    # Блокируем доступ к общим ресурсам
    with lock:
        while not found:
            url_search = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&query={encoded_query}&resultset=catalog&sort=popular&spp=28&suppressSpellcheck=false&page={num_page}'
            try:
                response = requests.get(url_search)
                data = response.json()
                product_ids = [product['id'] for product in data['data']['products']]
                if int(articul) in product_ids:
                    index = product_ids.index(int(articul))
                    page_number = num_page
                    position = index + 1
                    bot.reply_to(message,
                                 f"Артикул {articul} находится на {page_number} странице, на {position} месте.")
                    found = True
                else:
                    num_page += 1
                    bot.reply_to(message, f"Ищу на странице: {num_page}")
            except requests.exceptions.JSONDecodeError:
                bot.reply_to(message, "Весь сайт закончился, товар не найден. \nПопробуйте изменить поисковый запрос.")
                break


bot.polling()
