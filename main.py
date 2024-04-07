from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMessageBox, QTextEdit, QVBoxLayout, QComboBox, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPainter, QLinearGradient, QIcon, QFont
from PyQt5.QtCore import Qt
import sys

import nltk
nltk.download('punkt')

import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer

LANGUAGE = "russian"
SENTECES_COUNT = 1

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
        self.setWindowTitle('Summarizer')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #ECFFFD;")
        # self.setWindowIcon(QIcon(''))

        # Download button whitout gardient
        self.download_file_button = QPushButton('Upload file', self)
        self.download_file_button.setStyleSheet("QPushButton {background-color: #7ED3D9; border-radius: 10px; font-size: 14pt; color: black; font-weight: semi bold;}")
        # self.download_file_button.connect(self.download_file_button_click)

        # The list of refering methods
        self.list_refering_methods = QComboBox(self)
        self.list_refering_methods.setStyleSheet("QComboBox {background-color: #7ED3D9; border-radius: 10px; font-size: 14pt; color: black; font-weight: semi bold;}")
        self.list_refering_methods.addItems(["LSA", "Lung", "LexRank"])

        # Button for start algorithm
        self.start_button = QPushButton('Generate', self)
        self.start_button.setStyleSheet("QPushButton {background-color: #7ED3D9; border-radius: 10px; font-size: 14pt; color: black; font-weight: semi bold;}")
        self.start_button.clicked.connect(self.start_button_click)

        # Button for downlading answer
        self.answer_download_button = QPushButton('Save answer', self)
        self.answer_download_button.setStyleSheet("QPushButton {border-radius: 10px; background-color: #7ED3D9; font-size: 14pt; color: black; font-weight: semi bold;}")
        # self.answer_download_button.connect(self.answer_download_button_click)

        #text widgets
        self.request_text_frame = PlaceholderTextEdit('Insert your text here', self)
        self.request_text_frame.setStyleSheet("background-color: #C2D4D5; border-radius: 10px; font-size: 14pt; color: black; font-weight: semi bold;")

        self.answer_text_frame = PlaceholderTextEdit('Here will be your short version of text', self)
        self.answer_text_frame.setStyleSheet("background-color: #C2D4D5; border-radius: 10px; font-size: 14pt; color: black; font-weight: semi bold;")

        # Создание основного виджета
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Создание вертикального макета для основного виджета
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

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

    def start_button_click(self):
        self.answer_text_frame.clear()
        if self.request_text_frame.toPlainText():
            parser = PlaintextParser.from_string(str(self.request_text_frame.toPlainText()), Tokenizer(LANGUAGE))
            stemmer = Stemmer(LANGUAGE)
            selected_variant_of_refering_methods = self.list_refering_methods.currentText()
            if selected_variant_of_refering_methods == "LSA":
                lsa_summarizer = LsaSummarizer(stemmer)
                lsa_summarizer.stop_words = get_stop_words(LANGUAGE)
                for sentence in lsa_summarizer(parser.document, SENTECES_COUNT):
                    self.answer_text_frame.append(str(sentence))
            elif selected_variant_of_refering_methods == "Lung":
                summarizer_luhn = LuhnSummarizer()
                summary_1 = summarizer_luhn(parser.document, SENTECES_COUNT)
                for sentence in summary_1:
                    self.answer_text_frame.append(str(sentence))
            elif selected_variant_of_refering_methods == "LexRank":
                summarizer = LexRankSummarizer()
                lex_summary = summarizer(parser.document, SENTECES_COUNT)
                for sentence in lex_summary:
                    self.answer_text_frame.append(str(sentence))
        else:
            self.answer_text_frame.append("You don't write a text in first frame or don't download a file")

    # def download_file_button_click(self):
    #     return
    #
    #
    # def answer_download_button_click(self):
    #     if self.answer_text_frame.toPlainText():
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*);;Text Files (*.txt)", options=options)
    #         if file_name:
    #             self.selected_file_path = file_name
    #     else:
    #         self.answer_text_frame.append("You don't have anything to save")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
