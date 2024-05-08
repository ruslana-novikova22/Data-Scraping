import csv
import scrapy
from mkr2.mkr2.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from mkr2.mkr2.items import Mkr2Item

class OLXSpider(scrapy.Spider):
    name = "olx"
    start_urls = ["https://www.olx.ua/uk/elektronika/prochaja-electronika/q-%D0%A1%D0%BC%D0%B0%D1%80%D1%82-%D0%B3%D0%BE%D0%B4%D0%B8%D0%BD%D0%BD%D0%B8%D0%BA%D0%B8-%D1%82%D0%B0-%D1%84%D1%96%D1%82%D0%BD%D0%B5%D1%81-%D0%B1%D1%80%D0%B0%D1%81%D0%BB%D0%B5%D1%82%D0%B8/?currency=UAH"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=expected_conditions.element_to_be_clickable(
                   (By.CSS_SELECTOR, '.css-1apmciz')
                ),
            )

    def parse(self, response):
        items = []
        listings = response.css('.css-1apmciz')

        for div in listings.css('div'):
            title = div.css('::attr(href)').get()
            price = div.css('p.span::text').get()
            location_date = div.css("p.span::text").get()

            yield Mkr2Item({
                'Назва оголошення': title,
                'Ціна': price,
                'Місце та дата': location_date,
            })

        self.write_to_csv(items)

    def write_to_csv(self, items):
        filename = 'olx_watches.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Назва оголошення', 'Ціна', 'Місце та дата'])
            writer.writeheader()
            for item in items:
                writer.writerow(item)
        self.log("Saved file %s" % filename)
