from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QIntValidator
import sqlite3
import requests

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
        listArea={'Свердловкая область':1261,'Москва':1,'Курская область':1308,
                  'Новгородская область':1051,'Ростовская область':1530}
        k=listArea.keys()
        name=self.nameinput.text()
        sem = int(self.Seminput.text())
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        for el in k:
            if el==branch:
                n=listArea[el]
        url = 'https://api.hh.ru/vacancies/'
        par = {'text': name,'area':n,'per_page': '50','page': sem}
        for i in requests.get(url, params=par).json()['items']:
            key_skills_string = ''
            vac_id = i['id']
            vac_name = str(i['name'])+';'
            vacancy = requests.get('https://api.hh.ru/vacancies/' + vac_id).json()
            key_skills = vacancy['key_skills']
            for e in key_skills:
                skill = e['name']
                if skill is not None:
                    key_skills_string += skill + ','
            area = vacancy['area']
            if area['name'] is not None:
                town = area['name']+';'
            employer = vacancy['employer']
            if employer['name'] is not None:
                company = employer['name']+';'

            #Работа с DB
            self.conn = sqlite3.connect("Result.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO Result (name,area,employer,keySkills) VALUES (?,?,?,?)",
                       (vac_name, town, company, key_skills_string+';'))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            self.close()




