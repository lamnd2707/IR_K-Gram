from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import re
import subprocess


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.data = None

        # label
        styleLabel = QLabel("Nhập tên file hoặc vn express url:")

        # file path text
        self.qline_filename = QLineEdit(self)
        self.qline_filename.setFixedWidth(1000)

        # browse button
        fileButton = QPushButton("Browse")
        fileButton2 = QPushButton("Xong")
        fileButton.clicked.connect(self.browse_path_button_click)
        fileButton2.clicked.connect(self.set_output_text)

        # stop word
        with open('vietnamese-stopwords.txt', 'r', encoding='utf-8') as f:
            self.stop_words = []
            for word in f.readlines():
                self.stop_words.append(word.strip('\n'))

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(self.qline_filename)
        topLayout.addWidget(fileButton)
        topLayout.addWidget(fileButton2)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 15)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 20)
        self.setLayout(mainLayout)

        self.setWindowTitle("Tìm Kiếm Thông Tin")
        self.setWindowIcon(QIcon("icon.ico"))

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")
        nhapLabel = QLabel("Nhập K: ")
        self.k_gram_text = QLineEdit()

        # button
        xongButton = QPushButton("Xong")
        xongButton.clicked.connect(self.k_gram_button_click)

        # nhapLabel1 = QLabel("Nhập chữ: ")
        # self.gram_text = QLineEdit()
        #
        # xongButton1 = QPushButton("Xong")
        # xongButton.clicked.connect(self.k_gram_button_click)

        layout = QVBoxLayout()
        layout.addWidget(nhapLabel)
        layout.addWidget(self.k_gram_text)
        layout.addWidget(xongButton)

        # layout.addWidget(nhapLabel1)
        # layout.addWidget(self.gram_text)
        # layout.addWidget(xongButton1)

        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Kết Quả")
        self.text2 = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Văn bản gốc: "))
        layout.addWidget(self.text2, 12)
        layout.addStretch(1)

        self.text3 = QTextEdit()
        layout.addWidget(QLabel("Văn bản lược bỏ từ dừng: "))
        layout.addWidget(self.text3, 12)
        layout.addStretch(2)

        self.text4 = QTextEdit()
        layout.addWidget(QLabel("K-gram được tách ra: "))
        layout.addWidget(self.text4, 12)
        layout.addStretch(3)

        self.topRightGroupBox.setLayout(layout)

    def browse_path_button_click(self):
        try:
            fname = str(QFileDialog.getOpenFileName(self, 'Open file',
                                                    '', "Text files (*.txt)"))
            fname = fname.split("'")[1]
            self.qline_filename.setText(str(fname))
        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Không mở được file')
            error_dialog.exec_()

    def set_output_text(self):
        import time
        if self.qline_filename.text().endswith('.txt'):
            with open(self.qline_filename.text(), 'r', encoding='utf-8') as file:
                self.data = file.read()
                self.text2.setText(self.data)
        else:
            self.vnexpress_crawler(self.qline_filename.text())
            time.sleep(5)
            self.data = open('output.txt', 'r', encoding='utf-8').read()
            self.text2.setText(self.data)

    @staticmethod
    def vnexpress_crawler(url):
        subprocess.Popen(["scrapy", "crawl", "crawler", "-a", "start_url={}".format(url)], shell=True)

    def k_gram_button_click(self):
        '''
        Get input k-gram at k-gram box and find in self.data
        Show result at right box
        '''

        try:
            k_gram = int(self.k_gram_text.text())
            regex = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ"]+\b'
            paragraphs = self.data.split("\n\n")

            self.text2.clear()
            total_gram = dict()
            if os.path.exists('result.txt'):
                os.remove('result.txt')
            if os.path.exists('stop_word_stripped.txt'):
                os.remove('stop_word_stripped.txt')

            for paragraph_index, paragraph in enumerate(paragraphs):
                for line_index, line in enumerate(paragraph.split('\n')):
                    res = ""
                    for stop_word in self.stop_words:
                        line = line.replace(' ' + stop_word + ' ', ' ')
                    # stop word
                    with open('stop_word_stripped.txt', 'a', encoding='utf-8') as f:
                        f.write(''.join(line) + '\n')
                    for c in (re.findall(regex, line)):
                        res += c
                    grams = [res[i:i + k_gram] for i in range(len(res) - k_gram + 1)]
                    for gram in grams:
                        if total_gram.get(gram) is not None:
                            total_gram[gram] = total_gram.get(gram) + 1
                        else:
                            total_gram[gram] = 1

            with open('result.txt', 'a', encoding='utf-8') as f:
                for i in sorted(total_gram.keys(), key=str.casefold):
                    f.write(i + ' - Tần suất: ' + str(total_gram.get(i)) + '\n')

            with open('sample.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    self.text2.insertPlainText(''.join(line) + '\n')

            with open('stop_word_stripped.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    self.text3.insertPlainText(''.join(line) + '\n')

            with open('result.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    self.text4.insertPlainText(''.join(line))
        except Exception as e:
            print(e)
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Lỗi khi tìm k-gram')
            error_dialog.exec_()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.showMaximized()  # set this to prevent small window
    sys.exit(app.exec_())
