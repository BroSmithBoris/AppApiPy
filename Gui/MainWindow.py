import csv
import pandas as pd
import xlrd
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtWidgets import (QApplication, QComboBox,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QSizePolicy,
                             QStyleFactory, QTableWidget, QTabWidget,
                             QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox)
import sqlite3
import concurrent
import time
import concurrent.futures
from sqlite3worker import Sqlite3Worker

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.create_top_left_group_box()
        self.create_top_right_group_box()
        self.create_bottom_left_tab_widget()
        self.create_bottom_right_group_box()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.topRightGroupBox, 3, 0)
        mainLayout.addWidget(self.bottomLeftTabWidget, 1, 1, 3, 3)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("HH API")
        self.setMinimumSize(800, 600)

    def advance_progress_bar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def create_top_left_group_box(self):
        self.topLeftGroupBox = QGroupBox("Сохранение")

        nameStr = QLabel()
        nameStr.setText("Имя файла:")
        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Имя")
        nameStrForm = QLabel()
        nameStrForm.setText("Формат:")
        self.formatbranchinput = QComboBox()
        self.formatbranchinput.addItem("CSV")
        self.formatbranchinput.addItem("JSON")

        QBtnSave = QPushButton("Сохранить")
        QBtnSave.clicked.connect(self.add_save)
        layout = QVBoxLayout()
        layout.addWidget(nameStr)
        layout.addWidget(self.nameinput)
        layout.addWidget(nameStrForm)
        layout.addWidget(self.formatbranchinput)
        layout.addWidget(QBtnSave)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def add_save(self):
        name = self.nameinput.text()
        branch = self.formatbranchinput.itemText(self.formatbranchinput.currentIndex())
        try:
            print(branch)
            if branch == "CSV":
                self.conn = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result', self.conn).to_csv(name + '.cvs')

            if branch == "JSON":
                self.conn = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result', self.conn).to_json(name + '.json')
            QMessageBox.information(QMessageBox(), 'Successful', 'Сохранено')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось сохранить')

    def create_top_right_group_box(self):
        self.topRightGroupBox = QGroupBox("Удалить все")

        defaultPushButton = QPushButton("Удалить все")
        defaultPushButton.clicked.connect(self.delete_all_works)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def delete_all_works(self):
        try:
            self.conn = sqlite3.connect("Result.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from Result")
            self.conn.commit()
            self.conn.close()
            self.load_data()
            QMessageBox.information(QMessageBox(), 'Successful', 'Удаленно')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось удалить вакансии')

    def create_bottom_left_tab_widget(self):
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
        self.load_data()
        tab1hbox = QHBoxLayout()

        tab1hbox.addWidget(self.tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QLabel("Инструкция\nпользователю")

        tab2hbox = QHBoxLayout()
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Help")

    def create_bottom_right_group_box(self):
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
        QBtn.clicked.connect(self.add_work)

        layout = QGridLayout()
        layout.addWidget(self.name_Vac, 0, 0, 1, 2)
        layout.addWidget(self.branchinput, 1, 0, 1, 2)
        layout.addWidget(QBtn, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def add_work(self):
        def request_items(page):
            vac_id_list = []
            par = {'text': name, 'area': n, 'per_page': '100', 'page': page}
            try:
                items = requests.get(url, params=par).json()['items']
            except KeyError:
                return
            for i in items:
                vac_id_list.append(url + i['id'])
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
                pool.map(request_vac_id, vac_id_list)

        def request_vac_id(vac_url):
            try:
                vacancy = requests.get(vac_url)
                assert (vacancy.status_code == 200), ("Ошибка, Код ответа: ", vacancy.status_code, vac_url)
            except Exception as e:
                print(e)
                time.sleep(5)
                return request_vac_id(vac_url)
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

                conn.execute("INSERT INTO Result (name,area,employer,keySkills) VALUES (?,?,?,?)",
                             (vacancy['name'], area['name'], employer['name'], key_skills_string))
                print(conn.queue_size)
                return 0

        listArea = {'Свердловкая область': 1261, 'Москва': 1, 'Курская область': 1308,
                    'Новгородская область': 1051, 'Ростовская область': 1530}
        k = listArea.keys()
        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        for el in k:
            if el == branch:
                n = listArea[el]
        url = 'https://api.hh.ru/vacancies/'
        conn = Sqlite3Worker("Result.db")
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            pool.map(request_items, range(20))
        conn.close()
        self.load_data()

    def load_data(self):
        self.connection = sqlite3.connect("Result.db")
        query = "SELECT * FROM Result"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.connection.close()

    def handle_paint_request(self, printer):
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
