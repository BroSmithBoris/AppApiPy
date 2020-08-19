from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog


class AboutDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("HH API")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        layout.addWidget(QLabel("""Тут 
может быть                           
инструкция"""))

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
