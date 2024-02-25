#1. Знайти відкрите джерело даних, що містить список підрозділів з URL для переходу
#на сторінку цього підрозділу. Кожна із сторінок повинна  містити список деяких об'єктів. 

#Сайт Маріупольського державного університету https://mu.edu.ua/uk

#2. Переконатись, що сторінки є статичними. Використовуючи бібліотеку requests завантажити сторінку зі списком та вивести в консоль.

from requests import get
from bs4 import BeautifulSoup
url = "https://mu.edu.ua/uk/faculties/"

list_of_faculties = get(url)

print(list_of_faculties.text)
print("-------------------------------------------------")

#3. Використовуючи бібліотеку Beautiful soap отримати список підрозділів та їх URL 
#5. Зберегти результати скрапінгу до текстового файлу.

FILE_NAME = "mdu.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:

    soup = BeautifulSoup(list_of_faculties.text, 'html.parser')
    faculties = soup.find(class_='links-list page-addition')
    for a in faculties.find_all('a'):
        fac_title = a.find('span').find(string=True, recursive=False)
        fac_link = a.get('href')
        
        file.write(f"Назва факультету: {fac_title}")
        file.write(f"Покликання: {fac_link}")
        file.write("--------------------------------------------------")

    #4. Використовуючи запити отримати списки із кожної зі сторінок підрозділів.

        fac_page = get(fac_link)

        soup = BeautifulSoup(fac_page.content, 'html.parser')
        dep_list = soup.find(class_= "faculty-department")

        if dep_list:
            for a in dep_list.find_all("a"):
                dep_title = a.find('span').find(string=True, recursive=False)
                dep_link = a.get('href')

                file.write(f"Назва кафедри: {dep_title}")
                file.write(f"Покликання: {dep_link}")
                file.write("------------------")

                dep_page = get(dep_link)

                soup = BeautifulSoup(dep_page.content, 'html.parser')
                staff_list = soup.find(class_= "department-teachers")
                teachers_list = staff_list.find_all(class_="teacher__name")
                if staff_list:
                    for teacher_name_span in teachers_list:
                        name = teacher_name_span.find(string=True, recursive=False)
                        file.write(f"Викладач кафедри: {name}")
                file.write("==============================================")
    print("--------------------------------------------------")
