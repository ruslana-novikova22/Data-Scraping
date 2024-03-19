import scrapy
from mdu.items import FacultyItem, DepartmentItem, StaffItem


class MduspiderXpathSpider(scrapy.Spider):
    name = "mduspider_xpath"
    allowed_domains = ["mu.edu.ua"]
    start_urls = ["https://mu.edu.ua/uk/faculties"]

    def parse(self, response):
        faculties = response.xpath('//div[@class="links-list page-addition"]//a')
        for faculty in faculties:
            fac_title = faculty.xpath('.//span/text()').get().strip()
            fac_link = faculty.xpath('./@href').get()
            yield FacultyItem(
                name=fac_title,
                url=fac_link
            )
            yield scrapy.Request(
                url=fac_link,
                callback=self.parse_faculty,
                meta={"faculty": fac_title}
            )

    def parse_faculty(self, response):
        faculty = response.meta.get("faculty")
        dep_list = response.xpath('//div[@class="faculty-department"]//a')
        for dep in dep_list:
            dep_title = f"Кафедра {dep.xpath('.//span/text()').get().strip()}"
            dep_link = dep.xpath('./@href').get()
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
        staff_list = response.xpath('//div[@class="department-teachers"]//span[@class="teacher__name"]')
        for teacher_name_span in staff_list:
            name = teacher_name_span.xpath('.//text()').get().strip()
            yield StaffItem(
                teacher=name,
                department=department
            )
