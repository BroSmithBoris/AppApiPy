import csv
import pandas as pd
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtWidgets import (QApplication, QComboBox,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QSizePolicy,
                             QStyleFactory, QTableWidget, QTabWidget,
                             QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox)
import sqlite3

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.topRightGroupBox, 3, 0)
        mainLayout.addWidget(self.bottomLeftTabWidget, 1,1,3,3)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("HH API")
        self.setMinimumSize(800, 600)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Сохранение")

        nameStr = QLabel()
        nameStr.setText("Имя файла:")
        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Имя")
        nameStrForm = QLabel()
        nameStrForm.setText("Формат:")
        self.branchinput = QComboBox()
        self.branchinput.addItem("CSV")
        self.branchinput.addItem("JSON")

        QBtnSave = QPushButton("Сохранить")
        QBtnSave.clicked.connect(self.addSave)
        layout = QVBoxLayout()
        layout.addWidget(nameStr)
        layout.addWidget(self.nameinput)
        layout.addWidget(nameStrForm)
        layout.addWidget(self.branchinput)
        layout.addWidget(QBtnSave)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def addSave(self):
        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        try:
            if branch=="CSV":
                csvWriter = csv.writer(open(name+'.csv', 'w', newline=''),delimiter=';')
                conn = sqlite3.connect('Result.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Result")
                rows = cursor.fetchall()
                for row in rows:
                    csvWriter.writerow(row)

            if branch =="JSON":
                conn = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result',conn).to_json(name+'.json')

            QMessageBox.information(QMessageBox(), 'Successful', 'Сохранено')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось сохранить')


    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Удалить все")

        defaultPushButton = QPushButton("Удалить все")
        defaultPushButton.clicked.connect(self.deleteAllWorks)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def deleteAllWorks(self):
        try:
            self.conn = sqlite3.connect("Result.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from Result")
            self.conn.commit()
            self.conn.close()
            self.loaddata
            QMessageBox.information(QMessageBox(), 'Successful', 'Удаленно')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось удалить вакансии')

    def createBottomLeftTabWidget(self):
        self.conn = sqlite3.connect("Result.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS Result(name TEXT,area TEXT,employer TEXT,keySkills TEXT)")
        self.c.close()
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Название", "Город", "Компания", "Ключевые навыки"))
        self.loaddata
        tab1hbox = QHBoxLayout()

        tab1hbox.addWidget(self.tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QLabel("""Инструкция
пользователю""")


        tab2hbox = QHBoxLayout()
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Help")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Добавить вакансии")


        self.name_Vac = QLineEdit()
        self.name_Vac.setPlaceholderText("Название")

        self.branchinput = QComboBox()
        self.branchinput.addItem("Свердловкая область")
        self.branchinput.addItem("Москва")
        self.branchinput.addItem("Ростовская область")
        self.branchinput.addItem("Курская область")
        self.branchinput.addItem("Новгородская область")

        QBtn = QPushButton("Добавить")
        QBtn.clicked.connect(self.addWork)

        layout = QGridLayout()
        layout.addWidget(self.name_Vac, 0, 0, 1, 2)
        layout.addWidget(self.branchinput, 1, 0, 1, 2)
        layout.addWidget(QBtn, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def addWork(self):
        listArea={'Свердловкая область':1261,'Москва':1,'Курская область':1308,
                  'Новгородская область':1051,'Ростовская область':1530}
        k=listArea.keys()
        name=self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        for el in k:
            if el==branch:
                n=listArea[el]
        url = 'https://api.hh.ru/vacancies/'
        par = {'text': name,'area':n,'per_page': '50','page': 0}
        for i in requests.get(url, params=par).json()['items']:
            key_skills_string = ''
            vac_id = i['id']
            vac_name = str(i['name'])+';'
            vacancy = requests.get('https://api.hh.ru/vacancies/' + vac_id).json()
            key_skills = vacancy['key_skills']
            for e in key_skills:
                skill = e['name']
                if skill is not None:
                    key_skills_string += skill + ', '
            if len(key_skills_string) > 0:
                key_skills_string = key_skills_string[0:-2] + ';'
            area = vacancy['area']
            if area['name'] is not None:
                town = area['name'] + ';'
            employer = vacancy['employer']
            if employer['name'] is not None:
                company = employer['name'] + ';'

            #Работа с DB
            self.conn = sqlite3.connect("Result.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO Result (name,area,employer,keySkills) VALUES (?,?,?,?)",
                       (vac_name, town, company, key_skills_string))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            self.loaddata



    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def loaddata(self):
        self.connection = sqlite3.connect("Result.db")
        query = "SELECT * FROM Result"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

