import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL для скрапінгу
url = "https://bank.gov.ua/ua/markets/exchangerate-chart?cn%5B%5D=AZN&startDate=04.03.2024&endDate=04.06.2024"

# Завантаження сторінки
response = requests.get(url)
html = response.content

# Парсинг HTML
soup = BeautifulSoup(html, 'html.parser')

# Знаходження таблиці
table = soup.find('table', {'class': 'table'})

# Збирання даних
data = []
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 0:
        date = columns[0].text.strip()
        rate = columns[1].text.strip()
        data.append([date, rate])

# Створення DataFrame
df = pd.DataFrame(data, columns=['date', 'rate'])

# Збереження даних у CSV файл
csv_filename = r'C:\Users\MegaNotik\Desktop\нівер\DataScraping\lab8\exchange_rates_AZN.csv'
df.to_csv(csv_filename, index=False)

csv_filename
