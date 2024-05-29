import scrapy

class FacultyItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

class DepartmentItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    faculty = scrapy.Field()

class StaffItem(scrapy.Item):
    teacher = scrapy.Field()
    department = scrapy.Field()
    img_url = scrapy.Field()
