from PyQt5.QtWidgets import QMessageBox


class MessageWindow(object):
    def show_question_message_window(self, window_icon, window_title_text, text):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Question)
        message_box.setWindowTitle(window_title_text)
        message_box.setText(text)
        message_box.addButton("Нет", QMessageBox.NoRole)
        yes_button = message_box.addButton("Да", QMessageBox.YesRole)
        message_box.setWindowIcon(window_icon)
        message_box.exec()
        return message_box.clickedButton() == yes_button

    def show_message_window(self, icon, window_icon, window_title_text, text):
        message_box = QMessageBox()
        message_box.setIcon(icon)
        message_box.setWindowTitle(window_title_text)
        message_box.setText(text)
        message_box.addButton("Хорошо", QMessageBox.AcceptRole)
        message_box.setWindowIcon(window_icon)
        message_box.exec()