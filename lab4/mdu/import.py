import sqlite3
import xml.etree.ElementTree as ET

tree = ET.parse('output.xml')
root = tree.getroot()

conn = sqlite3.connect('university.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Faculty (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Department (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT,
    faculty_id INTEGER,
    FOREIGN KEY(faculty_id) REFERENCES Faculty(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Lecturer (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    img_url TEXT,
    department_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES Department(id)
)
''')

faculties = {}
departments = {}

for item in root.findall('item'):
    if item.find('teacher') is None:
        name = item.find('name').text
        url = item.find('url').text
        
        faculty_name = item.find('faculty')
        
        if faculty_name is None:
            cursor.execute('INSERT INTO Faculty (name, url) VALUES (?, ?)', (name, url))
            faculty_id = cursor.lastrowid
            faculties[name] = faculty_id
        else:
            faculty_id = faculties[faculty_name.text]
            cursor.execute('INSERT INTO Department (name, url, faculty_id) VALUES (?, ?, ?)', (name, url, faculty_id))
            department_id = cursor.lastrowid
            departments[name] = department_id
    else:
        name = item.find('teacher').text
        img_url = item.find('img_url').text
        department_name = item.find('department').text
        
        department_id = departments[department_name]
        cursor.execute('INSERT INTO Lecturer (name, img_url, department_id) VALUES (?, ?, ?)', (name, img_url, department_id))

conn.commit()

conn.close()
