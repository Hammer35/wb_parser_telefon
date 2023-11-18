from requests import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class WBParser:
    def __init__(self):
        self.headers = {
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
        self.u_memmories = {
            "128": 12868,
            "256": 25425,
            "512": 117419,
            "1": 87749
        }
        self.u_collors = {
            "бежевый": 16119260,
            "белый": 16777215,
            "серый": 8421504,
            "синий": 255,
            "черный": 0,
            "голубой": 11393254,
            "желтый": 16776960,
            "фиолетовый": 15631086,
            "зеленый": 32768,
            "корраловый": '%D0%BA%D0%BE%D1%80%D0%B0%D0%BB%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9'

        }

    def main(self, base_url):
        count = 0
        s = Session()
        s.headers.update(self.headers)
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
            print('Цвет =>', data["data"]["products"][0]["colors"][0]["name"])
            print("Продавец =>", item['supplier'])
            print("Артикул =>", item['id'])
            # print("Фотографии =>", item['pics'])
            print("Цена до скидки =>", int(item['priceU'] / 100))
            print("Цена =>", int(item['salePriceU'] / 100))
            print("Скидка =>", item['sale'], "%")
            print("Отзывы =>", item['feedbacks'])
            print("Рейтинг =>", item['rating'])
            # print("Рейтинг отзывов =>", item['reviewRating'])
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

    def parse_search_list(self, search_list):
        for search in search_list:
            search_elements = search.split()
            model = ' '.join(search_elements[:-2])
            memory_ = search_elements[-2]
            color_ = search_elements[-1].strip()
            encoded_model = model.replace(' ', '%20')
            if color_ in self.u_collors:
                color_value = self.u_collors[color_]
            else:
                color_value = ''  # присваиваем пустую строку, если значение цвета не найдено
            if memory_ in self.u_memmories:
                memory_value = self.u_memmories[memory_]
            base_url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-445278&f4424={memory_value}&fcolor={color_value}&page=1&query={encoded_model}&resultset=catalog&sort=priceup&spp=25&suppressSpellcheck=false'
            print(base_url)
            self.main(base_url)

    def start(self):
        print('Введите искомое: ')
        search_list = []
        while True:
            search = input()
            if not search:
                break
            search_list.append(search.strip())
        self.parse_search_list(search_list)


parser = WBParser()
parser.start()

# https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-445278&f4424=12868&fcolor=32768&page=1&query=iphone%20xr%20128&resultset=catalog&sort=priceup&spp=25&suppressSpellcheck=false
# https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-445278&f4424=25425&fcolor=&page=1&query=iphone%20XR&resultset=catalog&sort=priceup&spp=25&suppressSpellcheck=false
