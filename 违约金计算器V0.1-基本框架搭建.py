import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QRadioButton, QButtonGroup, QDateEdit, QComboBox, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 违约金计算模块
def calculate_penalty_with_method(amount, lpr_data, start_date, end_date, days_base, method):
    days = (end_date - start_date).days

    if method == "分段LPR计算":
        # 分段LPR计算（示例为简单处理，你可以根据需要进一步调整）
        rate = float(lpr_data.get("一年期LPR", 0)) / 100
        penalty = amount * rate * (days / days_base)

    elif method == "平均LPR":
        # 平均LPR计算
        rate = (float(lpr_data.get("一年期LPR", 0)) + float(lpr_data.get("五年期LPR", 0))) / 200
        penalty = amount * rate * (days / days_base)

    elif method == "截止月LPR":
        # 截止月LPR计算
        rate = float(lpr_data.get("一年期LPR", 0)) / 100
        penalty = amount * rate * (days / days_base)

    elif method == "起始月LPR":
        # 起始月LPR计算
        rate = float(lpr_data.get("五年期LPR", 0)) / 100
        penalty = amount * rate * (days / days_base)

    elif method == "法定最高LPR":
        # 法定最高LPR（LPR的4倍）
        rate = 4 * (float(lpr_data.get("一年期LPR", 0)) / 100)
        penalty = amount * rate * (days / days_base)

    else:
        penalty = 0  # 未知方式，返回0
    
    return round(penalty, 2)

# 保存和读取LPR利率
def load_lpr_config():
    try:
        with open('lpr_config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # 如果文件不存在，返回空字典

def save_lpr_config(lpr_data):
    with open('lpr_config.json', 'w') as file:
        json.dump(lpr_data, file, ensure_ascii=False, indent=4)

# 爬虫模块 - 爬取最新的LPR数据并保存到配置文件
def fetch_latest_lpr():
    url = "https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lpr_data = {}
    table = soup.find('table')
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        period = cells[0].text.strip()
        rate = cells[1].text.strip()
        lpr_data[period] = rate
    
    save_lpr_config(lpr_data)  # 保存到配置文件
    return lpr_data

# 文件生成模块
def save_to_excel(data, file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"数据已保存到 {file_name}")

def save_to_markdown(data, file_name):
    df = pd.DataFrame(data)
    with open(file_name, 'w') as f:
        f.write(df.to_markdown())
    print(f"数据已保存到 {file_name}")

# 主程序UI模块
class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.lpr_data = load_lpr_config()  # 加载LPR利率配置

    def init_ui(self):
        # 设置窗口的基本属性
        self.setWindowTitle('违约金计算器')
        self.setGeometry(100, 100, 800, 600)
        
        # 苹果风格字体
        font = QFont("Helvetica Neue", 12)

        # 创建主布局
        layout = QVBoxLayout()

        # 创建违约金额输入框
        self.amount_label = QLabel('违约金额 (元):')
        self.amount_input = QLineEdit()
        self.amount_input.setFont(font)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        # 创建起止日期选择器
        self.start_date_label = QLabel('开始日期:')
        self.start_date_input = QDateEdit()
        self.start_date_input.setFont(font)
        self.start_date_input.setDate(QDate.currentDate())
        
        self.end_date_label = QLabel('结束日期:')
        self.end_date_input = QDateEdit()
        self.end_date_input.setFont(font)
        self.end_date_input.setDate(QDate.currentDate())

        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)

        # 选择LPR利率模式
        self.lpr_label = QLabel('选择LPR利率:')
        self.lpr_input = QComboBox()
        self.lpr_input.addItems(["一年期LPR", "五年期LPR"])
        self.lpr_input.setFont(font)
        layout.addWidget(self.lpr_label)
        layout.addWidget(self.lpr_input)

        # 自然年天数基准选择
        self.days_base_label = QLabel('选择自然年天数基准:')
        self.days_base_input = QComboBox()
        self.days_base_input.addItems(["360天", "365天"])
        self.days_base_input.setFont(font)
        layout.addWidget(self.days_base_label)
        layout.addWidget(self.days_base_input)

        # 增加计息方式选择
        self.method_label = QLabel('选择计息方式:')
        self.method_group = QButtonGroup(self)
        
        self.segmented_lpr_radio = QRadioButton("分段LPR计算")
        self.average_lpr_radio = QRadioButton("平均LPR")
        self.end_lpr_radio = QRadioButton("截止月LPR")
        self.start_lpr_radio = QRadioButton("起始月LPR")
        self.legal_lpr_radio = QRadioButton("法定最高LPR")
        
        self.method_group.addButton(self.segmented_lpr_radio)
        self.method_group.addButton(self.average_lpr_radio)
        self.method_group.addButton(self.end_lpr_radio)
        self.method_group.addButton(self.start_lpr_radio)
        self.method_group.addButton(self.legal_lpr_radio)
        
        layout.addWidget(self.method_label)
        layout.addWidget(self.segmented_lpr_radio)
        layout.addWidget(self.average_lpr_radio)
        layout.addWidget(self.end_lpr_radio)
        layout.addWidget(self.start_lpr_radio)
        layout.addWidget(self.legal_lpr_radio)

        # 计算违约金按钮
        self.calculate_btn = QPushButton('计算违约金')
        self.calculate_btn.setFont(font)
        self.calculate_btn.clicked.connect(self.calculate_penalty_handler)
        layout.addWidget(self.calculate_btn)

        # 违约金显示框
        self.result_display = QTextEdit()
        self.result_display.setFont(font)
        layout.addWidget(self.result_display)

        # 更新LPR按钮
        self.update_lpr_btn = QPushButton('更新LPR利率')
        self.update_lpr_btn.setFont(font)
        self.update_lpr_btn.clicked.connect(self.update_lpr_handler)
        layout.addWidget(self.update_lpr_btn)

        # 保存文件按钮
        self.save_file_btn = QPushButton('保存结果为文件')
        self.save_file_btn.setFont(font)
        self.save_file_btn.clicked.connect(self.save_file_handler)
        layout.addWidget(self.save_file_btn)

        self.setLayout(layout)

    def calculate_penalty_handler(self):
        # 获取用户输入
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.result_display.setText("请输入有效的违约金额。")
            return

        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()

        # 获取用户选择的计息方式
        selected_method = None
        if self.segmented_lpr_radio.isChecked():
            selected_method = "分段LPR计算"
        elif self.average_lpr_radio.isChecked():
            selected_method = "平均LPR"
        elif self.end_lpr_radio.isChecked():
            selected_method = "截止月LPR"
        elif self.start_lpr_radio.isChecked():
            selected_method = "起始月LPR"
        elif self.legal_lpr_radio.isChecked():
            selected_method = "法定最高LPR"

        # 天数基准
        days_base = 365 if self.days_base_input.currentText() == "365天" else 360

        # 根据计息方式计算违约金
        penalty = calculate_penalty_with_method(amount, self.lpr_data, start_date, end_date, days_base, selected_method)
        result_text = f"违约金额: {amount} 元\n利率方式: {selected_method}\n起始日期: {start_date}\n结束日期: {end_date}\n违约金: {penalty} 元"
        self.result_display.setText(result_text)

    def update_lpr_handler(self):
        self.lpr_data = fetch_latest_lpr()
        self.result_display.setText("LPR利率已更新:\n" + str(self.lpr_data))

    def save_file_handler(self):
        # 获取保存文件的路径
        file_dialog = QFileDialog(self)
        file_name, _ = file_dialog.getSaveFileName(self, "保存文件", "", "Excel 文件 (*.xlsx);;Markdown 文件 (*.md)")
        
        if file_name:
            # 获取当前显示的结果
            result_text = self.result_display.toPlainText()
            data = [result_text.split('\n')]
            
            if file_name.endswith('.xlsx'):
                save_to_excel(data, file_name)
            elif file_name.endswith('.md'):
                save_to_markdown(data, file_name)

# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec_())
