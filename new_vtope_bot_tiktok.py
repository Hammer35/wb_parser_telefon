from requests import Session
import json

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/zhenshchinam/odezhda/bluzki-i-rubashki',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-requested-with': 'XMLHttpRequest',
}


# category = input('Введите категорию: =>')
# article = input('Введите артикул: =>')


def main(base_url):
    count = 0
    s = Session()
    s.headers.update(headers)
    response = s.get(base_url)
    data = response.json()
    # print(data)
    print(data)
    for item in data['data']['products']:
        count += 1
        print('*' * 30)
        print("Порядковый №", count)
        print("Заголовок =>", item['name'])
        print("Бренд =>", item['brand'])
        print("Артикул =>", item['id'])
        print("Фотографии =>", item['pics'])
        print("Цена до скидки =>", item['priceU'] / 100)
        print("Цена =>", item['salePriceU'] / 100)
        print("Скидка =>", item['sale'], "%")
        print("Отзывы =>", item['feedbacks'])
        print("Рейтинг =>", item['rating'])
        print("Рейтинг отзывов =>", item['reviewRating'])
        try:
            print("Название акции =>", item['promoTextCat'])
        except:
            print('В акции не участвует')

base_url = 'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-455222&f4424=12868&fcolor=16119260&page=1&query=iphone%2012&resultset=catalog&sort=priceup&spp=25&suppressSpellcheck=false&uclusters=0'
main(base_url)


# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#
# ids_list = [
#     176754607,
#     180518469,
#     180518531,
#     178281171,
#     179567092,
#     183523312,
#     178297328,
#     185696853,
#     177819725,
#     183821736,
# ]
# driver = webdriver.Chrome()
# for i in ids_list:
#     driver.get(f"https://www.wildberries.ru/catalog/{i}/detail.aspx?targetUrl=SP")  # Замените URL на нужный
#     # time.sleep(3)
#     driver.implicitly_wait(10)
#     delivery_element = driver.find_elements(By.CLASS_NAME, "delivery__title")[0].text
#     print(delivery_element)