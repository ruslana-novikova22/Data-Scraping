import os
import scrapy
import requests
from mdu.items import FacultyItem, DepartmentItem, StaffItem

class MduspiderSpider(scrapy.Spider):
    name = "mduspider"
    allowed_domains = ["mu.edu.ua"]
    start_urls = ["https://mu.edu.ua/uk/faculties"]

    def parse(self, response):
        faculties = response.css('.links-list.page-addition a')
        for a in faculties:
            fac_title = a.css('span::text').get().strip()
            fac_link = response.urljoin(a.attrib['href'])
            faculty_item = FacultyItem(
                name=fac_title,
                url=fac_link
            )
            self.send_data('http://localhost:3000/api/faculties', faculty_item)
            yield scrapy.Request(
                url=fac_link,
                callback=self.parse_faculty,
                meta={"faculty": fac_title}
            )

    def parse_faculty(self, response):
        faculty = response.meta.get("faculty")
        departments = response.css('.flex.flex-col.gap-3 a')
        for a in departments:
            dep_title = f"Кафедра {a.css('span::text').get().strip()}"
            dep_link = response.urljoin(a.attrib['href'])
            department_item = DepartmentItem(
                name=dep_title,
                url=dep_link,
                faculty=faculty
            )
            self.send_data('http://localhost:3000/api/departments', department_item)
            yield scrapy.Request(
                url=dep_link,
                callback=self.parse_department,
                meta={"department": dep_title}
            )

    def parse_department(self, response):
        department = response.meta.get("department")
        staff_list = response.css('.flex-1.flex.flex-col.items-center.p-8')
        for teacher_info in staff_list:
            img_url = response.urljoin(teacher_info.css('img::attr(src)').get())
            name = teacher_info.css('span::text').get().strip()

            filename = os.path.basename(img_url)

            if not os.path.exists('img'):
                os.makedirs('img')

            filepath = f'img/{filename}'
            with open(filepath, 'wb') as f:
                f.write(response.body)

            staff_item = StaffItem(
                teacher=name,
                department=department,
                img_url=img_url,
                img_path=filepath  
            )
            self.send_data('http://localhost:3000/api/staff', staff_item)

    def send_data(self, url, item):
        data = dict(item)
        response = requests.post(url, json=data)
        if response.status_code != 201:
            self.log(f"Не вдалося надіслати дані до {url}: {response.content}")
