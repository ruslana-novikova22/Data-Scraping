from requests import get, post
from bs4 import BeautifulSoup

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

url = "https://hotline.ua/ua/fashion/naruchnye-chasy/"

response = get(url, headers=HEADERS)

if response.status_code == 200:
    html_content = response.text 
    soup = BeautifulSoup(html_content, 'html.parser')

    watches = soup.find_all(class_='list-item__info')
    items_data = []

    for watch in watches:
        watch_info = watch.find('div').text.strip()
        watch_link = watch.find('a')['href'] 

        watch_page = get(watch_link, headers=HEADERS)
        soup = BeautifulSoup(watch_page.content, 'html.parser')
        shop_list = soup.find(class_='list')
        
        shops_data = []
        if shop_list:
            for shop in shop_list.find_all('div'):
                shop_name = shop.find('div').text.strip()
                shop_link = shop.find('a')['href']
                shops_data.append({"Назва магазину": shop_name, "Посилання": shop_link})

        items_data.append({"Інформація про годинник": watch_info, "Посилання на годинник": watch_link, "Магазини": shops_data})

    server_url_shops = "https://mockend.com/Andrashko/scraping2023/Shops"
    response_shops = post(server_url_shops, json=items_data)
    print(f"Статус відповіді на сервері магазинів: {response_shops.status_code}")

    server_url_items = "https://mockend.com/Andrashko/scraping2023/Items"
    response_items = post(server_url_items, json=items_data)
    print(f"Статус відповіді на сервері годинників: {response_items.status_code}")

else:
    print(f"Помилка при отриманні відповіді: {response.status_code}")
