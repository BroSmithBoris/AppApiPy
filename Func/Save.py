import csv
import xlsxwriter
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from Gui import Message


class SaveVacancy(object):
    def __init__(self):
        self.messages = Message.MessageWindow()

    def save(self, name, branch):
        name = name
        branch = branch
        connect_ = sqlite3.connect(r'Result.db')
        try:
            if branch == "CSV":
                _csv_writer = csv.writer(open(name + '.csv', 'w', newline=''), delimiter=';')
                cursor_ = connect_.cursor()
                cursor_.execute("SELECT * FROM Result")
                for row in cursor_.fetchall():
                    _csv_writer.writerow(row)

            elif branch == "JSON":
                pd.read_sql_query("SELECT * FROM Result", connect_).to_json(name + '.json')

            elif branch == "XLSX":
                pd.read_sql_query("SELECT * FROM Result", connect_).to_excel(name + '.xlsx',
                                                                             header=['ID', 'Название', 'Город',
                                                                                     'Компания',
                                                                                     'Ключевые навыки'],
                                                                             index=False,
                                                                             engine='xlsxwriter')
            self.messages.show_message_window(QMessageBox.Information,
                                              QIcon(r'Images\Добавить.png'),
                                              "Успешно!",
                                              "Сохранено")
        except Exception as exception_:
            print(exception_)
            self.messages.show_message_window(QMessageBox.Critical,
                                              QIcon(r'Images\Добавить.png'),
                                              "Ошибка!",
                                              "Не удалось сохранить")
        connect_.close()
