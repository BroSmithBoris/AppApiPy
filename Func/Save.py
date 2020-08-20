import sqlite3
import csv
import os
import pandas as pd
import json
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox, QMessageBox


class SaveDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(SaveDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Сохранить")
        self.setWindowTitle("Сохранить")
        self.setWindowIcon(QIcon("Images\помощь.png"))
        self.setFixedWidth(300)
        self.setFixedHeight(250)
        self.QBtn.clicked.connect(self.addSave)
        layout = QVBoxLayout()

        self.nameStr = QLabel()
        self.nameStr.setText("Имя файла:")
        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Имя")
        layout.addWidget(self.nameStr)
        layout.addWidget(self.nameinput)

        self.nameStr = QLabel()
        self.nameStr.setText("Формат:")
        self.branchinput = QComboBox()
        self.branchinput.addItem("CSV")
        self.branchinput.addItem("JSON")
        layout.addWidget(self.nameStr)
        layout.addWidget(self.branchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addSave(self):
        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        inputFolder =r'C:\Users\Человек\PycharmProjects\AppApi'
        try:
            if branch=="CSV":
                csvWriter = csv.writer(open(inputFolder + '/'+name+'.csv', 'w', newline=''),delimiter=';')
                conn = sqlite3.connect('Result.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Result")
                rows = cursor.fetchall()
                for row in rows:
                    csvWriter.writerow(row)

            if branch =="JSON":
                conn = sqlite3.connect('Result.db')
                pd.read_sql_query('SELECT * FROM Result',conn).to_json(inputFolder+'/'+name+'.json')

            QMessageBox.information(QMessageBox(), 'Successful', 'Сохранено')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Не удалось сохранить')
