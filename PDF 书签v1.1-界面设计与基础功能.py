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
        """根据提供的目录数据添加书签到 PDF。"""
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


class MainWindow(QMainWindow):
    """主界面类：选择 PDF 文件和目录输入模式。"""
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Bookmark Editor")
        self.setGeometry(100, 100, 400, 200)

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

        # 目录输入方式
        self.radio_auto = QRadioButton("自动识别目录", self)
        self.radio_auto.setChecked(True)
        self.radio_manual = QRadioButton("手动输入目录", self)
        layout.addWidget(self.radio_auto)
        layout.addWidget(self.radio_manual)

        # 下一步按钮，打开目录配置界面
        self.next_button = QPushButton("下一步", self)
        self.next_button.clicked.connect(self.open_config_window)
        layout.addWidget(self.next_button)

    def select_file(self):
        """处理文件选择事件。"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        if file_path:
            self.file_input.setText(file_path)

    def open_config_window(self):
        """打开目录配置界面。"""
        input_pdf_path = self.file_input.text()
        if not input_pdf_path:
            QMessageBox.critical(self, "错误", "请选择 PDF 文件")
            return

        mode = 'auto' if self.radio_auto.isChecked() else 'manual'
        self.config_window = ConfigWindow(input_pdf_path, mode)
        self.config_window.show()


class ConfigWindow(QMainWindow):
    """目录配置界面类：提供目录页码范围输入或手动书签编辑。"""
    
    def __init__(self, input_pdf_path, mode):
        super().__init__()

        self.setWindowTitle("PDF Bookmark Configuration")
        self.setGeometry(100, 100, 600, 500)

        self.input_pdf_path = input_pdf_path
        self.mode = mode
        self.handler = PdfBookmarkHandler()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 页码范围输入（自动识别模式）
        self.page_input = QLineEdit(self)
        if self.mode == 'auto':
            self.page_label = QLabel("输入目录页码或范围（如 4-15）：", self)
            layout.addWidget(self.page_label)
            self.page_input.setPlaceholderText("1 或 4-15")
            layout.addWidget(self.page_input)
        else:
            # 手动输入文本框
            self.manual_input = QTextEdit(self)
            self.manual_input.setPlaceholderText("手动输入目录格式：标题 页码\n章节一 1\n章节二 10")
            layout.addWidget(self.manual_input)

        # 处理按钮
        self.process_button = QPushButton("添加书签", self)
        self.process_button.clicked.connect(self.process_pdf)
        layout.addWidget(self.process_button)

    def process_pdf(self):
        """处理 PDF 文件并添加书签。"""
        output_pdf_path = self.input_pdf_path.replace('.pdf', '_with_bookmarks.pdf')

        if self.mode == 'auto':
            toc_range = self.page_input.text()
            if not toc_range or not (toc_range.isdigit() or '-' in toc_range):
                QMessageBox.critical(self, "错误", "请输入有效的页码或范围，例如：4 或 4-15")
                return
            toc_data = self.handler.auto_extract_toc(self.input_pdf_path, toc_range)
        else:
            toc_data = self.handler.manual_extract_toc(self.manual_input.toPlainText())
            if not toc_data:
                QMessageBox.critical(self, "错误", "请输入有效的目录格式")
                return

        try:
            message = self.handler.add_bookmarks_to_pdf(self.input_pdf_path, output_pdf_path, toc_data)
            QMessageBox.information(self, "成功", message)
        except RuntimeError as error:
            QMessageBox.critical(self, "错误", str(error))


# 启动应用程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
