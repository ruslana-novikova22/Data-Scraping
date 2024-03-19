import scrapy
from mdu.items import FacultyItem, DepartmentItem, StaffItem

class MduspiderCssSpider(scrapy.Spider):
    name = "mduspider_css"
    allowed_domains = ["mu.edu.ua"]
    start_urls = ["https://mu.edu.ua/uk/faculties"]

    def parse(self, response):
        faculties = response.css('.links-list.page-addition')
        for a in faculties.css('a'):
            fac_title = a.css('span::text').get().strip()
            fac_link = a.css('::attr(href)').get()
            yield FacultyItem(
                name=fac_title,
                url=fac_link
            )
            yield scrapy.Request(
                url=fac_link,
                callback=self.parse_faculty,
                meta={
                    "faculty": fac_title
                }
            )

    def parse_faculty(self, response):
        faculty = response.meta.get("faculty")
        dep_list = response.css(".faculty-department")
        for a in dep_list.css("a"):
            dep_title = f"Кафедра {a.css('span::text').get().strip()}"
            dep_link = a.css('::attr(href)').get()
            yield DepartmentItem(
                name=dep_title,
                url=dep_link,
                faculty=faculty
            )
            yield scrapy.Request(
                url=dep_link,
                callback=self.parse_department,
                meta={"department": dep_title}
            )

    def parse_department(self, response):
        department = response.meta.get("department")
        staff_list = response.css(".department-teachers")
        teachers_list = staff_list.css(".teacher__name::text").getall()
        for teacher_name in teachers_list:
            yield StaffItem(
                teacher=teacher_name,
                department=department
            )