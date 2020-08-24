import csv
import xlsxwriter
import pandas as pd
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextDocument, QTextCursor, QIcon
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
from Func import Help

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
        self.setWindowIcon(QIcon("Images\Иконка.png"))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint
                            | QtCore.Qt.WindowMaximizeButtonHint)

    def advance_progress_bar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def create_top_left_group_box(self):
        self.topLeftGroupBox = QGroupBox("Сохранение")

        nameStr = QLabel()
        nameStr.setText("Имя файла:")
        self.saveNameInput = QLineEdit()
        self.saveNameInput.setPlaceholderText("Имя")
        nameStrForm = QLabel()
        nameStrForm.setText("Формат:")
        self.formatBranchInput = QComboBox()
        self.formatBranchInput.addItem("CSV")
        self.formatBranchInput.addItem("JSON")
        self.formatBranchInput.addItem("XLSX")


        QBtnSave = QPushButton("Сохранить")
        QBtnSave.clicked.connect(self.add_save)
        layout = QVBoxLayout()
        layout.addWidget(nameStr)
        layout.addWidget(self.saveNameInput)
        layout.addWidget(nameStrForm)
        layout.addWidget(self.formatBranchInput)
        layout.addWidget(QBtnSave)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def add_save(self):
        name = self.saveNameInput.text()
        branch = self.formatBranchInput.itemText(self.formatBranchInput.currentIndex())
        try:
            if branch == "CSV":
                csvWriter = csv.writer(open(name + '.csv', 'w', newline=''), delimiter=';')
                conn = sqlite3.connect('Result.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Result")
                rows = cursor.fetchall()
                for row in rows:
                    csvWriter.writerow(row)

            if branch == "JSON":
                conn = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result', conn).to_json(name + '.json')

            if branch == "XLSX":
                self.connect = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result', self.connect).to_excel(name + '.xlsx',
                                                                                 header=['Название', 'Город', 'Компания', 'Ключевые навыки'], index=False)

            QMessageBox.information(QMessageBox(), 'Successful', 'Сохранено')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось сохранить')

    def create_top_right_group_box(self):
        self.topRightGroupBox = QGroupBox()

        defaultPushButton = QPushButton("Помощь")
        defaultPushButton.clicked.connect(self.about)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def delete_all_works(self):
        message = 'Вы уверены, что хотите продолжить?'
        reply = QtWidgets.QMessageBox.question(self, 'Уведомление', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.connect = sqlite3.connect("Result.db")
            self.cursor = self.connect.cursor()
            self.cursor.execute("DELETE from Result")
            self.connect.commit()
            self.connect.close()
            self.load_data()
            QMessageBox.information(QMessageBox(), 'Successful', 'Удаленно')
        elif reply==QtWidgets.QMessageBox.No:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось удалить вакансии')

    def create_bottom_left_tab_widget(self):
        self.connect = sqlite3.connect("Result.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Result(name TEXT,area TEXT,employer TEXT,keySkills TEXT)")
        self.cursor.close()
        self.bottomLeftTabWidget = QGroupBox()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)

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
        self.bottomLeftTabWidget.setLayout(tab1hbox)

    def about(self):
        dlg = Help.AboutDialog()
        dlg.exec_()

    def create_bottom_right_group_box(self):
        self.bottomRightGroupBox = QGroupBox("Добавить вакансии")

        self.vacancyNameInput = QLineEdit()
        self.vacancyNameInput.setPlaceholderText("Название")

        self.regionBranchInput = QComboBox()
        self.regionBranchInput.addItem("Свердловкая область")
        self.regionBranchInput.addItem("Москва")
        self.regionBranchInput.addItem("Ростовская область")
        self.regionBranchInput.addItem("Курская область")
        self.regionBranchInput.addItem("Новгородская область")

        QBtn = QPushButton("Добавить")
        QBtn.clicked.connect(self.add_work)
        defaultPushButton = QPushButton("Удалить все")
        defaultPushButton.clicked.connect(self.delete_all_works)

        layout = QGridLayout()
        layout.addWidget(self.vacancyNameInput, 0, 0, 1, 2)
        layout.addWidget(self.regionBranchInput, 1, 0, 1, 2)
        layout.addWidget(QBtn, 2, 0, 1, 2)
        layout.addWidget(defaultPushButton, 3, 0, 1, 2)
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
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
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
        name = self.vacancyNameInput.text()
        branch = self.regionBranchInput.itemText(self.formatBranchInput.currentIndex())
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
