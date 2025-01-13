import sys
import time
import os
import pickle
import winreg
import re
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QMessageBox, QInputDialog,
    QFileDialog, QComboBox, QVBoxLayout, QDialog, QPushButton, QLabel,
    QCheckBox, QSizePolicy, QWidget, QHBoxLayout, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QHeaderView, QLineEdit, QTableWidget, QTableWidgetItem,
    QFrame, QGroupBox, QFormLayout, QDateTimeEdit
)
from PyQt5.QtGui import QIcon, QColor, QPalette, QFont
from PyQt5.QtCore import (
    Qt, QTimer, pyqtSignal, QObject, QDateTime
)
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# 初始化日志记录
logging.basicConfig(filename='auto_naming.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')  # 添加encoding='utf-8'

# 用于清理文件名中的非法字符
def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

class MyHandler(FileSystemEventHandler):
    def __init__(self, target_path, naming_rule, log_callback, include_subfolders=False):
        self.target_path = target_path
        self.naming_rule = naming_rule
        self.log_callback = log_callback
        self.include_subfolders = include_subfolders
        self.file_counter = 1  # 用于顺序命名
        super().__init__()

    def is_temp_or_hidden_file(self, file_path):
        """判断是否为临时文件或隐藏文件"""
        file_name = os.path.basename(file_path)
        # 判断是否为隐藏文件（以.开头或具有隐藏属性）
        if file_name.startswith('.') or os.stat(file_path).st_file_attributes & 0x2:
            return True
        # 判断是否为临时文件（常见的临时文件后缀）
        temp_extensions = ['.tmp', '.temp', '~']
        if any(file_name.lower().endswith(ext) for ext in temp_extensions):
            return True
        return False

    def is_file_from_other_folder(self, file_path):
        """判断文件是否是从其他文件夹复制或移动过来的"""
        # 获取文件的创建时间
        create_time = os.path.getctime(file_path)
        current_time = time.time()
        # 如果文件的创建时间与当前时间相差较小（例如1秒内），则认为是外部文件
        return abs(current_time - create_time) < 0.1  # 0.1秒的阈值

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if self.is_temp_or_hidden_file(file_path):
                self.log_callback(f'忽略临时文件或隐藏文件: {file_path}')
                return
            if not self.is_file_from_other_folder(file_path):
                self.log_callback(f'忽略非外部文件: {file_path}')
                return

            file_dir, file_name = os.path.split(file_path)
            file_name_no_ext, file_ext = os.path.splitext(file_name)
            file_name_no_ext = clean_filename(file_name_no_ext)  # 清理文件名中的非法字符

            # 获取当前日期，并去掉月份和天数的前导零
            now = datetime.now()
            current_date = f"{now.year}-{now.month}-{now.day}"  # 手动去掉前导零

            if self.naming_rule == "顺序命名":
                new_file_name = f"{self.file_counter}.{file_name_no_ext}{file_ext}"
                self.file_counter += 1
            else:
                new_file_name = self.naming_rule.format(file_name=file_name_no_ext, date=current_date) + file_ext

            new_file_path = os.path.join(file_dir, new_file_name)
            max_retries = 5
            retry_delay = 0.5
            for retry in range(max_retries):
                try:
                    os.rename(file_path, new_file_path)
                    self.log_callback(f'重命名文件 {file_path} 为 {new_file_path} 成功')
                    break
                except OSError as e:
                    self.log_callback(f'重命名文件 {file_path} 时出现错误: {e}')
                    if retry < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        self.log_callback(f'重命名文件 {file_path} 失败，经过 {max_retries} 次重试')

class TrayApp(QObject):
    monitor_started = pyqtSignal()
    log_updated = pyqtSignal(str)  # 新增信号，用于传递日志内容

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)  # 确保程序不因最后一个窗口关闭而退出
        self.app.setApplicationName("工作流自动化-文件重命名")  # 设置程序名称

        # 创建一个主窗口，用于绑定快捷键
        self.main_window = QWidget()
        self.main_window.setWindowTitle("工作流自动化-文件重命名")
        self.main_window.hide()  # 隐藏主窗口，只显示托盘图标

        self.icon_path = r"C:\Users\Administrator\OneDrive\Desktop\py\屏幕截图 2024-01-16 000502-1种尺寸.ico"
        self.target_paths = []  # 多个目标路径
        self.naming_rules = {}  # 每个路径对应的命名规则
        self.include_subfolders = {}  # 每个路径是否包含子文件夹
        self.is_running = False
        self.template_path = ""
        self.templates = []
        self.startup_checkbox = QCheckBox('开机自动启动')
        self.log_history = []  # 全局日志记录
        self.load_templates()
        self.load_startup_status()
        self.load_log_history()  # 加载日志历史
        self.load_last_settings()  # 加载上次的设置

        self.monitor_started.connect(self.show_start_monitor_notification)

        # 创建系统托盘图标
        self.tray = QSystemTrayIcon(QIcon(self.icon_path))
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

        # 创建菜单
        self.menu = QMenu()
        self.start_action = self.menu.addAction('开始自动命名')
        self.stop_action = self.menu.addAction('结束自动命名')
        self.settings_action = self.menu.addAction('设置')
        self.template_action = self.menu.addAction('模板')
        self.exit_action = self.menu.addAction('关闭程序')

        self.start_action.triggered.connect(self.start_auto_naming)
        self.stop_action.triggered.connect(self.stop_auto_naming)
        self.settings_action.triggered.connect(self.show_settings_dialog)
        self.template_action.triggered.connect(self.show_template_menu)
        self.exit_action.triggered.connect(self.exit_app)

        self.tray.setContextMenu(self.menu)

        # 初始化观察者
        self.observer = None
        self.executor = ThreadPoolExecutor()

        # 初始化 settings_dialog 为 None
        self.settings_dialog = None

    def load_last_settings(self):
        """加载上次的设置"""
        if os.path.exists('last_settings.template'):
            try:
                with open('last_settings.template', 'rb') as f:
                    template_data = pickle.load(f)
                    self.target_paths = template_data.get('target_paths', [])
                    self.naming_rules = template_data.get('naming_rules', {})
                    self.include_subfolders = template_data.get('include_subfolders', {})
                    self.log_message("成功加载缓存模板: last_settings.template")
            except Exception as e:
                self.log_message(f"加载缓存模板时出现错误: {e}")
        else:
            self.log_message("未找到缓存模板，使用默认设置")

    def update_ui_with_last_settings(self):
        """将加载的设置反馈到界面"""
        if self.settings_dialog is not None:
            # 清空目录树
            self.settings_dialog.folder_tree.clear()
            # 添加文件夹到目录树
            for target_path in self.target_paths:
                item = QTreeWidgetItem(self.settings_dialog.folder_tree)
                item.setText(1, target_path)  # 文件夹名
                checkbox = QCheckBox()
                checkbox.setChecked(True)  # 默认选中
                checkbox.stateChanged.connect(lambda state, item=item: self.on_checkbox_state_changed(state, item))
                self.settings_dialog.folder_tree.setItemWidget(item, 0, checkbox)
                
                # 添加删除按钮
                delete_button = QPushButton("❎")
                delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        color: #ff0000;
                    }
                    QPushButton:pressed {
                        color: #cc0000;
                    }
                """)
                delete_button.clicked.connect(lambda: self.delete_folder_item(item))
                self.settings_dialog.folder_tree.setItemWidget(item, 2, delete_button)

    def save_last_settings(self):
        """保存当前设置为缓存模板"""
        template_data = {
            'target_paths': self.target_paths,
            'naming_rules': self.naming_rules,
            'include_subfolders': self.include_subfolders
        }
        try:
            with open('last_settings.template', 'wb') as f:
                pickle.dump(template_data, f)
            self.log_message("成功保存缓存模板: last_settings.template")
        except Exception as e:
            self.log_message(f"保存缓存模板时出现错误: {e}")

    def log_message(self, message):
        """记录日志到全局日志列表"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}"
        self.log_history.append(log_entry)
        self.save_log_history()  # 保存日志到文件
        self.log_updated.emit(log_entry)  # 发送信号，通知日志更新

    def load_log_history(self):
        """从文件加载日志历史"""
        if os.path.exists('log_history.txt'):
            with open('log_history.txt', 'r', encoding='utf-8') as f:
                self.log_history = f.read().splitlines()

    def save_log_history(self):
        """保存日志历史到文件"""
        with open('log_history.txt', 'a', encoding='utf-8') as f:  # 使用追加模式
            f.write("\n".join(self.log_history) + "\n")

    def load_startup_status(self):
        """加载开机自启状态"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                 winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, "工作流自动化-文件重命名")
                if value:
                    self.startup_checkbox.setChecked(True)
                    self.log_message("开机自启状态: 已启用")
                else:
                    self.startup_checkbox.setChecked(False)
                    self.log_message("开机自启状态: 未启用")
            except FileNotFoundError:
                self.startup_checkbox.setChecked(False)
                self.log_message("开机自启状态: 未启用")
            winreg.CloseKey(key)
        except FileNotFoundError:
            self.startup_checkbox.setChecked(False)
            self.log_message("开机自启状态: 未启用")

    def set_startup(self, enable):
        """设置开机自启"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_SET_VALUE)
        if enable:
            script_path = os.path.abspath(sys.argv[0])
            winreg.SetValueEx(key, "工作流自动化-文件重命名", 0, winreg.REG_SZ, script_path)
            self.log_message("已启用开机自启")
        else:
            try:
                winreg.DeleteValue(key, "工作流自动化-文件重命名")
                self.log_message("已禁用开机自启")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)

    def start_auto_naming(self):
        if self.is_running:
            self.log_message("自动命名已经在运行中，无需重复启动")
            return
        if not self.is_running:
            self.is_running = True
            for target_path in self.target_paths:
                event_handler = MyHandler(target_path, self.naming_rules.get(target_path, "{date}-{file_name}"), self.log_message, self.include_subfolders.get(target_path, False))
                observer = Observer()
                observer.schedule(event_handler, target_path, recursive=self.include_subfolders.get(target_path, False))
                self.executor.submit(observer.start)
                self.log_message(f"监控已启动: {target_path}")
            self.monitor_started.emit()
            self.save_last_settings()  # 启动监控后自动保存缓存模板

    def stop_auto_naming(self):
        if not self.is_running:
            self.log_message("自动命名未运行，无需执行停止操作")
            return
        if self.is_running:
            self.is_running = False
            self.executor.shutdown(wait=False)
            self.log_message("监控已停止")
            self.save_last_settings()  # 停止监控后自动保存缓存模板

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # 单击
            self.show_settings_dialog()
        elif reason == QSystemTrayIcon.DoubleClick:  # 双击
            self.show_settings_dialog()

    def show_settings_dialog(self):
        if self.settings_dialog is None:
            self.settings_dialog = CustomDialog(self)  # 将 self 作为 parent_widget 传递
            self.apply_apple_style(self.settings_dialog)
            self.settings_dialog.setWindowTitle('设置')
            self.settings_dialog.resize(1000, 800)  # 设置对话框宽度

            # 设置全局字体
            font = QFont("微软雅黑", 12)
            font.setBold(True)
            self.settings_dialog.setFont(font)

            # 主布局
            main_layout = QVBoxLayout()

            # 命名规则模块
            naming_rule_group = QGroupBox("命名规则")
            naming_rule_layout = QVBoxLayout()
            naming_rule_label = QLabel('')
            self.naming_rule_tip = QLabel('示例：年-月-日-原有文件名称，可使用{date}代表当前日期，{file_name}代表原文件名，如：{date}-{file_name}')
            self.naming_rule_combo = QComboBox()
            self.naming_rule_combo.addItems(['{date}-{file_name}', '{file_name}-{date}', '{date}_{file_name}', '顺序命名'])
            self.naming_rule_combo.addItem('自定义')
            self.naming_rule_combo.currentIndexChanged.connect(self.handle_naming_rule_selection)

            self.custom_naming_rule_input = QInputDialog()
            self.custom_naming_rule_input.setLabelText('请输入自定义命名规则:')
            self.custom_naming_rule_input.setWindowTitle('自定义命名规则')
            self.custom_naming_rule_input.hide()

            naming_rule_layout.addWidget(naming_rule_label)
            naming_rule_layout.addWidget(self.naming_rule_tip)
            naming_rule_layout.addWidget(self.naming_rule_combo)
            naming_rule_layout.addWidget(self.custom_naming_rule_input)
            naming_rule_group.setLayout(naming_rule_layout)

            # 文件夹监控模块
            folder_group = QGroupBox("文件夹监控")
            folder_layout = QVBoxLayout()
            folder_label = QLabel('')
            self.folder_button = QPushButton('选择文件夹')
            self.folder_button.clicked.connect(self.select_folder)
            self.settings_dialog.folder_tree = QTreeWidget()
            self.settings_dialog.folder_tree.setHeaderLabels(["是否监控", "文件夹名", "删除"])
            self.settings_dialog.folder_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.settings_dialog.folder_tree.itemClicked.connect(self.on_folder_item_clicked)

            folder_layout.addWidget(folder_label)
            folder_layout.addWidget(self.folder_button)
            folder_layout.addWidget(self.settings_dialog.folder_tree)
            folder_group.setLayout(folder_layout)

            # 日志功能模块
            log_group = QGroupBox("日志记录")
            log_layout = QVBoxLayout()
            log_label = QLabel('')
            self.log_table = QTableWidget()
            self.log_table.setColumnCount(2)
            self.log_table.setHorizontalHeaderLabels(['操作时间', '操作内容'])
            self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # 日志查询功能
            log_query_layout = QHBoxLayout()
            self.log_query_button = QPushButton('查询日志')
            self.log_query_button.clicked.connect(self.show_log_query_dialog)

            log_query_layout.addWidget(self.log_query_button)

            log_layout.addWidget(log_label)
            log_layout.addLayout(log_query_layout)
            log_layout.addWidget(self.log_table)
            log_group.setLayout(log_layout)

            # 开机自启动功能
            startup_group = QGroupBox("")
            startup_layout = QVBoxLayout()
            self.startup_checkbox = QCheckBox('开机自动启动')
            self.startup_checkbox.stateChanged.connect(self.toggle_startup)
            startup_layout.addWidget(self.startup_checkbox)
            startup_group.setLayout(startup_layout)

            # 新增功能区
            action_group = QGroupBox("")
            action_layout = QVBoxLayout()

            # 第一行按钮
            first_row_layout = QHBoxLayout()
            self.save_template_button = QPushButton('保存为模板')
            self.load_template_button = QPushButton('加载模板')
            first_row_layout.addWidget(self.save_template_button)
            first_row_layout.addWidget(self.load_template_button)

            # 第二行按钮
            second_row_layout = QHBoxLayout()
            self.start_monitor_button = QPushButton('启动监控')
            self.stop_monitor_button = QPushButton('停止监控')
            second_row_layout.addWidget(self.start_monitor_button)
            second_row_layout.addWidget(self.stop_monitor_button)

            action_layout.addLayout(first_row_layout)
            action_layout.addLayout(second_row_layout)
            action_group.setLayout(action_layout)

            # 主布局添加模块
            main_layout.addWidget(naming_rule_group)
            main_layout.addWidget(folder_group)
            main_layout.addWidget(log_group)
            main_layout.addWidget(startup_group)
            main_layout.addWidget(action_group)

            self.settings_dialog.setLayout(main_layout)
            self.settings_dialog.closeEvent = self.handle_dialog_close

            # 连接日志更新信号
            self.log_updated.connect(self.settings_dialog.update_log_display)

            # 设置定时器，定期刷新日志显示
            self.log_timer = QTimer()
            self.log_timer.timeout.connect(self.settings_dialog.load_log_history)
            self.log_timer.start(1000)  # 每1秒刷新一次

        # 更新日志显示
        self.settings_dialog.load_log_history()
        # 如果 settings_dialog 已经初始化，更新界面
        if self.settings_dialog is not None:
            self.update_ui_with_last_settings()
        self.settings_dialog.show()

    def toggle_startup(self, state):
        """切换开机自启状态"""
        if state == Qt.Checked:
            self.set_startup(True)
        else:
            self.set_startup(False)

    def show_log_query_dialog(self):
        """显示日志查询对话框"""
        dialog = QDialog(self.settings_dialog)
        dialog.setWindowTitle('日志查询')
        dialog.resize(400, 200)

        layout = QVBoxLayout()

        # 开始时间选择
        start_time_label = QLabel('开始时间:')
        self.start_time_edit = QDateTimeEdit()
        self.start_time_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(start_time_label)
        layout.addWidget(self.start_time_edit)

        # 结束时间选择
        end_time_label = QLabel('结束时间:')
        self.end_time_edit = QDateTimeEdit()
        self.end_time_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(end_time_label)
        layout.addWidget(self.end_time_edit)

        # 查询按钮
        query_button = QPushButton('查询')
        query_button.clicked.connect(lambda: self.query_logs(
            self.start_time_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            self.end_time_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        ))
        layout.addWidget(query_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def query_logs(self, start_time, end_time):
        """查询日志"""
        self.log_table.setRowCount(0)
        for log_entry in self.log_history:
            parts = log_entry.split(' - ')
            if len(parts) >= 2:
                timestamp, message = parts[0], parts[1]
                if start_time <= timestamp <= end_time:
                    row = self.log_table.rowCount()
                    self.log_table.insertRow(row)
                    self.log_table.setItem(row, 0, QTableWidgetItem(timestamp))
                    self.log_table.setItem(row, 1, QTableWidgetItem(message))

    def handle_dialog_close(self, event):
        self.settings_dialog.hide()
        event.ignore()

    def apply_apple_style(self, dialog):
        # 设置整体背景色为淡灰色，接近苹果风格的素雅背景
        palette = dialog.palette()
        palette.setColor(QPalette.Window, QColor(242, 243, 245))
        palette.setColor(QPalette.WindowText, QColor(242, 243, 245))
        dialog.setPalette(palette)

        # 对按钮应用苹果风格的样式，增加悬浮效果
        style_sheet = """
            QPushButton {
                background-color: #007AFF;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
                font-family: 微软雅黑;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
            QLabel {
                color: #323232;
                font-family: 微软雅黑;
                font-size: 12px;
                font-weight: bold;
            }
            QDialog {
                background-color: #f8f8f8;
            }
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 3px;
                background-color: #f8f8f8;
                font-family: 微软雅黑;
                font-size: 12px;
                font-weight: bold;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f8f8f8;
                font-family: 微软雅黑;
                font-size: 12px;
                font-weight: bold;
            }
            QTreeWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f8f8f8;
                font-family: 微软雅黑;
                font-size: 12px;
                font-weight: bold;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f8f8f8;
                font-family: 微软雅黑;
                font-size: 12px;
                font-weight: bold;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                font-family: 微软雅黑;
                font-size: 14px;
                font-weight: bold;
            }
        """
        dialog.setStyleSheet(style_sheet)

    def handle_naming_rule_selection(self, index):
        if index == self.naming_rule_combo.count() - 1:
            self.custom_naming_rule_input.show()
        else:
            self.custom_naming_rule_input.hide()
        # 更新命名规则提示
        if index == 0:
            self.naming_rule_tip.setText("示例：年-月-日-原有文件名称，可使用{date}代表当前日期，{file_name}代表原文件名，如：{date}-{file_name}")
        elif index == 1:
            self.naming_rule_tip.setText("示例：原有文件名称-年-月-日，可使用{file_name}代表原文件名，{date}代表当前日期，如：{file_name}-{date}")
        elif index == 2:
            self.naming_rule_tip.setText("示例：年-月-日_原有文件名称，可使用{date}代表当前日期，{file_name}代表原文件名，如：{date}_{file_name}")
        elif index == 3:
            self.naming_rule_tip.setText("顺序命名：文件将按照1、2、3的顺序命名，如：1.文件名、2.文件名")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(None, '选择监控文件夹', '')
        if folder_path:
            # 检查文件夹是否已经存在
            if folder_path in self.target_paths:
                self.log_message(f"文件夹路径已存在: {folder_path}")
                return

            item = QTreeWidgetItem(self.settings_dialog.folder_tree)
            item.setText(1, folder_path)  # 文件夹名
            checkbox = QCheckBox()
            checkbox.setChecked(True)  # 默认选中
            checkbox.stateChanged.connect(lambda state, item=item: self.on_checkbox_state_changed(state, item))
            self.settings_dialog.folder_tree.setItemWidget(item, 0, checkbox)
            
            # 添加删除按钮
            delete_button = QPushButton("❎")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: #ff0000;
                }
                QPushButton:pressed {
                    color: #cc0000;
                }
            """)
            delete_button.clicked.connect(lambda: self.delete_folder_item(item))
            self.settings_dialog.folder_tree.setItemWidget(item, 2, delete_button)
            
            self.target_paths.append(folder_path)
            self.log_message(f"监控文件夹已添加: {folder_path}")
            self.log_message(f"当前 target_paths: {self.target_paths}")  # 调试日志
        else:
            self.log_message(f"文件夹路径无效: {folder_path}")  # 调试日志

    def delete_folder_item(self, item):
        """删除文件夹项"""
        folder_path = item.text(1)
        if folder_path in self.target_paths:
            self.target_paths.remove(folder_path)
            self.settings_dialog.folder_tree.takeTopLevelItem(self.settings_dialog.folder_tree.indexOfTopLevelItem(item))
            self.log_message(f"监控文件夹已删除: {folder_path}")
            self.log_message(f"当前 target_paths: {self.target_paths}")  # 调试日志

    def on_folder_item_clicked(self, item):
        folder_path = item.text(1)
        if os.path.isdir(folder_path) and item.childCount() == 0:  # 避免重复加载子文件夹
            for subdir in os.listdir(folder_path):
                subdir_path = os.path.join(folder_path, subdir)
                if os.path.isdir(subdir_path):
                    child_item = QTreeWidgetItem(item)
                    child_item.setText(1, subdir_path)  # 文件夹名
                    checkbox = QCheckBox()
                    checkbox.setChecked(True)  # 默认选中
                    checkbox.stateChanged.connect(lambda state, item=child_item: self.on_checkbox_state_changed(state, item))
                    self.settings_dialog.folder_tree.setItemWidget(child_item, 0, checkbox)
                    
                    # 添加删除按钮
                    delete_button = QPushButton("❎")
                    delete_button.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            border: none;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            color: #ff0000;
                        }
                        QPushButton:pressed {
                            color: #cc0000;
                        }
                    """)
                    delete_button.clicked.connect(lambda: self.delete_folder_item(child_item))
                    self.settings_dialog.folder_tree.setItemWidget(child_item, 2, delete_button)

    def on_checkbox_state_changed(self, state, item):
        """当复选框状态改变时，递归处理子文件夹"""
        checkbox = self.settings_dialog.folder_tree.itemWidget(item, 0)
        if checkbox.isChecked():
            # 如果选中父文件夹，自动选中所有子文件夹
            for i in range(item.childCount()):
                child_item = item.child(i)
                child_checkbox = self.settings_dialog.folder_tree.itemWidget(child_item, 0)
                child_checkbox.setChecked(True)
        else:
            # 如果取消选中父文件夹，自动取消选中所有子文件夹
            for i in range(item.childCount()):
                child_item = item.child(i)
                child_checkbox = self.settings_dialog.folder_tree.itemWidget(child_item, 0)
                child_checkbox.setChecked(False)

    def save_current_settings_as_template(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "保存模板文件", "", "Template Files (*.template)")
        if file_path:
            template_data = (os.path.basename(file_path), self.target_paths, self.naming_rules, self.include_subfolders)
            with open(file_path, 'wb') as f:
                pickle.dump(template_data, f)
            self.templates.append(template_data)
            self.log_message(f"模板已保存: {file_path}")
            QMessageBox.information(None, "提示", "模板保存成功")

    def show_template_menu(self):
        template_menu = QMenu('模板操作', self.menu)
        load_template_action = template_menu.addAction('读取模板')
        save_template_action = template_menu.addAction('保存模板')
        new_template_action = template_menu.addAction('新建模板')
        template_menu.addSeparator()
        close_template_menu_action = template_menu.addAction('关闭')

        load_template_action.triggered.connect(self.load_template)
        save_template_action.triggered.connect(self.save_template)
        new_template_action.triggered.connect(self.new_template)
        close_template_menu_action.triggered.connect(template_menu.close)

        self.menu.addMenu(template_menu)

    def load_template(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "选择模板文件", "", "Template Files (*.template)")
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    template_data = pickle.load(f)
                    self.templates.append(template_data)
                    self.log_message(f"模板已加载: {file_path}")
                    QMessageBox.information(None, "提示", "模板读取成功")
            except FileNotFoundError:
                self.log_message("指定的模板文件不存在，请检查文件路径是否正确")
                QMessageBox.warning(None, "提示", "指定的模板文件不存在，请检查文件路径是否正确")
            except pickle.UnpicklingError:
                self.log_message("模板文件格式有误，无法正确解析，请检查文件内容")
                QMessageBox.warning(None, "提示", "模板文件格式有误，无法正确解析，请检查文件内容")

    def save_template(self):
        if not self.template_path:
            file_path, _ = QFileDialog.getSaveFileName(None, "保存模板文件", "", "Template Files (*.template)")
        if file_path:
            self.template_path = file_path
            template_data = (os.path.basename(self.template_path), self.target_paths, self.naming_rules, self.include_subfolders)
            with open(self.template_path, 'wb') as f:
                pickle.dump(template_data, f)
            self.templates.append(template_data)
            self.log_message(f"模板已保存: {file_path}")
            QMessageBox.information(None, "提示", "模板保存成功")

    def new_template(self):
        new_rule, ok = QInputDialog.getText(None, '新建模板', '请输入新的命名规则')
        if ok and new_rule:
            new_path, ok = QInputDialog.getText(None, '新建模板', '请输入要监控的文件夹路径')
            if ok and new_path:
                if not os.path.exists(new_path):
                    self.log_message("输入的文件夹路径不存在，请重新输入")
                    QMessageBox.warning(None, "提示", "输入的文件夹路径不存在，请重新输入")
                    return
                file_path, _ = QFileDialog.getSaveFileName(None, "保存新建模板文件", "", "Template Files (*.template)")
                if file_path:
                    template_data = (os.path.basename(file_path), [new_path], {new_path: new_rule}, {new_path: True})
                    with open(file_path, 'wb') as f:
                        pickle.dump(template_data, f)
                    self.templates.append(template_data)
                    self.log_message(f"新建模板已保存: {file_path}")
                    QMessageBox.information(None, "提示", "新建模板保存成功")

    def load_templates(self):
        try:
            with open('templates.template', 'rb') as f:
                self.templates = pickle.load(f)
        except FileNotFoundError:
            self.templates = []

    def exit_app(self):
        self.stop_auto_naming()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        with open('templates.template', 'wb') as f:
            pickle.dump(self.templates, f)
        self.save_log_history()  # 退出时保存日志
        self.save_last_settings()  # 退出时保存当前设置
        self.app.quit()

    def show_start_monitor_notification(self):
        QMessageBox.information(None, '通知', '监控已启动')


class CustomDialog(QDialog):
    def __init__(self, parent_widget=None):
        super().__init__()
        self.parent_widget = parent_widget  # 保存父窗口的引用
        self.last_modified_time = 0  # 记录文件最后修改时间
        self.folder_tree = None  # 初始化 folder_tree 属性

    def load_log_history(self):
        """从文件加载日志历史并显示到表格中"""
        if os.path.exists('log_history.txt'):
            current_modified_time = os.path.getmtime('log_history.txt')
            if current_modified_time != self.last_modified_time:  # 仅在文件发生变化时读取
                self.last_modified_time = current_modified_time
                with open('log_history.txt', 'r', encoding='utf-8') as f:
                    log_content = f.read().splitlines()
                    self.parent_widget.log_table.setRowCount(len(log_content))
                    for row, log_entry in enumerate(log_content):
                        parts = log_entry.split(' - ')
                        if len(parts) >= 2:
                            timestamp, message = parts[0], parts[1]
                            self.parent_widget.log_table.setItem(row, 0, QTableWidgetItem(timestamp))
                            self.parent_widget.log_table.setItem(row, 1, QTableWidgetItem(message))

    def update_log_display(self, log_entry):
        """更新日志显示"""
        parts = log_entry.split(' - ')
        if len(parts) >= 2:
            row = self.parent_widget.log_table.rowCount()
            self.parent_widget.log_table.insertRow(row)
            self.parent_widget.log_table.setItem(row, 0, QTableWidgetItem(parts[0]))
            self.parent_widget.log_table.setItem(row, 1, QTableWidgetItem(parts[1]))

    def closeEvent(self, event):
        self.hide()
        event.ignore()


if __name__ == "__main__":
    app = TrayApp()
    sys.exit(app.app.exec_())