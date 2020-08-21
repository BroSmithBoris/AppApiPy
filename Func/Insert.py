from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QIntValidator
import sqlite3
import requests
import concurrent
import time
import concurrent.futures
from sqlite3worker import Sqlite3Worker


#Интерфейс
class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)
        self.QBtn = QPushButton()
        self.QBtn.setText("Добавить")
        self.setWindowTitle("Добавить")
        self.setWindowIcon(QIcon("Images\Добавить.png"))
        self.setFixedWidth(300)
        self.setFixedHeight(250)
        self.QBtn.clicked.connect(self.addWork)
        layout = QVBoxLayout()

        self.nameStr=QLabel()
        self.nameStr.setText("Название вакансии:")
        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Название")
        layout.addWidget(self.nameStr)
        layout.addWidget(self.nameinput)

        self.nameStr=QLabel()
        self.nameStr.setText("Номер страницы:")
        self.Seminput = QLineEdit()
        self.onlyInt=QIntValidator()
        self.Seminput.setValidator(self.onlyInt)
        self.Seminput.setPlaceholderText("№")
        layout.addWidget(self.nameStr)
        layout.addWidget(self.Seminput)

        self.nameStr = QLabel()
        self.nameStr.setText("Область:")
        self.branchinput = QComboBox()
        self.branchinput.addItem("Свердловкая область")
        self.branchinput.addItem("Москва")
        self.branchinput.addItem("Ростовская область")
        self.branchinput.addItem("Курская область")
        self.branchinput.addItem("Новгородская область")
        layout.addWidget(self.nameStr)
        layout.addWidget(self.branchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    #Функция
    def addWork(self):
        def request(url):
            try:
                vacancy = requests.get(url)
                assert (vacancy.status_code == 200), ("Ошибка, Код ответа: ", vacancy.status_code, url)
            except Exception as e:
                print(e)
                time.sleep(1)
                return self.request(url)
            else:
                key_skills_string = ''
                vacancy = vacancy.json()
                key_skills = vacancy['key_skills']
                for e in key_skills:
                    skill = e['name']
                    if skill is not None:
                        key_skills_string += skill + ', '
                area = vacancy['area']
                employer = vacancy['employer']

                print("check")
                conn.execute("INSERT INTO Result (name,area,employer,keySkills) VALUES (?,?,?,?)",
                               (vacancy['name'], area['name'], employer['name'], key_skills_string))
                print(conn.queue_size)
                return 0

        listArea={'Свердловкая область':1261,'Москва':1,'Курская область':1308,
                  'Новгородская область':1051,'Ростовская область':1530}
        k=listArea.keys()
        name=self.nameinput.text()
        sem = int(self.Seminput.text())
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        for el in k:
            if el == branch:
                n=listArea[el]

        count = 0
        count_check = 0
        page = 0
        url = 'https://api.hh.ru/vacancies/'
        print('ID Вакансии\tОбъявление\tГород\tКомпания\tКлючевые навыки')
        vac_id_list = []
        while True:
            par = {'text': name, 'area': n, 'per_page': '100', 'page': page}
            # 1261 -- Свердловская область
            try:
                items = requests.get(url, params=par).json()['items']
            except KeyError:
                break
            for i in items:
                vac_id_list.append(url + i['id'])
                count += 1
            if count_check == count:
                break
            else:
                count_check = count
                page += 1
        print(count)
        conn = Sqlite3Worker("Result.db")
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as pool:
            pool.map(request, vac_id_list)
        conn.close()
        self.close()




