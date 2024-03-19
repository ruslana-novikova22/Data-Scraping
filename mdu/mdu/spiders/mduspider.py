import scrapy
from bs4 import BeautifulSoup
from mdu.items import FacultyItem, DepartmentItem, StaffItem


class MduspiderSpider(scrapy.Spider):
    name = "mduspider"
    allowed_domains = ["mu.edu.ua"]
    start_urls = ["https://mu.edu.ua/uk/faculties"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        faculties = soup.find(class_='links-list page-addition')
        for a in faculties.find_all('a'):
            fac_title = a.find('span').find(string=True).strip()
            fac_link = a.get('href')
            yield FacultyItem(
                name = fac_title,
                url = fac_link
            )
            yield scrapy.Request(
                url = fac_link,
                callback=self.parse_faculty,
                meta={
                    "faculty": fac_title
                }
            )

    def parse_faculty(self, response):
        faculty = response.meta.get("faculty")
        soup = BeautifulSoup(response.body, 'html.parser')
        dep_list = soup.find(class_= "faculty-department")
        for a in dep_list.find_all("a"):
            dep_title = f"Кафедра {a.find('span').find(string=True, recursive=False).strip()}"
            dep_link = a.get('href')
            yield DepartmentItem(
                name = dep_title,
                url = dep_link,
                faculty = faculty
            )
            yield scrapy.Request(
                url = dep_link,
                callback = self.parse_department,
                meta ={"department": dep_title}
            )

    def parse_department(self,response):
        department = response.meta.get("department")
        soup = BeautifulSoup(response.body, 'html.parser')
        staff_list = soup.find(class_= "department-teachers")
        teachers_list = staff_list.find_all(class_="teacher__name")
        for teacher_name_span in teachers_list:
            name = teacher_name_span.find(string=True, recursive=False)
            yield StaffItem(
                teacher = name,
                department = department
            )
