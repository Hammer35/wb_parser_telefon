from requests import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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


def main(base_url):
    count = 0
    s = Session()
    s.headers.update(headers)
    response = s.get(base_url)
    data = response.json()

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    for item in data['data']['products'][:15]:
        count += 1
        print('*' * 30)
        print("Порядковый №", count)
        # print("Заголовок =>", item['name'])
        print("Бренд =>", item['brand'])
        print("Продавец =>", item['supplier'])
        print("Артикул =>", item['id'])
        # print("Фотографии =>", item['pics'])
        print("Цена до скидки =>", int(item['priceU'] / 100))
        print("Цена =>", int(item['salePriceU'] / 100))
        print("Скидка =>", item['sale'], "%")
        print("Отзывы =>", item['feedbacks'])
        print("Рейтинг =>", item['rating'])
        # print("Рейтинг отзывов =>", item['reviewRating'])

        # # Преобразование текущей даты и времени
        # current_date = time.time()
        # time1 = item['time1']
        # time2 = item['time2']
        # dist = item['dist']
        # delivery_hours = ((time1 + time2) * 3600)
        # data_time = (current_date + delivery_hours + 28800)
        # print(int(data_time))

        try:
            print("Название акции =>", item['promoTextCat'])
        except KeyError:
            print('В акции не участвует')

        driver.get(f"https://www.wildberries.ru/catalog/{item['id']}/detail.aspx?targetUrl=SP")
        try:
            delivery_element = driver.find_elements(By.CLASS_NAME, "delivery__title")[0].text
            print("Дата доставки =>", delivery_element)
        except IndexError:
            print('Нет в наличии')

    driver.quit()


base_url = 'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-445278&f4424=12868&fcolor=0&page=1&query=iphone%2013%20pro%20max&resultset=catalog&sort=priceup&spp=25&suppressSpellcheck=false'
main(base_url)
