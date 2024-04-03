from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMessageBox, QTextEdit, QVBoxLayout, QComboBox, QHBoxLayout
from PyQt5.QtGui import QPainter, QLinearGradient, QIcon, QFont
from PyQt5.QtCore import Qt
import sys

#Наверно стоит написать этот класс в отдельном файле но это пока шаблон
# class GradientButton(QPushButton):
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#
#         gradient = QLinearGradient(0, 0, self.width(), self.height())
#         gradient.setColorAt(0, Qt.blue)
#         gradient.setColorAt(1, Qt.green)
#
#         painter.setBrush(gradient)
#         painter.setPen(Qt.NoPen)
#
#         painter.drawRoundedRect(self.rect(), 10, 10)

#Класс где переопрелен TextEditor что бы выводть подсказки
class PlaceholderTextEdit(QTextEdit):
    def __init__(self, placeholder_text, parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder_text
        self.setPlaceholderText(self.placeholder_text)
        self.textChanged.connect(self.handleTextChange)
        self.textChangedOnce = False

    def focusInEvent(self, event):
        if not self.textChangedOnce:
            self.clear()
        super().focusInEvent(event)

    def handleTextChange(self):
        self.textChangedOnce = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Краткий пересказ')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #ECFFFD;")
        # self.setWindowIcon(QIcon(''))

        # Создание основного виджета
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Создание вертикального макета для основного виджета
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Download button whitout gardient
        self.download_file_button = QPushButton('Загрузи файл', self)
        self.download_file_button.setStyleSheet("QPushButton {background-color: #7ED3D9; border-radius: 10px; font-size: 14pt; color: #0019FF; font-weight: semi bold;}")

        # Button for start algorithm
        self.start_button = QPushButton('Генери!!!', self)
        self.start_button.setStyleSheet("QPushButton {background-color: #7ED3D9; border-radius: 10px; font-size: 14pt; color: #0019FF; font-weight: semi bold;}")

        # Button for downlading answer
        self.answer_download_button = QPushButton('Сохрани ответ', self)
        self.answer_download_button.setStyleSheet("QPushButton {border-radius: 10px; background-color: #7ED3D9; font-size: 14pt; color: #0019FF; font-weight: semi bold;}")

        # The list of refering methods
        self.list_refering_methods = QComboBox(self)
        self.list_refering_methods.setStyleSheet("QComboBox {background-color: #7ED3D9; border-radius: 10px; font-size: 14pt; color: #0019FF; font-weight: semi bold;}")

        #text widgets
        self.request_text_frame = PlaceholderTextEdit('Вставь или напиши сюда текст который хочешь сократить', self)
        self.request_text_frame.setStyleSheet("background-color: #C2D4D5; border-radius: 10px; font-size: 14pt; color: #5D69D5; font-weight: semi bold;")

        self.answer_text_frame = PlaceholderTextEdit('Здесь будет краткое содержание', self)
        self.answer_text_frame.setStyleSheet("background-color: #C2D4D5; border-radius: 10px; font-size: 14pt; color: #5D69D5; font-weight: semi bold;")



        # Download button whith gardient
        # self.button = GradientButton('Загрузи файл', self)
        # self.button.setGeometry(25, 294, 120, 30)

        # Добавление кнопок в горизонтальный макет
        button_list_layout = QHBoxLayout()
        button_list_layout.addWidget(self.download_file_button)
        button_list_layout.addSpacing(240)
        button_list_layout.addWidget(self.list_refering_methods)
        button_list_layout.addWidget(self.start_button)

        answer_button_layout = QHBoxLayout()
        answer_button_layout.addSpacing(600)
        answer_button_layout.addWidget(self.answer_download_button)

        # Добавление всех виджетов в вертикальный макет
        main_layout.addWidget(self.request_text_frame)
        main_layout.addLayout(button_list_layout)
        main_layout.addWidget(self.answer_text_frame)
        main_layout.addLayout(answer_button_layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
