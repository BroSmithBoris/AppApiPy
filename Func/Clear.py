from PyQt5.QtWidgets import QMessageBox
import sqlite3


class ClearVacancy(object):

    def clear(self):
        _message = 'Вы уверены, что хотите продолжить?'
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle("Потверждение удаления")
        msgBox.addButton("Нет", QMessageBox.NoRole)
        msgBox.setText("Удалить всё?")
        connectButton = msgBox.addButton("Да", QMessageBox.YesRole)
        msgBox.windowTitle()
        msgBox.exec()

        if msgBox.clickedButton() == connectButton:
            connect_ = sqlite3.connect("Result.db")
            _cursor = connect_.cursor()
            _cursor.execute("DELETE from Result")
            connect_.commit()
            connect_.close()
            QMessageBox.information(QMessageBox(), 'Успешно!', 'Вакансии удалены')
            return True
        else:
            return False
