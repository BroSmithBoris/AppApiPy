from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
from Gui import GuiSignal

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("Result.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS Result(name TEXT,area TEXT,employer TEXT,keySkills TEXT)")
        self.c.close()


        self.setWindowTitle("HH API")

        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("Images\Иконка.png"))
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.setHorizontalHeaderLabels(("Название","Город","Компания","Ключевые навыки"))
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("Images\Добавить.png"), "Добавить", self)
        btn_ac_adduser.triggered.connect(GuiSignal.insert)
        btn_ac_adduser.triggered.connect(self.loaddata)
        btn_ac_adduser.setStatusTip("Добавить")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("Images\Обновить.png"),"Обновить",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Обновить")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_delete = QAction(QIcon("Images\Удалить.png"), "Удалить", self)
        btn_ac_delete.triggered.connect(GuiSignal.delete)
        btn_ac_delete.triggered.connect(self.loaddata)
        btn_ac_delete.setStatusTip("Удалить")
        toolbar.addAction(btn_ac_delete)

        file_menu = self.menuBar().addMenu("&File")

        adduser_action = QAction(QIcon("icon/add.png"), "Сохранить файл", self)
        adduser_action.triggered.connect(GuiSignal.save)
        file_menu.addAction(adduser_action)

        about_action = QAction(QIcon("icon/info.png"), "Помощь", self)
        about_action.triggered.connect(GuiSignal.about)
        file_menu.addAction(about_action)
        self.loaddata()



    def loaddata(self):
        self.connection = sqlite3.connect("Result.db")
        query = "SELECT * FROM Result"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
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

