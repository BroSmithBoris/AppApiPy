from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QDialog, QGridLayout, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QSizePolicy, QTableWidget, QVBoxLayout, QTableWidgetItem, \
    QHeaderView
import sqlite3
from Gui import Help, Message
from Func import Request, Save, Clear


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.AREA_LIST = [1261, 1, 1308, 1051, 1530]
        self.URL = r'https://api.hh.ru/vacancies/'
        self.messages = Message.MessageWindow()
        self.request_vacancy = Request.RequestVacancy(self.URL)
        self.save_vacancy = Save.SaveVacancy()
        self.clear_vacancy = Clear.ClearVacancy()

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
        self.setWindowIcon(QIcon(r'Images\Иконка.png'))
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

    def create_top_right_group_box(self):
        self.top_right_group_box = QGroupBox()

        default_push_button = QPushButton("Помощь")
        default_push_button.clicked.connect(self.about)

        layout = QVBoxLayout()
        layout.addWidget(default_push_button)
        layout.addStretch(1)
        self.top_right_group_box.setLayout(layout)

    def create_bottom_left_tab_widget(self):
        self.connect_ = sqlite3.connect(r'Result.db')
        self.cursor = self.connect_.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Result(id TEXT, name TEXT,area TEXT,employer TEXT,keySkills TEXT)")
        self.cursor.close()
        self.bottom_left_tab_widget = QGroupBox()
        self.bottom_left_tab_widget.setSizePolicy(QSizePolicy.Preferred,
                                                  QSizePolicy.Ignored)

        self.table_widget = QTableWidget()
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setColumnCount(5)
        self.table_widget.horizontalHeader().setCascadingSectionResizes(True)
        self.table_widget.horizontalHeader().setSortIndicatorShown(False)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().Stretch
        self.table_widget.verticalHeader().ResizeToContents
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.verticalHeader().setCascadingSectionResizes(True)
        self.table_widget.verticalHeader().setStretchLastSection(False)
        self.table_widget.setHorizontalHeaderLabels(("ID", "Название", "Город", "Компания", "Ключевые навыки"))
        self.load_data()
        table_h_box = QHBoxLayout()
        table_h_box.addWidget(self.table_widget)
        self.bottom_left_tab_widget.setLayout(table_h_box)

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

    def delete_all_works(self):
        if self.clear_vacancy.clear():
            self.load_data()

    def add_work(self):
        self.request_vacancy.request(self.vacancy_name_input.text(),
                                     self.AREA_LIST[self.region_branch_input.currentIndex()],
                                     )
        self.load_data()

    def add_save(self):
        _name = self.save_name_input.text()
        _branch = self.format_branch_input.itemText(self.format_branch_input.currentIndex())
        self.save_vacancy.save(self.save_name_input.text(),
                               self.format_branch_input.itemText(self.format_branch_input.currentIndex()))

    def about(self):
        dialog = Help.AboutDialog()
        dialog.exec()

    def load_data(self):
        self.connect_ = sqlite3.connect(r'Result.db')
        _result = self.connect_.execute("SELECT * FROM Result")
        self.table_widget.setRowCount(0)
        for row_number, row_data in enumerate(_result):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.connect_.close()
