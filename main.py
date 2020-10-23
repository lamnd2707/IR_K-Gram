from PyQt5.QtWidgets import *
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
        if self.qline_filename.text().endswith('.txt'):
            with open(self.qline_filename.text(), 'r', encoding='utf-8') as file:
                self.data = file.read()
                self.text2.setText(self.data)
        else:
            self.vnexpress_crawler(self.qline_filename.text())
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
            k_gram = self.k_gram_text.text()
            regex = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ"]+\b'
            paragraphs = self.data.split("\n\n")

            self.text2.clear()
            total = 0
            for paragraph_index, paragraph in enumerate(paragraphs):
                for line_index, line in enumerate(paragraph.split('\n')):
                    res = ""
                    origin_line = line
                    for stop_word in self.stop_words:
                        line = line.replace(' ' + stop_word + ' ', ' ')
                    for c in (re.findall(regex, line)):
                        res += c
                    n = len(k_gram)
                    grams = [res[i:i + n] for i in range(len(res) - n + 1)]
                    if k_gram in grams:
                        total += grams.count(k_gram)
                        # print result to box @TODO: find word location
                        temp = ''
                        pos = 0
                        result_pos = []
                        for char in origin_line:
                            pos += 1
                            if char in ',.:;/][{}!@#$%^&*()-=+_\'\" ':
                                continue

                            if not temp:
                                if char == k_gram:
                                    result_pos.append(str(pos - len(k_gram) + 1))
                                    temp = ''
                                if char == k_gram[0]:
                                    temp += char
                                else:
                                    temp = ''
                                continue
                            temp += char

                            if temp == k_gram:
                                result_pos.append(str(pos - len(k_gram) + 1))
                                temp = ''

                            if temp not in k_gram:
                                temp = ''
                                continue

                        self.text2.insertPlainText(
                            "Tìm thấy {} trong đoạn thứ: {}, dòng thứ : {}, tại các vị trí {}:, \" {} \"\n".format(
                                grams.count(k_gram),
                                paragraph_index + 1,
                                line_index + 1,
                                ' '.join(result_pos),
                                origin_line.strip()))
            self.text2.insertPlainText("\nTìm thấy tổng cộng {} trong file".format(total))

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
