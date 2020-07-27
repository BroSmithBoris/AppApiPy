from PyQt5.QtWidgets import *
import sqlite3

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Поиск")

        self.setWindowTitle("Поиск вакансии")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchWorks)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("Название вакансии")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)


    def searchWorks(self):

        searchrol = self.searchinput.text()
        self.conn = sqlite3.connect("Result.db")
        self.c = self.conn.cursor()
        result = self.c.execute("SELECT * FROM Result WHERE name ="+str(searchrol))
        row=result.fetchall()
        QMessageBox.information(QMessageBox(), 'Successful')
        self.conn.commit()
        self.c.close()
        self.conn.close()




