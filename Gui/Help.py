from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog


class AboutDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)
        self.setWindowIcon(QIcon(r'Images\Помощь.png'))
        self.setWindowTitle("Помощь")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        text_lable = QLabel()
        text_lable.setText("Поиск по словам позволяет находить\nвакансии и резюме, в тексте которых\nсодержатся "
                           "интересующие вас ключевые\nслова или фразы.\nПри этом вы можете использовать\nспециальный "
                           "язык запросов, позволяющий\nуправлять поиском.\nС помощью этого языка можно "
                           "выполнять\nдостаточно сложные поисковые задачи.\nПодробно можете прочитать здесь:\n")
        url_lable = QLabel()
        url_lable.setText('<a href="https://hh.ru/article/1175/">Язык поисковых запросов HH.ru</a>')
        url_lable.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        url_lable.setOpenExternalLinks(True)
        layout = QVBoxLayout()
        layout.addWidget(text_lable)
        layout.addWidget(url_lable)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
