from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import re


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.data = None

        # label
        styleLabel = QLabel("File:")

        # file path text
        self.qline_filename = QLineEdit()

        # browse button @TODO: find path to browse file
        fileButton = QPushButton("Browser")
        fileButton.clicked.connect(self.browse_path_button_click)

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(self.qline_filename)
        topLayout.addWidget(fileButton)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 15)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 5)
        self.setLayout(mainLayout)

        self.setWindowTitle("Tìm Kiếm Thông Tin")

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")
        nhapLabel = QLabel("Nhập K: ")

        self.k_gram_text = QLineEdit()

        # button
        xongButton = QPushButton("Xong")
        xongButton.clicked.connect(self.k_gram_button_click)

        layout = QVBoxLayout()
        layout.addWidget(nhapLabel)
        layout.addWidget(self.k_gram_text)
        layout.addWidget(xongButton)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Kết Quả")
        self.text2 = QTextEdit()
        layout = QVBoxLayout()

        layout.addWidget(self.text2, 12)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def browse_path_button_click(self):
        '''
        Read the input txt file to self.data
        :return:
        '''

        try:
            file_path = self.qline_filename.text()  # get current file name in qline box
            with open(file_path, 'r', encoding="utf-8") as f:
                self.data = f.read()
        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Không mở được file')
            error_dialog.exec_()

    def k_gram_button_click(self):
        '''
        Get input k-gram at k-gram box and find in self.data
        Show result at right box
        '''

        try:
            k_gram = self.k_gram_text.text()
            regex = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ"]+\b'
            paragraphs = self.data.split("\n\n")
            for paragraph_index, paragraph in enumerate(paragraphs):
                for line_index, line in enumerate(paragraph.split('\n')):
                    res = ""

                    for c in (re.findall(regex, line)):
                        res += c
                    n = len(k_gram)
                    grams = [res[i:i + n] for i in range(len(res) - n + 1)]
                    if k_gram in grams:
                        # print result to box @TODO: find word location
                        self.text2.insertPlainText(
                            "Found {} in paragraph: {}, line : {}, position ??:, \" {} \"\n".format(grams.count(k_gram),
                                                                                                    paragraph_index + 1,
                                                                                                    line_index + 1,
                                                                                                    line.strip()))

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Lỗi k-gram')
            error_dialog.exec_()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.showMaximized()  # set this to prevent small window
    sys.exit(app.exec_())
