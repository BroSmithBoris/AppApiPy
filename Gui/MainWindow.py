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
                             QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox, QHeaderView)
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

        main_layout = QGridLayout()
        main_layout.addWidget(self.top_left_group_box, 2, 0)
        main_layout.addWidget(self.top_right_group_box, 3, 0)
        main_layout.addWidget(self.bottom_left_tab_widget, 1, 1, 3, 3)
        main_layout.addWidget(self.bottom_right_group_box, 1, 0)
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        self.setLayout(main_layout)

        self.setWindowTitle("HH API")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("Images\Иконка.png"))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint
                            | QtCore.Qt.WindowMaximizeButtonHint)

    def create_top_left_group_box(self):
        self.top_left_group_box = QGroupBox("Сохранение")

        name_str = QLabel()
        name_str.setText("Имя файла:")
        self.save_name_input = QLineEdit()
        self.save_name_input.setPlaceholderText("Имя")
        name_str_form = QLabel()
        name_str_form.setText("Формат:")
        self.format_branch_input = QComboBox()
        self.format_branch_input.addItem("CSV")
        self.format_branch_input.addItem("JSON")
        self.format_branch_input.addItem("XLSX")

        button_save = QPushButton("Сохранить")
        button_save.clicked.connect(self.add_save)
        layout = QVBoxLayout()
        layout.addWidget(name_str)
        layout.addWidget(self.save_name_input)
        layout.addWidget(name_str_form)
        layout.addWidget(self.format_branch_input)
        layout.addWidget(button_save)
        layout.addStretch(1)
        self.top_left_group_box.setLayout(layout)

    def add_save(self):
        _name = self.save_name_input.text()
        _branch = self.format_branch_input.itemText(self.format_branch_input.currentIndex())
        try:
            if _branch == "CSV":
                _csv_writer = csv.writer(open(_name + '.csv', 'w', newline=''), delimiter=';')
                _connect = sqlite3.connect('Result.db')
                _cursor = _connect.cursor()
                _cursor.execute("SELECT * FROM Result")
                for row in _cursor.fetchall():
                    _csv_writer.writerow(row)

            elif _branch == "JSON":
                _connect = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result', _connect).to_json(_name + '.json')

            elif _branch == "XLSX":
                self.connect_ = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result', self.connect_).to_excel(_name + '.xlsx',
                                                                                  header=['Название', 'Город',
                                                                                          'Компания',
                                                                                          'Ключевые навыки'],
                                                                                  index=False)

            QMessageBox.information(QMessageBox(), 'Успешно!', 'Сохранено')
        except Exception as exception_:
            print(exception_)
            QMessageBox.warning(QMessageBox(), 'Ошибка!', 'Не удалось сохранить')

    def create_top_right_group_box(self):
        self.top_right_group_box = QGroupBox()

        default_push_button = QPushButton("Помощь")
        default_push_button.clicked.connect(self.about)

        layout = QVBoxLayout()
        layout.addWidget(default_push_button)
        layout.addStretch(1)
        self.top_right_group_box.setLayout(layout)

    def delete_all_works(self):
        _message = 'Вы уверены, что хотите продолжить?'
        _reply = QtWidgets.QMessageBox.question(self, 'Уведомление', _message,
                                                QtWidgets.QMessageBox.Yes,
                                                QtWidgets.QMessageBox.No)

        if _reply == QtWidgets.QMessageBox.Yes:
            self.connect_ = sqlite3.connect("Result.db")
            self.cursor = self.connect_.cursor()
            self.cursor.execute("DELETE from Result")
            self.connect_.commit()
            self.connect_.close()
            self.load_data()
            QMessageBox.information(QMessageBox(), 'Успешно!', 'Вакансии удалены')

    def create_bottom_left_tab_widget(self):
        self.connect_ = sqlite3.connect("Result.db")
        self.cursor = self.connect_.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Result(name TEXT,area TEXT,employer TEXT,keySkills TEXT)")
        self.cursor.close()
        self.bottom_left_tab_widget = QGroupBox()
        self.bottom_left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                                  QSizePolicy.Ignored)

        self.table_widget = QTableWidget()
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setColumnCount(4)
        self.table_widget.horizontalHeader().setCascadingSectionResizes(True)
        self.table_widget.horizontalHeader().setSortIndicatorShown(False)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().Stretch
        self.table_widget.verticalHeader().ResizeToContents
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.verticalHeader().setCascadingSectionResizes(True)
        self.table_widget.verticalHeader().setStretchLastSection(False)
        self.table_widget.setHorizontalHeaderLabels(("Название", "Город", "Компания", "Ключевые навыки"))
        self.load_data()
        table_h_box = QHBoxLayout()
        table_h_box.addWidget(self.table_widget)
        self.bottom_left_tab_widget.setLayout(table_h_box)

    def about(self):
        dialog = Help.AboutDialog()
        dialog.exec_()

    def create_bottom_right_group_box(self):
        self.bottom_right_group_box = QGroupBox("Добавить вакансии")

        self.vacancy_name_input = QLineEdit()
        self.vacancy_name_input.setPlaceholderText("Название")

        self.region_branch_input = QComboBox()
        self.region_branch_input.addItem("Свердловкая область")
        self.region_branch_input.addItem("Москва")
        self.region_branch_input.addItem("Ростовская область")
        self.region_branch_input.addItem("Курская область")
        self.region_branch_input.addItem("Новгородская область")

        button_add_work = QPushButton("Добавить")
        button_add_work.clicked.connect(self.add_work)
        push_button = QPushButton("Удалить все")
        push_button.clicked.connect(self.delete_all_works)

        layout = QGridLayout()
        layout.addWidget(self.vacancy_name_input, 0, 0, 1, 2)
        layout.addWidget(self.region_branch_input, 1, 0, 1, 2)
        layout.addWidget(button_add_work, 2, 0, 1, 2)
        layout.addWidget(push_button, 3, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.bottom_right_group_box.setLayout(layout)

    def add_work(self):
        def request_items(page):
            _vacancy_id_list = []
            _par = {'text': vacancy_name, 'area': area, 'per_page': '100', 'page': page}
            try:
                _vacancy_description_list = requests.get(url, params=_par).json()['items']
            except KeyError:
                return
            for _vacancy_description in _vacancy_description_list:
                _vacancy_id_list.append(url + _vacancy_description['id'])
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
                pool.map(request_vacancy_id, _vacancy_id_list)

        def request_vacancy_id(vacancy_url):
            try:
                _vacancy = requests.get(vacancy_url)
                assert (_vacancy.status_code == 200), ("Ошибка, Код ответа: ", _vacancy.status_code, vacancy_url)
            except Exception as exception_:
                print(exception_)
                time.sleep(5)
                return request_vacancy_id(vacancy_url)
            else:
                _key_skills_string = ''
                _vacancy = _vacancy.json()
                for _key_skill in _vacancy['key_skills']:
                    _skill = _key_skill['name']
                    if _skill is not None:
                        _key_skills_string += _skill + ', '

                self.connect_.execute("INSERT INTO Result (name,area,employer,keySkills) VALUES (?,?,?,?)",
                                      (_vacancy['name'], _vacancy['area']['name'], _vacancy['employer']['name'],
                                       _key_skills_string))

        _area_list = [1261, 1, 1308, 1051, 1530]
        vacancy_name = self.vacancy_name_input.text()
        area = _area_list[self.region_branch_input.currentIndex()]
        url = 'https://api.hh.ru/vacancies/'
        self.connect_ = Sqlite3Worker("Result.db")
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            pool.map(request_items, range(20))
        self.connect_.close()
        self.load_data()

    def load_data(self):
        self.connect_ = sqlite3.connect("Result.db")
        _result = self.connect_.execute("SELECT * FROM Result")
        self.table_widget.setRowCount(0)
        for row_number, row_data in enumerate(_result):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.connect_.close()
