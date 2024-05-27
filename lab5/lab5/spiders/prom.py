from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Ініціалізую драйвер
driver = webdriver.Chrome()

url = 'https://prom.ua/ua/Dorozhnye-sumki-chemodany'
driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'JicYY')))

def extract_product_data(container):
    try:
        title_element = container.find_element(By.XPATH, './/span[@data-qaid="product_name"]')
        title = title_element.text
    except:
        title = 'N/A'
    try:
        price_element = container.find_element(By.XPATH, './/div[@data-qaid="product_price"]//span[@class="yzKb6"]')
        price = price_element.text
    except:
        price = 'N/A'
    try:
        store_element = container.find_element(By.XPATH, './/span[@data-qaid="company_name"]')
        store = store_element.text
    except:
        store = 'N/A'

    data = {
        'Title': title,
        'Price': price,
        'Store': store
    }
    return data

product_containers = driver.find_elements(By.CLASS_NAME, 'JicYY')
all_product_data = []
for container in product_containers:
    product_data = extract_product_data(container)
    all_product_data.append(product_data)

# Закриваю драйвер
driver.quit()

# Зберігаю дані у CSV файл, пропускаючи рядки з "N/A"
csv_file = 'product_offers.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Store'])
    writer.writeheader()
    for data_row in all_product_data:
        if all(value != 'N/A' for value in data_row.values()):
            writer.writerow(data_row)

print("Дані збережено у", csv_file)
