import sys
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QRadioButton, QButtonGroup, QDateEdit, QComboBox, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox
import logging
import ntplib
from time import ctime

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 获取指定日期最近的LPR
def get_lpr_for_date(lpr_data, date, lpr_type):
    lpr_date_keys = [datetime.strptime(key, "%Y-%m-%d").date() for key in lpr_data.keys()]
    # 找到不晚于指定日期的最近一次LPR发布日期
    past_dates = [d for d in lpr_date_keys if d <= date]
    if not past_dates:
        closest_date = min(lpr_date_keys)
    else:
        closest_date = max(past_dates)
    lpr_value = lpr_data[closest_date.strftime("%Y-%m-%d")][lpr_type]

    # 如果是字符串，去掉百分号并转换为浮点数
    if isinstance(lpr_value, str):
        lpr_value = float(lpr_value.replace('%', '')) / 100

    return lpr_value, closest_date

# 获取当前时间
def get_current_time():
    try:
        client = ntplib.NTPClient()
        logging.debug("正在从 NTP 服务器获取时间...")
        response = client.request('time1.aliyun.com', version=3)  # 使用 NTP 服务器获取时间
        current_time = ctime(response.tx_time)  # 将时间转换为可读格式
        logging.debug(f"成功获取时间: {current_time}")
        return current_time
    except Exception as e:
        logging.error(f"NTP 请求失败: {e}")
        return f"无法获取当前时间，错误: {str(e)}"

# 获取最近的LPR
def get_closest_lpr(lpr_data, target_date):
    # 将 LPR 数据的日期转换为 datetime 格式
    lpr_dates = [datetime.strptime(key, '%Y-%m-%d').date() for key in lpr_data.keys()]
    
    # 找到不晚于指定日期的最近一次LPR发布日期
    past_dates = [d for d in lpr_dates if d <= target_date]
    if not past_dates:
        closest_date = min(lpr_dates)
    else:
        closest_date = max(past_dates)
    
    # 获取最近日期对应的 LPR 值（包含一年期和五年期）
    closest_lpr_data = lpr_data[closest_date.strftime('%Y-%m-%d')]
    
    # 确保返回两个值：一年期和五年期LPR
    if isinstance(closest_lpr_data, dict):
        one_year_lpr = closest_lpr_data.get("一年期")
        five_year_lpr = closest_lpr_data.get("五年期")
        logging.debug(f"找到最近的LPR: 日期: {closest_date}, 一年期: {one_year_lpr}, 五年期: {five_year_lpr}")
        return one_year_lpr, five_year_lpr, closest_date
    else:
        raise ValueError(f"LPR 数据格式不正确: {closest_lpr_data}")

# 计算指定日期范围内的平均LPR
def calculate_average_lpr(lpr_data, start_date, end_date, lpr_type):
    lpr_dates = [datetime.strptime(key, '%Y-%m-%d').date() for key in lpr_data.keys()]
    # 获取指定日期范围内的所有LPR发布日期
    relevant_dates = [d for d in lpr_dates if start_date <= d <= end_date]
    if not relevant_dates:
        raise ValueError("指定日期范围内没有LPR数据。")
    lpr_values = []
    for date in relevant_dates:
        lpr_value = lpr_data[date.strftime('%Y-%m-%d')][lpr_type]
        if isinstance(lpr_value, str):
            lpr_value = float(lpr_value.replace('%', '')) / 100
        lpr_values.append(lpr_value)
    average_lpr = sum(lpr_values) / len(lpr_values)
    logging.debug(f"计算平均LPR: {average_lpr}, 期间: {start_date} 至 {end_date}")
    return average_lpr

# 违约金计算模块
def calculate_penalty(amount, start_date, end_date, days_base, method, lpr_data, day_calculation, lpr_type):
    days_total = (end_date - start_date).days
    if day_calculation == "算头不算尾":
        days_total -= 1
    elif day_calculation == "两头都算":
        days_total += 1

    logging.debug(f"计算违约金，方法: {method}")

    # 根据不同计息方式计算违约金
    calculation_process = ""
    if method == "分段LPR计算":
        total_penalty = 0
        current_date = start_date
        calculation_details = []
        while current_date < end_date:
            # 确定当前段的结束日期（每次到月底或结束日期）
            next_month = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
            period_end = min(end_date, next_month)
            days_in_period = (period_end - current_date).days

            # 获取当前期间的LPR
            lpr_value, lpr_date = get_lpr_for_date(lpr_data, current_date, lpr_type)
            penalty_segment = amount * (days_in_period / days_base) * lpr_value
            total_penalty += penalty_segment

            # 记录计算细节
            calculation_details.append(
                f"{current_date.strftime('%Y-%m-%d')} 至 {period_end.strftime('%Y-%m-%d')}, 天数: {days_in_period} 天, LPR发布日期: {lpr_date}, LPR利率: {lpr_value*100:.2f}%, 违约金: {penalty_segment:.2f} 元"
            )

            # 更新当前日期
            current_date = period_end

        penalty = total_penalty

        # 构建计算过程
        calculation_process = "<br>".join(calculation_details)
        calculation_process += f"<br><b>总违约金: {penalty:.2f} 元</b>"

    elif method == "平均LPR":
        # 计算平均LPR
        average_lpr = calculate_average_lpr(lpr_data, start_date, end_date, lpr_type)
        penalty = amount * (days_total / days_base) * average_lpr
        calculation_process = f"平均LPR利率: {average_lpr*100:.2f}%<br>违约金 = {amount} × ({days_total} / {days_base}) × {average_lpr*100:.2f}% = {penalty:.2f} 元"

    elif method == "截止月LPR":
        # 使用结束日期最近的LPR
        chosen_lpr, lpr_date = get_lpr_for_date(lpr_data, end_date, lpr_type)
        penalty = amount * (days_total / days_base) * chosen_lpr
        calculation_process = f"使用截止日期 {end_date} 最近的LPR（发布日期: {lpr_date}，利率: {chosen_lpr*100:.2f}%）<br>违约金 = {amount} × ({days_total} / {days_base}) × {chosen_lpr*100:.2f}% = {penalty:.2f} 元"

    elif method == "起始月LPR":
        # 使用开始日期最近的LPR
        chosen_lpr, lpr_date = get_lpr_for_date(lpr_data, start_date, lpr_type)
        penalty = amount * (days_total / days_base) * chosen_lpr
        calculation_process = f"使用起始日期 {start_date} 最近的LPR（发布日期: {lpr_date}，利率: {chosen_lpr*100:.2f}%）<br>违约金 = {amount} × ({days_total} / {days_base}) × {chosen_lpr*100:.2f}% = {penalty:.2f} 元"

    elif method == "法定最高LPR":
        # 使用结束日期最近的LPR的4倍
        chosen_lpr, lpr_date = get_lpr_for_date(lpr_data, end_date, lpr_type)
        chosen_lpr *= 4
        penalty = amount * (days_total / days_base) * chosen_lpr
        calculation_process = f"使用截止日期 {end_date} 最近的LPR的4倍（发布日期: {lpr_date}，利率: {chosen_lpr*100:.2f}%）<br>违约金 = {amount} × ({days_total} / {days_base}) × {chosen_lpr*100:.2f}% = {penalty:.2f} 元"

    else:
        raise ValueError("未知的计息方式。")

    return round(penalty, 2), calculation_process

# 保存和读取LPR利率
def load_lpr_config():
    config_file = 'lpr_config.json'  # 定义配置文件名
    try:
        with open(config_file, 'r') as file:
            lpr_data = json.load(file)
            logging.debug(f"LPR 数据已从 {config_file} 成功加载: {lpr_data}")
            return lpr_data
    except FileNotFoundError:
        logging.error(f"配置文件 {config_file} 未找到。")
        return {}
    except Exception as e:
        logging.error(f"读取 LPR 数据失败: {e}")
        return {}

def save_lpr_config(lpr_data):
    config_file = 'lpr_config.json'  # 定义配置文件名
    try:
        with open(config_file, 'w') as file:
            json.dump(lpr_data, file, ensure_ascii=False, indent=4)
        logging.debug(f"LPR 数据已成功保存到 {config_file}: {lpr_data}")
    except Exception as e:
        logging.error(f"保存 LPR 数据到 {config_file} 失败: {e}")

# 更新后的 fetch_latest_lpr 函数
def fetch_latest_lpr():
    url = "https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html"
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保正确解析中文编码
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lpr_data = {}
    table = soup.find('table')
    if not table:
        logging.error("未找到LPR数据表格。")
        return {}
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            date_str = cells[0].text.strip()
            one_year_lpr = cells[1].text.strip()
            five_year_lpr = cells[2].text.strip()

            # 尝试多种日期格式进行解析
            try:
                # 尝试解析格式如 "2023年09月20日"
                date_obj = datetime.strptime(date_str, "%Y年%m月%d日")
            except ValueError:
                try:
                    # 如果失败，尝试解析格式如 "2024-08-20"
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    logging.error(f"无法解析日期格式: {date_str}")
                    continue  # 跳过无法解析的日期

            formatted_date = date_obj.strftime("%Y-%m-%d")

            lpr_data[formatted_date] = {
                "一年期": one_year_lpr,
                "五年期": five_year_lpr
            }

    save_lpr_config(lpr_data)  # 保存到配置文件
    logging.debug(f"LPR 数据已成功抓取并保存: {lpr_data}")
    return lpr_data

# 保存数据到 Excel 文件
def save_to_excel(data, file_name):
    try:
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
        logging.debug(f"数据已成功保存到 Excel 文件: {file_name}")
    except Exception as e:
        logging.error(f"保存到 Excel 文件失败: {e}")

# 保存数据到 Markdown 文件
def save_to_markdown(data, file_name):
    try:
        df = pd.DataFrame(data)
        with open(file_name, 'w') as f:
            f.write(df.to_markdown(index=False))
        logging.debug(f"数据已成功保存到 Markdown 文件: {file_name}")
    except Exception as e:
        logging.error(f"保存到 Markdown 文件失败: {e}")

# 主程序UI模块
class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.lpr_data = load_lpr_config()

    def init_ui(self):
        self.setWindowTitle('违约金计算器----made by 江山j19972280991')
        self.setGeometry(100, 100, 800, 600)

        font = QFont("Helvetica Neue", 12)

        layout = QVBoxLayout()

        self.amount_label = QLabel('违约金额 (元):')
        self.amount_input = QLineEdit()
        self.amount_input.setFont(font)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        self.start_date_label = QLabel('开始日期:')
        self.start_date_input = QDateEdit()
        self.start_date_input.setFont(font)
        self.start_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)

        self.end_date_label = QLabel('结束日期:')
        self.end_date_input = QDateEdit()
        self.end_date_input.setFont(font)
        self.end_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)

        self.rate_type_label = QLabel('选择利率模式:')
        self.rate_type_input = QComboBox()
        self.rate_type_input.addItems(["万分之五", "LPR利率", "自定义利率"])
        self.rate_type_input.setFont(font)
        self.rate_type_input.currentIndexChanged.connect(self.toggle_rate_input)
        layout.addWidget(self.rate_type_label)
        layout.addWidget(self.rate_type_input)

        # 自定义利率输入框
        self.custom_rate_label = QLabel('自定义利率 (%):')
        self.custom_rate_input = QLineEdit()
        self.custom_rate_input.setFont(font)
        self.custom_rate_input.setVisible(False)  # 默认隐藏
        layout.addWidget(self.custom_rate_label)
        layout.addWidget(self.custom_rate_input)

        self.custom_rate_mode_label = QLabel('选择自定义利率模式:')
        self.custom_rate_mode_input = QComboBox()
        self.custom_rate_mode_input.addItems(["日利率", "月利率", "年利率"])
        self.custom_rate_mode_input.setFont(font)
        self.custom_rate_mode_input.setVisible(False)  # 默认隐藏
        layout.addWidget(self.custom_rate_mode_label)
        layout.addWidget(self.custom_rate_mode_input)

        self.lpr_label = QLabel('选择LPR利率:')
        self.lpr_input = QComboBox()
        self.lpr_input.addItems(["一年期LPR", "五年期LPR"])
        self.lpr_input.setFont(font)
        self.lpr_input.setVisible(False)
        layout.addWidget(self.lpr_label)
        layout.addWidget(self.lpr_input)

        self.days_base_label = QLabel('选择自然年天数基准:')
        self.days_base_input = QComboBox()
        self.days_base_input.addItems(["360天", "365天"])
        self.days_base_input.setFont(font)
        layout.addWidget(self.days_base_label)
        layout.addWidget(self.days_base_input)

        self.day_calculation_label = QLabel('选择天数算法:')
        self.day_calculation_input = QComboBox()
        self.day_calculation_input.addItems(["算头不算尾", "两头都算"])
        self.day_calculation_input.setFont(font)
        layout.addWidget(self.day_calculation_label)
        layout.addWidget(self.day_calculation_input)

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

        self.method_label.setVisible(False)
        self.segmented_lpr_radio.setVisible(False)
        self.average_lpr_radio.setVisible(False)
        self.end_lpr_radio.setVisible(False)
        self.start_lpr_radio.setVisible(False)
        self.legal_lpr_radio.setVisible(False)

        self.calculate_btn = QPushButton('计算违约金')
        self.calculate_btn.setFont(font)
        self.calculate_btn.clicked.connect(self.calculate_penalty_handler)
        layout.addWidget(self.calculate_btn)

        self.result_display = QTextEdit()
        self.result_display.setFont(font)
        layout.addWidget(self.result_display)

        # 更新LPR按钮
        self.update_lpr_btn = QPushButton('更新LPR利率')
        self.update_lpr_btn.setFont(font)
        self.update_lpr_btn.clicked.connect(self.update_lpr_handler)
        layout.addWidget(self.update_lpr_btn)

        # 查看当前LPR按钮
        self.view_lpr_btn = QPushButton('查看当前LPR')
        self.view_lpr_btn.setFont(font)
        self.view_lpr_btn.clicked.connect(self.show_current_lpr_handler)  # 绑定事件
        layout.addWidget(self.view_lpr_btn)

        # 保存文件按钮
        self.save_file_btn = QPushButton('保存结果为文件')
        self.save_file_btn.setFont(font)
        self.save_file_btn.clicked.connect(self.save_file_handler)
        layout.addWidget(self.save_file_btn)

        self.setLayout(layout)

    def toggle_rate_input(self):
        rate_type = self.rate_type_input.currentText()
        if rate_type == "LPR利率":
            self.lpr_label.setVisible(True)
            self.lpr_input.setVisible(True)
            self.custom_rate_label.setVisible(False)
            self.custom_rate_input.setVisible(False)
            self.custom_rate_mode_label.setVisible(False)
            self.custom_rate_mode_input.setVisible(False)
            self.method_label.setVisible(True)
            self.segmented_lpr_radio.setVisible(True)
            self.average_lpr_radio.setVisible(True)
            self.end_lpr_radio.setVisible(True)
            self.start_lpr_radio.setVisible(True)
            self.legal_lpr_radio.setVisible(True)
        elif rate_type == "自定义利率":
            self.lpr_label.setVisible(False)
            self.lpr_input.setVisible(False)
            self.custom_rate_label.setVisible(True)
            self.custom_rate_input.setVisible(True)
            self.custom_rate_mode_label.setVisible(True)
            self.custom_rate_mode_input.setVisible(True)
            self.method_label.setVisible(False)
            self.segmented_lpr_radio.setVisible(False)
            self.average_lpr_radio.setVisible(False)
            self.end_lpr_radio.setVisible(False)
            self.start_lpr_radio.setVisible(False)
            self.legal_lpr_radio.setVisible(False)
        else:
            self.lpr_label.setVisible(False)
            self.lpr_input.setVisible(False)
            self.custom_rate_label.setVisible(False)
            self.custom_rate_input.setVisible(False)
            self.custom_rate_mode_label.setVisible(False)
            self.custom_rate_mode_input.setVisible(False)
            self.method_label.setVisible(False)
            self.segmented_lpr_radio.setVisible(False)
            self.average_lpr_radio.setVisible(False)
            self.end_lpr_radio.setVisible(False)
            self.start_lpr_radio.setVisible(False)
            self.legal_lpr_radio.setVisible(False)

    def calculate_penalty_handler(self):
        try:
            # 获取用户输入的违约金额
            amount = float(self.amount_input.text())
        except ValueError:
            self.result_display.setText("请输入有效的违约金额。")
            return

        # 获取用户选择的起始日期和结束日期
        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()

        # 获取用户选择的天数基准（360天或365天）
        days_base = 365 if self.days_base_input.currentText() == "365天" else 360

        # 计算实际的违约天数
        days_total = (end_date - start_date).days

        # 应用天数算法
        day_calculation = self.day_calculation_input.currentText()
        if day_calculation == "算头不算尾":
            days_total -= 1
        elif day_calculation == "两头都算":
            days_total += 1

        # 获取用户选择的利率类型和模式
        rate_type = self.rate_type_input.currentText()
        rate_mode = self.lpr_input.currentText() if rate_type == "LPR利率" else None

        # 从配置文件中加载LPR数据
        lpr_data = load_lpr_config()
        logging.debug(f"当前加载的LPR数据: {lpr_data}")
        
        if rate_type == "LPR利率" and not lpr_data:
            self.result_display.setText("未找到有效的LPR数据，请更新LPR利率。")
            return

        try:
            # 初始化用于存储计算详细过程的文本
            calculation_process = ""

            # 根据不同利率模式进行计算
            if rate_type == "万分之五":
                rate = 0.0005
                penalty = round(amount * rate * days_total, 2)  # 保留两位小数
                calculation_process = f"{amount} × {rate} × {days_total} = {penalty} 元"

            elif rate_type == "自定义利率":
                try:
                    rate = float(self.custom_rate_input.text()) / 100
                    rate_mode = self.custom_rate_mode_input.currentText()
                    if rate_mode == "日利率":
                        penalty = round(amount * rate * days_total, 2)
                        calculation_process = f"{amount} × {rate} × {days_total} = {penalty} 元"
                    elif rate_mode == "月利率":
                        penalty = round(amount * rate * (days_total / 30), 2)
                        calculation_process = f"{amount} × {rate} × ({days_total} / 30) = {penalty} 元"
                    elif rate_mode == "年利率":
                        penalty = round(amount * rate * (days_total / days_base), 2)
                        calculation_process = f"{amount} × {rate} × ({days_total} / {days_base}) = {penalty} 元"

                except ValueError:
                    self.result_display.setText("请输入有效的自定义利率。")
                    return

            elif rate_type == "LPR利率":
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
                if not selected_method:
                    self.result_display.setText("请选择计息方式。")
                    return

                # 获取用户选择的LPR利率类型（一年期或五年期）
                lpr_type = "一年期" if rate_mode == "一年期LPR" else "五年期"

                # 调用计算函数进行违约金计算
                penalty, calculation_process_detail = calculate_penalty(
                    amount, start_date, end_date, days_base, selected_method,
                    lpr_data, day_calculation, lpr_type
                )
                calculation_process = calculation_process_detail

            else:
                self.result_display.setText("请选择利率类型。")
                return

            # 使用HTML格式优化显示内容，苹果审美风格排版
            result_text = (
                f"<b>违约金额:</b> {amount} 元<br>"
                f"<b>利率方式:</b> {rate_type}<br>"
            )
            
            if rate_type == "自定义利率":
                result_text += (
                    f"<b>自定义利率:</b> {rate * 100}%<br>"
                    f"<b>自定义利率模式:</b> {rate_mode}<br>"
                )
            
            result_text += (
                f"<b>起始日期:</b> {start_date}<br>"
                f"<b>结束日期:</b> {end_date}<br>"
                f"<b>天数基准:</b> {days_base} 天<br>"
                f"<b>违约天数:</b> {days_total} 天<br>"
                f"<b>违约金:</b> {penalty} 元<br><br>"
                f"<b>计算过程:</b><br>{calculation_process}<br>"
                f"<hr>"  # 加分割线
            )

            self.result_display.setHtml(result_text)

        except ValueError as e:
            # 捕获错误并在结果框中显示错误信息
            self.result_display.setText(str(e))

    def update_lpr_handler(self):
        self.lpr_data = fetch_latest_lpr()
        if self.lpr_data:
            # 将 lpr_data 转换为 DataFrame
            df = pd.DataFrame.from_dict(self.lpr_data, orient='index')
            df.index.name = '日期'
            df.reset_index(inplace=True)
            # 调整列的顺序
            df = df[['日期', '一年期', '五年期']]
            # 设置表格样式
            html_table = df.style.set_table_styles(
                [
                    {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('margin', '0 auto')]},
                    {'selector': 'th, td', 'props': [('border', '2px solid black'), ('text-align', 'center'), ('padding', '8px')]},
                ]
            ).hide(axis='index').to_html()
            # 在结果显示框中显示表格
            self.result_display.setHtml(html_table)
        else:
            self.result_display.setText("LPR利率更新失败，请检查网络连接或稍后再试。")

    def show_current_lpr_handler(self):
        # 获取当前时间
        current_time = get_current_time()

        # 获取最近的LPR，包括一年期和五年期
        try:
            one_year_lpr, five_year_lpr, closest_date = get_closest_lpr(self.lpr_data, datetime.now().date())
        except Exception as e:
            self.result_display.setText(f"获取LPR时出现错误: {str(e)}")
            return

        # 创建消息框
        msg = QMessageBox()
        msg.setWindowTitle("当前LPR信息")
        
        # 设置消息内容
        msg.setText(
            f"<b>当前时间:</b> {current_time}<br>"
            f"<b>最近LPR公布日期:</b> {closest_date}<br>"
            f"<b>一年期LPR:</b> {one_year_lpr}<br>"
            f"<b>五年期LPR:</b> {five_year_lpr}<br>"
            f"<b>时间服务器:</b> time1.aliyun.com (<a href='http://time1.aliyun.com/'>http://time1.aliyun.com/</a>)<br>"
            f"<b>LPR公布网站:</b> <a href='https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html'>LPR信息</a>"
        )
        
        # 启用超链接
        msg.setTextFormat(1)  # 1 = Qt.RichText
        
        # 显示消息框
        msg.exec_()

    def save_file_handler(self):
        file_dialog = QFileDialog(self)
        file_name, _ = file_dialog.getSaveFileName(self, "保存文件", "", "Excel 文件 (*.xlsx);;Markdown 文件 (*.md)")
        
        if file_name:
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
