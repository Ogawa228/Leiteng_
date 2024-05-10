import sys
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
from pdf2image import convert_from_path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QRadioButton, QTextEdit
)
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
from PyQt5.QtWidgets import QInputDialog
import re

import sys
import re
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
from pdf2image import convert_from_path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QRadioButton, QTextEdit
)
from PyQt5.QtCore import Qt

# 设置 pytesseract 的路径（如果需要）
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class PdfBookmarkHandler:
    """负责处理 PDF 并添加书签的功能类。"""

    @staticmethod
    def preprocess_image(image):
        """对图像进行预处理：灰度化、二值化和去噪。"""
        image = image.convert('L')  # 转换为灰度图
        image = image.filter(ImageFilter.MedianFilter())  # 中值滤波去噪
        threshold = 200
        image = image.point(lambda p: p > threshold and 255)  # 二值化
        return image

    @staticmethod
    def auto_extract_toc(input_pdf_path, toc_range):
        """自动从指定的页面范围提取目录。"""
        try:
            start_page, end_page = map(int, toc_range.split('-'))
        except ValueError:
            start_page = end_page = int(toc_range)

        # 提高分辨率以获得更清晰的图像
        images = convert_from_path(input_pdf_path, first_page=start_page, last_page=end_page, dpi=300)

        toc_text = ""
        custom_oem_psm_config = r'--oem 3 --psm 6'  # 使用 LSTM 引擎并假设固定布局
        for image in images:
            processed_image = PdfBookmarkHandler.preprocess_image(image)
            toc_text += pytesseract.image_to_string(processed_image, config=custom_oem_psm_config, lang='eng')

        # 分析 OCR 结果，提取章节标题和页码
        toc_data = []
        for line in toc_text.split('\n'):
            if line.strip():
                parts = line.rsplit(' ', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    toc_data.append((parts[0].strip(), int(parts[1])))

        return toc_data

    @staticmethod
    def manual_extract_toc(toc_text):
        """解析用户手动输入的目录文本。"""
        toc_data = []
        for line in toc_text.split('\n'):
            parts = line.strip().split()
            if len(parts) >= 2 and parts[-1].isdigit():
                title = " ".join(parts[:-1])
                page_num = int(parts[-1])
                toc_data.append((title, page_num))
        return toc_data

    @staticmethod
    def add_bookmarks_to_pdf(input_pdf_path, output_pdf_path, toc_data):
        """
        根据提供的目录数据添加书签到 PDF。

        参数:
            input_pdf_path: 输入的 PDF 文件路径
            output_pdf_path: 输出的 PDF 文件路径
            toc_data: 目录数据，包括标题和页码
        """
        try:
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            for title, page_num in toc_data:
                writer.add_outline_item(title, page_num - 1)

            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)

            return "书签添加完成！"
        except Exception as e:
            raise RuntimeError(f"处理 PDF 时出错：{str(e)}")

class PdfBookmarkApp(QMainWindow):
    """提供图形用户界面以与用户交互的应用程序类。"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Bookmark Adder")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 文件选择
        self.file_label = QLabel("选择 PDF 文件：", self)
        layout.addWidget(self.file_label)
        self.file_input = QLineEdit(self)
        layout.addWidget(self.file_input)
        self.select_button = QPushButton("选择文件", self)
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        # 正则表达式输入
        regex_label = QLabel("输入正则表达式：", self)
        layout.addWidget(regex_label)
        self.regex_input = QLineEdit(self)
        self.regex_input.setPlaceholderText(r"第 (\d+) 条[\s\S]*?【(.*?)】[\s\S]*?(\d+)\n")
        layout.addWidget(self.regex_input)

        # 正文起始页输入
        start_page_label = QLabel("输入正文起始页：", self)
        layout.addWidget(start_page_label)
        self.start_page_input = QLineEdit(self)
        self.start_page_input.setPlaceholderText("1")
        layout.addWidget(self.start_page_input)

        # 目录输入方式
        self.radio_auto = QRadioButton("自动识别目录", self)
        self.radio_auto.setChecked(True)
        self.radio_manual = QRadioButton("手动输入目录", self)
        layout.addWidget(self.radio_auto)
        layout.addWidget(self.radio_manual)

        # 页码范围输入
        self.page_label = QLabel("输入目录页码或范围（如 4-15）：", self)
        layout.addWidget(self.page_label)
        self.page_input = QLineEdit(self)
        self.page_input.setPlaceholderText("1 或 4-15")
        layout.addWidget(self.page_input)

        # 手动输入文本框
        self.manual_input = QTextEdit(self)
        self.manual_input.setPlaceholderText("手动输入目录格式：标题 页码\n章节一 1\n章节二 10")
        self.manual_input.setContextMenuPolicy(Qt.CustomContextMenu)
        self.manual_input.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.manual_input)
        self.manual_input.setHidden(True)

        # 处理按钮
        self.process_button = QPushButton("添加书签", self)
        self.process_button.clicked.connect(self.process_pdf)
        layout.addWidget(self.process_button)

        self.radio_auto.toggled.connect(self.toggle_input_mode)
        self.radio_manual.toggled.connect(self.toggle_input_mode)

    def toggle_input_mode(self):
        """切换目录输入模式：自动或手动。"""
        if self.radio_auto.isChecked():
            self.page_input.setHidden(False)
            self.manual_input.setHidden(True)
        else:
            self.page_input.setHidden(True)
            self.manual_input.setHidden(False)

    def select_file(self):
        """处理文件选择事件。"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        if file_path:
            self.file_input.setText(file_path)

    def process_pdf(self):
        """处理 PDF 文件，并添加书签。"""
        input_pdf_path = self.file_input.text()
        output_pdf_path = input_pdf_path.replace('.pdf', '_with_bookmarks.pdf')

        if not input_pdf_path:
            QMessageBox.critical(self, "错误", "请选择 PDF 文件")
            return

        if self.radio_auto.isChecked():
            toc_range = self.page_input.text()
            if not toc_range or not (toc_range.isdigit() or '-' in toc_range):
                QMessageBox.critical(self, "错误", "请输入有效的页码或范围，例如：4 或 4-15")
                return
            toc_data = self.auto_extract_toc(input_pdf_path, toc_range)
        else:
            toc_data = self.manual_extract_toc(self.manual_input.toPlainText())
            if not toc_data:
                QMessageBox.critical(self, "错误", "请输入有效的目录格式")
                return

        try:
            message = self.add_bookmarks_to_pdf(input_pdf_path, output_pdf_path, toc_data)
            QMessageBox.information(self, "成功", message)
        except RuntimeError as error:
            QMessageBox.critical(self, "错误", str(error))

    def auto_extract_toc(self, input_pdf_path, toc_range):
        """自动从指定的页面范围提取目录。"""
        start_page, end_page = map(int, toc_range.split('-'))
        images = convert_from_path(input_pdf_path, first_page=start_page, last_page=end_page, dpi=300)

        toc_text = ""
        for image in images:
            toc_text += pytesseract.image_to_string(image)

        toc_data = []
        for line in toc_text.split('\n'):
            if line.strip():
                parts = line.rsplit(' ', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    toc_data.append((parts[0].strip(), int(parts[1])))
        return toc_data

    def manual_extract_toc(self, toc_text):
        """解析用户手动输入的目录文本。"""
        toc_data = []
        for line in toc_text.split('\n'):
            parts = line.strip().split()
            if len(parts) >= 2 and parts[-1].isdigit():
                title = " ".join(parts[:-1])
                page_num = int(parts[-1])
                toc_data.append((title, page_num))
        return toc_data

    def show_context_menu(self, point):
        """在文本框中显示自定义右键菜单，包括查找、替换和格式化文档功能。"""
        context_menu = self.manual_input.createStandardContextMenu()
        context_menu.addSeparator()

        # 查找和替换
        find_action = context_menu.addAction("查找和替换")
        find_action.triggered.connect(self.find_and_replace)

        # 格式化文档
        format_action = context_menu.addAction("格式化文档")
        format_action.triggered.connect(self.format_document)

        context_menu.exec_(self.manual_input.mapToGlobal(point))

    def find_and_replace(self):
        """在同一界面中查找和替换文本。"""
        find_replace_dialog = QWidget(self, Qt.Window)
        find_replace_dialog.setWindowTitle("查找和替换")
        find_replace_dialog.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout(find_replace_dialog)

        # 查找标签和输入框
        find_label = QLabel("查找：", find_replace_dialog)
        layout.addWidget(find_label)
        self.find_input = QLineEdit(find_replace_dialog)
        layout.addWidget(self.find_input)

        # 替换标签和输入框
        replace_label = QLabel("替换为：", find_replace_dialog)
        layout.addWidget(replace_label)
        self.replace_input = QLineEdit(find_replace_dialog)
        layout.addWidget(self.replace_input)

        # 查找并替换按钮
        replace_button = QPushButton("查找并替换", find_replace_dialog)
        replace_button.clicked.connect(self.execute_find_and_replace)
        layout.addWidget(replace_button)

        find_replace_dialog.show()

    def execute_find_and_replace(self):
        """执行查找并替换的操作逻辑。"""
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()

        if find_text:
            cursor = self.manual_input.textCursor()
            cursor.beginEditBlock()
            doc = self.manual_input.document()
            cursor = doc.find(find_text, cursor)
            while not cursor.isNull():
                cursor.insertText(replace_text)
                cursor = doc.find(find_text, cursor)
            cursor.endEditBlock()

    def format_document(self):
        """使用用户定义的正则表达式格式化文档内容。"""
        regex = self.regex_input.text()
        pattern = re.compile(regex)
        text = self.manual_input.toPlainText()
        formatted_lines = []
        for line in text.splitlines():
            match = pattern.match(line)
            if match:
                title = match.group(2)
                page_num = int(match.group(3)) + int(self.start_page_input.text()) - 1
                formatted_lines.append(f"{title} {page_num}")
        self.manual_input.setPlainText("\n".join(formatted_lines))

# 启动应用程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PdfBookmarkApp()
    window.show()
    sys.exit(app.exec_())
