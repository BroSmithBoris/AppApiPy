from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog


class AboutDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)
        self.setWindowIcon(QIcon("Images\помощь.png"))
        self.setWindowTitle("Помощь")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("""Тут 
может быть                           
инструкция"""))

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
