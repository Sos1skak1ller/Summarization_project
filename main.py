from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QVBoxLayout, QComboBox, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon
import sys

import sumy_algorithm

import nltk
nltk.download('punkt')

LANGUAGE = "russian"
SENTENCES_COUNT = 1

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
        self.setWindowIcon(QIcon('path/to/icon.png'))  # Укажите правильный путь к иконке

        self.download_file_button = QPushButton('Upload file', self)
        self.download_file_button.clicked.connect(self.download_file_button_click)

        self.list_refering_methods = QComboBox(self)
        self.list_refering_methods.addItems(["lsa", "luhn", "lexrank"])

        self.start_button = QPushButton('Generate', self)
        self.start_button.clicked.connect(self.start_button_click)

        self.answer_download_button = QPushButton('Save answer', self)
        self.answer_download_button.clicked.connect(self.answer_download_button_click)

        self.request_text_frame = PlaceholderTextEdit('Insert your text here', self)
        self.answer_text_frame = PlaceholderTextEdit('Here will be your short version of text', self)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        button_list_layout = QHBoxLayout()
        button_list_layout.addWidget(self.download_file_button)
        button_list_layout.addSpacing(240)
        button_list_layout.addWidget(self.list_refering_methods)
        button_list_layout.addWidget(self.start_button)

        answer_button_layout = QHBoxLayout()
        answer_button_layout.addSpacing(600)
        answer_button_layout.addWidget(self.answer_download_button)

        main_layout.addWidget(self.request_text_frame)
        main_layout.addLayout(button_list_layout)
        main_layout.addWidget(self.answer_text_frame)
        main_layout.addLayout(answer_button_layout)
        self.show()

    def start_button_click(self):
        self.answer_text_frame.clear()
        input_text = self.request_text_frame.toPlainText()
        if input_text:
            selected_variant_of_refering_methods = self.list_refering_methods.currentText()
            num_sentences = SENTENCES_COUNT
            summary = sumy_algorithm.summarize_text(input_text, num_sentences, selected_variant_of_refering_methods)
            if summary:  # Проверка на наличие результата
                for sentence in summary:
                    self.answer_text_frame.append(str(sentence))
            else:
                self.answer_text_frame.append("Error in summarizing the text.")
        else:
            self.answer_text_frame.append("You don't write a text in first frame or don't download a file")

    def download_file_button_click(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            try:
                with open(fileName, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.request_text_frame.clear()
                    self.request_text_frame.setText(text)

            except Exception as e:
                self.answer_text_frame.clear()
                self.answer_text_frame.append("Error loading file: " + str(e))

    def answer_download_button_click(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            try:
                text = self.answer_text_frame.toPlainText()
                with open(fileName, 'w', encoding='utf-8') as file:  # Укажите кодировку utf-8
                    file.write(text)
            except Exception as e:
                self.answer_text_frame.clear()
                self.answer_text_frame.setText("Error saving file: " + str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
