import sys
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QRadioButton, QButtonGroup, QDateEdit, QComboBox, QLineEdit,
    QTextEdit, QFileDialog, QInputDialog, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime, timedelta
import logging
import ntplib
from time import ctime

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 获取指定日期最近的LPR
def get_lpr_for_date(lpr_data, date, lpr_type):
    lpr_date_keys = [datetime.strptime(key, "%Y-%m-%d").date() for key in lpr_data.keys()]
    past_dates = [d for d in lpr_date_keys if d <= date]
    if not past_dates:
        closest_date = min(lpr_date_keys)
    else:
        closest_date = max(past_dates)
    lpr_value = lpr_data[closest_date.strftime("%Y-%m-%d")][lpr_type]

    if isinstance(lpr_value, str):
        lpr_value = float(lpr_value.replace('%', '')) / 100

    return lpr_value, closest_date

# 获取当前时间
def get_current_time():
    try:
        client = ntplib.NTPClient()
        logging.debug("正在从 NTP 服务器获取时间...")
        response = client.request('time1.aliyun.com', version=3)
        current_time = ctime(response.tx_time)
        logging.debug(f"成功获取时间: {current_time}")
        return current_time
    except Exception as e:
        logging.error(f"NTP 请求失败: {e}")
        return f"无法获取当前时间，错误: {str(e)}"

# 获取最近的LPR
def get_closest_lpr(lpr_data, target_date):
    lpr_dates = [datetime.strptime(key, '%Y-%m-%d').date() for key in lpr_data.keys()]
    past_dates = [d for d in lpr_dates if d <= target_date]
    if not past_dates:
        closest_date = min(lpr_dates)
    else:
        closest_date = max(past_dates)
    closest_lpr_data = lpr_data[closest_date.strftime('%Y-%m-%d')]

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

    calculation_process = ""
    if method == "分段LPR计算":
        total_penalty = 0
        current_date = start_date
        calculation_details = []
        while current_date < end_date:
            next_month = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
            period_end = min(end_date, next_month)
            days_in_period = (period_end - current_date).days

            lpr_value, lpr_date = get_lpr_for_date(lpr_data, current_date, lpr_type)
            penalty_segment = amount * (days_in_period / days_base) * lpr_value
            total_penalty += penalty_segment

            calculation_details.append(
                f"{current_date.strftime('%Y-%m-%d')} 至 {period_end.strftime('%Y-%m-%d')}, 天数: {days_in_period} 天, LPR发布日期: {lpr_date}, LPR利率: {lpr_value*100:.2f}%, 违约金: {penalty_segment:.2f} 元"
            )

            current_date = period_end

        penalty = total_penalty
        calculation_process = "<br>".join(calculation_details)
        calculation_process += f"<br><b>总违约金: {penalty:.2f} 元</b>"

    elif method == "平均LPR":
        average_lpr = calculate_average_lpr(lpr_data, start_date, end_date, lpr_type)
        penalty = amount * (days_total / days_base) * average_lpr
        calculation_process = f"平均LPR利率: {average_lpr*100:.2f}%<br>违约金 = {amount} × ({days_total} / {days_base}) × {average_lpr*100:.2f}% = {penalty:.2f} 元"

    elif method == "截止月LPR":
        chosen_lpr, lpr_date = get_lpr_for_date(lpr_data, end_date, lpr_type)
        penalty = amount * (days_total / days_base) * chosen_lpr
        calculation_process = f"使用截止日期 {end_date} 最近的LPR（发布日期: {lpr_date}，利率: {chosen_lpr*100:.2f}%）<br>违约金 = {amount} × ({days_total} / {days_base}) × {chosen_lpr*100:.2f}% = {penalty:.2f} 元"

    elif method == "起始月LPR":
        chosen_lpr, lpr_date = get_lpr_for_date(lpr_data, start_date, lpr_type)
        penalty = amount * (days_total / days_base) * chosen_lpr
        calculation_process = f"使用起始日期 {start_date} 最近的LPR（发布日期: {lpr_date}，利率: {chosen_lpr*100:.2f}%）<br>违约金 = {amount} × ({days_total} / {days_base}) × {chosen_lpr*100:.2f}% = {penalty:.2f} 元"

    elif method == "法定最高LPR":
        chosen_lpr, lpr_date = get_lpr_for_date(lpr_data, end_date, lpr_type)
        chosen_lpr *= 4
        penalty = amount * (days_total / days_base) * chosen_lpr
        calculation_process = f"使用截止日期 {end_date} 最近的LPR的4倍（发布日期: {lpr_date}，利率: {chosen_lpr*100:.2f}%）<br>违约金 = {amount} × ({days_total} / {days_base}) × {chosen_lpr*100:.2f}% = {penalty:.2f} 元"

    else:
        raise ValueError("未知的计息方式。")

    return round(penalty, 2), calculation_process

# 保存和读取LPR利率
def load_lpr_config():
    config_file = 'lpr_config.json'
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
    config_file = 'lpr_config.json'
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
    response.encoding = 'utf-8'
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

            try:
                date_obj = datetime.strptime(date_str, "%Y年%m月%d日")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    logging.error(f"无法解析日期格式: {date_str}")
                    continue

            formatted_date = date_obj.strftime("%Y-%m-%d")

            lpr_data[formatted_date] = {
                "一年期": one_year_lpr,
                "五年期": five_year_lpr
            }

    save_lpr_config(lpr_data)
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







# 模板管理界面类
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QDoubleValidator, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit,
    QComboBox, QPushButton, QHBoxLayout, QMessageBox, QWidget
)
import json
import logging


from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle, QSizePolicy

from PyQt5.QtGui import QIcon

class TemplateManagerDialog(QDialog):
    def __init__(self, parent=None):
        super(TemplateManagerDialog, self).__init__(parent)
        self.setWindowTitle('模板管理')
        self.setGeometry(100, 100, 600, 400)  # 窗口大小调整为合适的宽高
        self.setStyleSheet("background-color: #F5F5F5;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # 四列，包含“模板名称”、“利率 (%)”、“利率模式”和“操作”
        self.table.setHorizontalHeaderLabels(['模板名称', '利率 (%)', '利率模式', '操作'])
        self.table.setFixedSize(580, 300)  # 调整表格的大小，使其匹配窗口

        # 载入模板数据
        self.load_templates()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_templates(self):
        template_data = self.load_custom_template()  # 从文件加载模板数据
        self.table.setRowCount(len(template_data) + 1)  # 加1，用于新增模板行

        for i, (name, data) in enumerate(template_data.items()):
            if isinstance(data, dict):
                # 模板名称
                name_item = QLineEdit(name)
                self.table.setCellWidget(i, 0, name_item)

                # 利率输入框，只允许输入数字
                rate_input = QLineEdit(str(data.get('利率', '')))
                rate_input.setValidator(QDoubleValidator(0.0, 100.0, 2))  # 0-100之间的两位小数
                rate_input.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i, 1, rate_input)

                # 利率模式下拉菜单
                mode_input = QComboBox()
                mode_input.addItems(['日利率', '月利率', '年利率'])
                mode_input.setCurrentText(data.get('模式', '日利率'))
                self.table.setCellWidget(i, 2, mode_input)

                # 操作列
                control_layout = QHBoxLayout()
                control_widget = QWidget()

                save_button = QPushButton()
                save_button.setIcon(QIcon("path/to/green_check_icon.png"))  # 绿色的✓
                save_button.setFixedWidth(30)
                save_button.clicked.connect(lambda _, row=i: self.save_template(row))

                delete_button = QPushButton()
                delete_button.setIcon(QIcon("path/to/red_cross_icon.png"))  # ❌
                delete_button.setFixedWidth(30)
                delete_button.clicked.connect(lambda _, row=i: self.delete_template(row))

                control_layout.addWidget(save_button)
                control_layout.addWidget(delete_button)
                control_widget.setLayout(control_layout)
                self.table.setCellWidget(i, 3, control_widget)

        # 添加新增模板的图标按钮
        self.add_new_template_button()

        self.table.resizeColumnsToContents()

    def add_new_template_button(self):
        """ 在表格最后一行增加一个“新增模板”的图标按钮 """
        add_button = QPushButton()
        add_button.setIcon(QIcon("path/to/add_icon.png"))  # ➕图标
        add_button.setFixedWidth(30)
        add_button.clicked.connect(self.add_template)

        control_layout = QHBoxLayout()
        control_widget = QWidget()

        control_layout.addWidget(add_button)
        control_widget.setLayout(control_layout)

        # 在最后一行的操作列中添加新增按钮
        self.table.setCellWidget(self.table.rowCount() - 1, 3, control_widget)


    def save_template(self, row):
        name_widget = self.table.cellWidget(row, 0)
        rate_widget = self.table.cellWidget(row, 1)
        mode_widget = self.table.cellWidget(row, 2)

        name = name_widget.text()
        rate = rate_widget.text()
        mode = mode_widget.currentText()

        if not rate or float(rate) <= 0:
            QMessageBox.warning(self, '无效输入', '请输入大于 0 的有效利率')
            return

        template_data = self.load_custom_template()

        # 检查模板名称是否重复
        if name in template_data:
            QMessageBox.warning(self, '模板重复', '模板名称已存在，请修改模板名称。')
            return

        template_data[name] = {'利率': float(rate), '模式': mode}
        self.save_custom_template(template_data)
        QMessageBox.information(self, '保存成功', f'模板 {name} 已保存。')

    def delete_template(self, row):
        name_widget = self.table.cellWidget(row, 0)
        name = name_widget.text()

        reply = QMessageBox.question(self, '删除确认', f'确定要删除模板 {name} 吗？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_custom_template(name)
            self.table.removeRow(row)
            QMessageBox.information(self, '删除成功', f'模板 {name} 已删除。')

    def add_template(self):
        """ 新增模板时调用 """
        row_position = self.table.rowCount() - 1  # 在倒数第二行插入新模板
        self.table.insertRow(row_position)

        # 模板名称列
        name_item = QLineEdit('')
        self.table.setCellWidget(row_position, 0, name_item)

        # 利率列
        rate_input = QLineEdit('')
        rate_input.setValidator(QDoubleValidator(0.0, 100.0, 2))  # 0-100的两位小数
        rate_input.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row_position, 1, rate_input)

        # 利率模式下拉菜单
        mode_input = QComboBox()
        mode_input.addItems(['日利率', '月利率', '年利率'])
        self.table.setCellWidget(row_position, 2, mode_input)

        # 操作列
        control_layout = QHBoxLayout()
        control_widget = QWidget()

        save_button = QPushButton()
        save_button.setIcon(QIcon.fromTheme("document-save"))  # 使用保存图标
        save_button.setFixedWidth(30)
        save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        save_button.clicked.connect(lambda _, row=row_position: self.save_template(row))

        delete_button = QPushButton()
        delete_button.setIcon(QIcon.fromTheme("edit-delete"))  # 使用删除图标
        delete_button.setFixedWidth(30)
        delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        delete_button.clicked.connect(lambda _, row=row_position: self.delete_template(row))

        control_layout.addWidget(save_button)
        control_layout.addWidget(delete_button)
        control_widget.setLayout(control_layout)

        self.table.setCellWidget(row_position, 3, control_widget)

        # 新增模板行的图标按钮保持在最后
        self.add_new_template_button()

    def load_custom_template(self):
        config_file = 'custom_rate_template.json'
        try:
            with open(config_file, 'r') as file:
                template_data = json.load(file)
                if isinstance(template_data, dict):  # 确保数据是字典格式
                    logging.debug(f"自定义利率模板已从 {config_file} 成功加载: {template_data}")
                    return template_data
                else:
                    logging.error(f"模板数据格式错误: 期望是字典格式，但得到的是 {type(template_data)}")
                    return {}
        except FileNotFoundError:
            logging.error(f"模板文件 {config_file} 未找到。")
            return {}
        except json.JSONDecodeError:
            logging.error(f"模板文件 {config_file} 不是有效的 JSON 格式。")
            return {}
        except Exception as e:
            logging.error(f"读取模板数据失败: {e}")
            return {}

    def save_custom_template(self, template_data):
        config_file = 'custom_rate_template.json'
        try:
            with open(config_file, 'w') as file:
                json.dump(template_data, file, ensure_ascii=False, indent=4)
            logging.debug(f"自定义利率模板已成功保存到 {config_file}: {template_data}")
        except Exception as e:
            logging.error(f"保存模板数据失败: {e}")

    def delete_custom_template(self, template_name):
        template_data = self.load_custom_template()
        if template_name in template_data:
            del template_data[template_name]
            self.save_custom_template(template_data)
            logging.debug(f"模板 {template_name} 已成功删除")
        else:
            logging.error(f"模板 {template_name} 不存在")





# 主程序UI模块
class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.lpr_data = load_lpr_config()

    def init_ui(self):
        self.setWindowTitle('违约金计算器 ---- made by 江山 j19972280991')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        font = QFont("Microsoft Yahei", 13, QFont.Bold)

        main_layout = QVBoxLayout()
        input_layout = QGridLayout()

        self.amount_label = QLabel('违约金额 (元):')
        self.amount_label.setFont(font)
        self.amount_input = QLineEdit()
        self.amount_input.setFont(font)
        input_layout.addWidget(self.amount_label, 0, 0)
        input_layout.addWidget(self.amount_input, 0, 1)

        self.start_date_label = QLabel('开始日期:')
        self.start_date_label.setFont(font)
        self.start_date_input = QDateEdit()
        self.start_date_input.setFont(font)
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        input_layout.addWidget(self.start_date_label, 1, 0)
        input_layout.addWidget(self.start_date_input, 1, 1)

        self.end_date_label = QLabel('结束日期:')
        self.end_date_label.setFont(font)
        self.end_date_input = QDateEdit()
        self.end_date_input.setFont(font)
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        input_layout.addWidget(self.end_date_label, 1, 2)
        input_layout.addWidget(self.end_date_input, 1, 3)

        self.rate_type_label = QLabel('选择利率模式:')
        self.rate_type_label.setFont(font)
        self.rate_type_input = QComboBox()
        self.rate_type_input.addItems(["万分之五", "LPR利率", "自定义利率"])
        self.rate_type_input.setFont(font)
        self.rate_type_input.currentIndexChanged.connect(self.toggle_rate_input)
        input_layout.addWidget(self.rate_type_label, 2, 0)
        input_layout.addWidget(self.rate_type_input, 2, 1)

        self.custom_rate_label = QLabel('自定义利率 (%):')
        self.custom_rate_label.setFont(font)
        self.custom_rate_input = QLineEdit()
        self.custom_rate_input.setFont(font)
        self.custom_rate_input.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.custom_rate_label.setVisible(False)
        self.custom_rate_input.setVisible(False)
        input_layout.addWidget(self.custom_rate_label, 3, 0)
        input_layout.addWidget(self.custom_rate_input, 3, 1)

        self.custom_rate_mode_label = QLabel('自定义利率模式:')
        self.custom_rate_mode_label.setFont(font)
        self.custom_rate_mode_input = QComboBox()
        self.custom_rate_mode_input.addItems(["日利率", "月利率", "年利率"])
        self.custom_rate_mode_input.setFont(font)
        self.custom_rate_mode_label.setVisible(False)
        self.custom_rate_mode_input.setVisible(False)
        input_layout.addWidget(self.custom_rate_mode_label, 3, 2)
        input_layout.addWidget(self.custom_rate_mode_input, 3, 3)

        self.save_template_btn = QPushButton('保存自定义模板')
        self.save_template_btn.setFont(font)
        self.save_template_btn.setVisible(False)
        self.save_template_btn.clicked.connect(self.save_custom_template_handler)
        input_layout.addWidget(self.save_template_btn, 3, 4)

        self.load_template_btn = QPushButton('加载自定义模板')
        self.load_template_btn.setFont(font)
        self.load_template_btn.setVisible(False)
        self.load_template_btn.clicked.connect(self.load_custom_template_handler)
        input_layout.addWidget(self.load_template_btn, 3, 5)

        self.manage_template_btn = QPushButton('模板管理')
        self.manage_template_btn.setFont(font)
        self.manage_template_btn.setVisible(False)
        self.manage_template_btn.clicked.connect(self.manage_custom_template_handler)
        input_layout.addWidget(self.manage_template_btn, 4, 4)

        self.lpr_label = QLabel('选择LPR利率:')
        self.lpr_label.setFont(font)
        self.lpr_input = QComboBox()
        self.lpr_input.addItems(["一年期LPR", "五年期LPR"])
        self.lpr_input.setFont(font)
        self.lpr_label.setVisible(False)
        self.lpr_input.setVisible(False)
        input_layout.addWidget(self.lpr_label, 4, 0)
        input_layout.addWidget(self.lpr_input, 4, 1)

        self.days_base_label = QLabel('选择自然年天数基准:')
        self.days_base_label.setFont(font)
        self.days_base_input = QComboBox()
        self.days_base_input.addItems(["360天", "365天"])
        self.days_base_input.setFont(font)
        input_layout.addWidget(self.days_base_label, 5, 0)
        input_layout.addWidget(self.days_base_input, 5, 1)

        self.day_calculation_label = QLabel('选择天数算法:')
        self.day_calculation_label.setFont(font)
        self.day_calculation_input = QComboBox()
        self.day_calculation_input.addItems(["算头不算尾", "两头都算"])
        self.day_calculation_input.setFont(font)
        input_layout.addWidget(self.day_calculation_label, 5, 2)
        input_layout.addWidget(self.day_calculation_input, 5, 3)

        self.method_label = QLabel('选择计息方式:')
        self.method_label.setFont(font)
        self.method_group = QButtonGroup(self)

        self.segmented_lpr_radio = QRadioButton("分段LPR计算")
        self.segmented_lpr_radio.setFont(font)
        self.average_lpr_radio = QRadioButton("平均LPR")
        self.average_lpr_radio.setFont(font)
        self.end_lpr_radio = QRadioButton("截止月LPR")
        self.end_lpr_radio.setFont(font)
        self.start_lpr_radio = QRadioButton("起始月LPR")
        self.start_lpr_radio.setFont(font)
        self.legal_lpr_radio = QRadioButton("法定最高LPR")
        self.legal_lpr_radio.setFont(font)

        self.method_group.addButton(self.segmented_lpr_radio)
        self.method_group.addButton(self.average_lpr_radio)
        self.method_group.addButton(self.end_lpr_radio)
        self.method_group.addButton(self.start_lpr_radio)
        self.method_group.addButton(self.legal_lpr_radio)

        self.method_label.setVisible(False)
        self.segmented_lpr_radio.setVisible(False)
        self.average_lpr_radio.setVisible(False)
        self.end_lpr_radio.setVisible(False)
        self.start_lpr_radio.setVisible(False)
        self.legal_lpr_radio.setVisible(False)

        input_layout.addWidget(self.method_label, 6, 0)
        input_layout.addWidget(self.segmented_lpr_radio, 6, 1)
        input_layout.addWidget(self.average_lpr_radio, 6, 2)
        input_layout.addWidget(self.end_lpr_radio, 6, 3)
        input_layout.addWidget(self.start_lpr_radio, 6, 4)
        input_layout.addWidget(self.legal_lpr_radio, 6, 5)

        main_layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.calculate_btn = QPushButton('计算违约金')
        self.calculate_btn.setFont(font)
        self.calculate_btn.clicked.connect(self.calculate_penalty_handler)
        self.calculate_btn.setFixedHeight(40)
        button_layout.addWidget(self.calculate_btn)

        self.update_lpr_btn = QPushButton('更新LPR利率')
        self.update_lpr_btn.setFont(font)
        self.update_lpr_btn.clicked.connect(self.update_lpr_handler)
        self.update_lpr_btn.setFixedHeight(40)
        button_layout.addWidget(self.update_lpr_btn)

        self.view_lpr_btn = QPushButton('查看当前LPR')
        self.view_lpr_btn.setFont(font)
        self.view_lpr_btn.clicked.connect(self.show_current_lpr_handler)
        self.view_lpr_btn.setFixedHeight(40)
        button_layout.addWidget(self.view_lpr_btn)

        self.save_file_btn = QPushButton('保存结果为文件')
        self.save_file_btn.setFont(font)
        self.save_file_btn.clicked.connect(self.save_file_handler)
        self.save_file_btn.setFixedHeight(40)
        button_layout.addWidget(self.save_file_btn)

        main_layout.addLayout(button_layout)

        self.result_display = QTextEdit()
        self.result_display.setFont(font)
        self.result_display.setReadOnly(True)
        main_layout.addWidget(self.result_display)

        self.setLayout(main_layout)

    def toggle_rate_input(self):
        rate_type = self.rate_type_input.currentText()
        if rate_type == "LPR利率":
            self.lpr_label.setVisible(True)
            self.lpr_input.setVisible(True)
            self.custom_rate_label.setVisible(False)
            self.custom_rate_input.setVisible(False)
            self.custom_rate_mode_label.setVisible(False)
            self.custom_rate_mode_input.setVisible(False)
            self.save_template_btn.setVisible(False)
            self.load_template_btn.setVisible(False)
            self.manage_template_btn.setVisible(False)
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
            self.save_template_btn.setVisible(True)
            self.load_template_btn.setVisible(True)
            self.manage_template_btn.setVisible(True)
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
            self.save_template_btn.setVisible(False)
            self.load_template_btn.setVisible(False)
            self.manage_template_btn.setVisible(False)
            self.method_label.setVisible(False)
            self.segmented_lpr_radio.setVisible(False)
            self.average_lpr_radio.setVisible(False)
            self.end_lpr_radio.setVisible(False)
            self.start_lpr_radio.setVisible(False)
            self.legal_lpr_radio.setVisible(False)



    def save_template(self, row):
        name_widget = self.table.cellWidget(row, 0)
        rate_widget = self.table.cellWidget(row, 1)
        mode_widget = self.table.cellWidget(row, 2)

        rate = rate_widget.text()
        mode = mode_widget.currentText()

        if not rate or float(rate) <= 0:
            QMessageBox.warning(self, '无效输入', '请输入大于 0 的有效利率')
            return

        # 弹出对话框输入模板名称
        name, ok = QInputDialog.getText(self, '保存模板', '请输入模板名称:')
        if not ok or not name:
            return

        template_data = self.load_custom_template()

        # 检查模板名称是否重复
        if name in template_data:
            QMessageBox.warning(self, '模板重复', '模板名称已存在，请修改模板名称。')
            return

        template_data[name] = {'利率': float(rate), '模式': mode}
        self.save_custom_template(template_data)
        QMessageBox.information(self, '保存成功', f'模板 {name} 已保存。')

    def load_template(self):
        template_data = self.load_custom_template()

        # 如果没有模板可供选择
        if not template_data:
            QMessageBox.warning(self, '没有可用模板', '当前没有可用模板，请先保存一个模板。')
            return

        # 使用下拉菜单选择要加载的模板
        template_list = list(template_data.keys())
        dialog = QInputDialog(self)
        dialog.setComboBoxItems(template_list)
        dialog.setLabelText('选择要加载的模板:')
        dialog.setWindowTitle('加载模板')

        if dialog.exec_() == QInputDialog.Accepted:
            selected_template = dialog.textValue()
            data = template_data.get(selected_template)

            # 加载模板信息到当前表格
            self.table.setRowCount(1)  # 清空表格，仅保留一行
            name_item = QLineEdit(selected_template)
            self.table.setCellWidget(0, 0, name_item)
            rate_input = QLineEdit(str(data.get('利率', '')))
            rate_input.setValidator(QDoubleValidator(0.0, 100.0, 2))  # 0-100之间的两位小数
            rate_input.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(0, 1, rate_input)
            mode_input = QComboBox()
            mode_input.addItems(['日利率', '月利率', '年利率'])
            mode_input.setCurrentText(data.get('模式', '日利率'))
            self.table.setCellWidget(0, 2, mode_input)

            QMessageBox.information(self, '加载成功', f'模板 {selected_template} 已成功加载。')   

    def save_custom_template_handler(self):
        rate = self.custom_rate_input.text()
        rate_mode = self.custom_rate_mode_input.currentText()

        if not rate or float(rate) <= 0:
            self.result_display.setText("请输入有效的利率（大于 0）。")
            return

        # 弹出对话框要求用户输入模板名称
        template_name, ok = QInputDialog.getText(self, '保存模板', '请输入模板名称:')
        if not ok or not template_name:
            self.result_display.setText("模板保存已取消。")
            return

        template_data = self.load_custom_template()  # 调用类中的方法读取现有模板

        # 检查是否存在相同模板名称
        if template_name in template_data:
            self.result_display.setText(f"模板名称 '{template_name}' 已存在，请选择其他名称。")
            return

        # 将新的模板保存到字典中
        template_data[template_name] = {
            "利率": rate,
            "模式": rate_mode
        }

        # 保存到JSON文件
        self.save_custom_template(template_data)
        self.result_display.setText(f"自定义利率模板 '{template_name}' 已成功保存:\n利率: {rate}%\n模式: {rate_mode}")

    def load_custom_template_handler(self):
        template_data = self.load_custom_template()  # 调用类中的方法加载模板

        if not template_data:
            self.result_display.setText("未找到自定义利率模板，请先保存模板。")
            return

        # 弹出对话框选择要加载的模板
        template_name, ok = QInputDialog.getItem(self, '加载模板', '请选择模板:', template_data.keys(), 0, False)
        if not ok or not template_name:
            self.result_display.setText("模板加载已取消。")
            return

        selected_template = template_data.get(template_name)
        if selected_template:
            # 加载模板信息到输入框
            self.custom_rate_input.setText(selected_template.get("利率", ""))
            mode = selected_template.get("模式", "日利率")
            index = self.custom_rate_mode_input.findText(mode)
            if index != -1:
                self.custom_rate_mode_input.setCurrentIndex(index)

            self.result_display.setText(f"自定义利率模板 '{template_name}' 已加载:\n利率: {selected_template.get('利率', '')}%\n模式: {mode}")
        else:
            self.result_display.setText("未找到选定的模板。")



    def manage_custom_template_handler(self):
        self.template_manager = TemplateManagerDialog(self)
        self.template_manager.exec_()

    def calculate_penalty_handler(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.result_display.setText("请输入有效的违约金额。")
            return

        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()
        days_base = 365 if self.days_base_input.currentText() == "365天" else 360
        days_total = (end_date - start_date).days
        day_calculation = self.day_calculation_input.currentText()
        if day_calculation == "算头不算尾":
            days_total -= 1
        elif day_calculation == "两头都算":
            days_total += 1

        rate_type = self.rate_type_input.currentText()
        rate_mode = self.lpr_input.currentText() if rate_type == "LPR利率" else None
        lpr_data = load_lpr_config()
        logging.debug(f"当前加载的LPR数据: {lpr_data}")
        
        if rate_type == "LPR利率" and not lpr_data:
            self.result_display.setText("未找到有效的LPR数据，请更新LPR利率。")
            return

        try:
            calculation_process = ""

            if rate_type == "万分之五":
                rate = 0.0005
                penalty = round(amount * rate * days_total, 2)
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

                lpr_type = "一年期" if rate_mode == "一年期LPR" else "五年期"

                penalty, calculation_process_detail = calculate_penalty(
                    amount, start_date, end_date, days_base, selected_method,
                    lpr_data, day_calculation, lpr_type
                )
                calculation_process = calculation_process_detail

            else:
                self.result_display.setText("请选择利率类型。")
                return

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
                f"<hr>"
            )

            self.result_display.setHtml(result_text)

        except ValueError as e:
            self.result_display.setText(str(e))

    def update_lpr_handler(self):
        self.lpr_data = fetch_latest_lpr()
        if self.lpr_data:
            df = pd.DataFrame.from_dict(self.lpr_data, orient='index')
            df.index.name = '日期'
            df.reset_index(inplace=True)
            df = df[['日期', '一年期', '五年期']]
            html_table = df.style.set_table_styles(
                [
                    {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('margin', '0 auto')]},
                    {'selector': 'th, td', 'props': [('border', '2px solid black'), ('text-align', 'center'), ('padding', '8px')]},
                ]
            ).hide(axis='index').to_html()
            self.result_display.setHtml(html_table)
        else:
            self.result_display.setText("LPR利率更新失败，请检查网络连接或稍后再试。")

    def show_current_lpr_handler(self):
        current_time = get_current_time()

        try:
            one_year_lpr, five_year_lpr, closest_date = get_closest_lpr(self.lpr_data, datetime.now().date())
        except Exception as e:
            self.result_display.setText(f"获取LPR时出现错误: {str(e)}")
            return

        msg = QMessageBox()
        msg.setWindowTitle("当前LPR信息")
        
        msg.setText(
            f"<b>当前时间:</b> {current_time}<br>"
            f"<b>最近LPR公布日期:</b> {closest_date}<br>"
            f"<b>一年期LPR:</b> {one_year_lpr}<br>"
            f"<b>五年期LPR:</b> {five_year_lpr}<br>"
            f"<b>时间服务器:</b> time1.aliyun.com (<a href='http://time1.aliyun.com/'>http://time1.aliyun.com/</a>)<br>"
            f"<b>LPR公布网站:</b> <a href='https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html'>LPR信息</a>"
        )
        
        msg.setTextFormat(1)
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
