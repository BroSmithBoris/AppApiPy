import csv
import xlsxwriter
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
import sqlite3


class SaveVacancy(object):

    def save(self, name, branch):
        name = name
        branch = branch
        connect_ = sqlite3.connect('Result.db')
        try:
            if branch == "CSV":
                _csv_writer = csv.writer(open(name + '.csv', 'w', newline=''), delimiter=';')
                _cursor = connect_.cursor()
                _cursor.execute("SELECT * FROM Result")
                for row in _cursor.fetchall():
                    _csv_writer.writerow(row)

            elif branch == "JSON":
                pd.read_sql_query('SELECT * FROM Result', connect_).to_json(name + '.json')

            elif branch == "XLSX":
                pd.read_sql_query('SELECT * FROM Result', connect_).to_excel(name + '.xlsx',
                                                                             header=['Название', 'Город',
                                                                                     'Компания',
                                                                                     'Ключевые навыки'],
                                                                             index=False)

            QMessageBox.information(QMessageBox(), 'Успешно!', 'Сохранено')
        except Exception as exception_:
            print(exception_)
            QMessageBox.warning(QMessageBox(), 'Ошибка!', 'Не удалось сохранить')
        connect_.close()
