# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import re

class DataCleaningPipeline:
    def process_item(self, item, spider):
        # Очистка даних від зайвих пробілів та символів переносу рядка
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip()
            elif isinstance(value, list):
                item[key] = [val.strip() for val in value]

        # Очистка даних від HTML-тегів
        html_tags = re.compile(r'<[^>]+>')
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = html_tags.sub('', value)
            elif isinstance(value, list):
                item[key] = [html_tags.sub('', val) for val in value]

        return item

