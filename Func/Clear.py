from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from Gui import Message


class ClearVacancy(object):
    def __init__(self):
        self.messages = Message.MessageWindow()

    def clear(self):
        if self.messages.show_question_message_window(QIcon(r'Images\Удалить.png'),
                                                      "Потверждение удаления",
                                                      "Удалить всё?"):
            connect_ = sqlite3.connect(r'Result.db')
            cursor_ = connect_.cursor()
            cursor_.execute("DELETE from Result")
            connect_.commit()
            connect_.close()
            self.messages.show_message_window(QMessageBox.Information,
                                              QIcon(r'Images\Удалить.png'),
                                              "Успешно!",
                                              "Вакансии удалены")
            return True
        else:
            return False
