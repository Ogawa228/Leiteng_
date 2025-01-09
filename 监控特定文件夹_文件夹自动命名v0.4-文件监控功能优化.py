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
    QCheckBox, QSizePolicy, QShortcut, QWidget, QHBoxLayout, QKeySequenceEdit,
    QTextEdit
)
from PyQt5.QtGui import QIcon, QColor, QPalette, QKeySequence
from PyQt5.QtCore import (
    Qt, QTimer, pyqtSignal, QObject
)
from datetime import datetime

# 初始化日志记录
logging.basicConfig(filename='auto_naming.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')  # 添加encoding='utf-8'

# 用于清理文件名中的非法字符
def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

class MyHandler(FileSystemEventHandler):
    def __init__(self, target_path, naming_rule, log_callback):
        self.target_path = target_path
        self.naming_rule = naming_rule
        self.log_callback = log_callback
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
        self.target_path = r"C:\Users\Administrator\OneDrive\我的工作\雷腾律所mac\非诉业务\合同审核"
        self.naming_rule = "{date}-{file_name}"
        self.is_running = False
        self.template_path = ""
        self.templates = []
        self.startup_checkbox = QCheckBox('开机自动启动')
        self.log_history = []  # 全局日志记录
        self.load_templates()
        self.load_startup_status()
        self.load_log_history()  # 加载日志历史

        # 创建快捷键，绑定到主窗口
        self.start_shortcut = QShortcut(QKeySequence('F7'), self.main_window)
        self.start_shortcut.activated.connect(self.start_auto_naming)
        self.stop_shortcut = QShortcut(QKeySequence('F8'), self.main_window)
        self.stop_shortcut.activated.connect(self.stop_auto_naming)

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

        # 初始化 settings_dialog 为 None
        self.settings_dialog = None

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
        with open('log_history.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(self.log_history))

    def load_startup_status(self):
        """加载开机自启状态"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                 winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, "工作流自动化-文件重命名")
                if value:
                    self.startup_checkbox.setChecked(True)
                else:
                    self.startup_checkbox.setChecked(False)
            except FileNotFoundError:
                self.startup_checkbox.setChecked(False)
            winreg.CloseKey(key)
        except FileNotFoundError:
            self.startup_checkbox.setChecked(False)

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
            # 每次启动时创建一个新的 Observer 实例
            self.observer = Observer()
            event_handler = MyHandler(self.target_path, self.naming_rule, self.log_message)
            try:
                self.observer.schedule(event_handler, self.target_path, recursive=True)
                self.observer.start()
                self.is_running = True
                self.monitor_started.emit()
                self.log_message("监控已启动")
            except Exception as e:
                self.log_message(f"启动监控时出现错误: {e}")

    def stop_auto_naming(self):
        if not self.is_running:
            self.log_message("自动命名未运行，无需执行停止操作")
            return
        if self.is_running:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            self.log_message("监控已停止")

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # 单击
            self.show_settings_dialog()
        elif reason == QSystemTrayIcon.DoubleClick:  # 双击
            self.show_settings_dialog()

    def show_settings_dialog(self):
        if self.settings_dialog is None:
            self.settings_dialog = CustomDialog()
            self.apply_apple_style(self.settings_dialog)
            self.settings_dialog.setWindowTitle('设置')
            layout = QVBoxLayout()

            naming_rule_label = QLabel('命名规则:')
            naming_rule_tip = QLabel(
                '示例：年-月-日-原有文件名称，可使用{date}代表当前日期，{file_name}代表原文件名，如：{date}-{file_name}')
            self.naming_rule_combo = QComboBox()
            self.naming_rule_combo.addItems(['{date}-{file_name}', '{file_name}-{date}', '{date}_{file_name}'])
            self.naming_rule_combo.addItem('自定义')
            self.naming_rule_combo.currentIndexChanged.connect(self.handle_naming_rule_selection)

            self.custom_naming_rule_input = QInputDialog()
            self.custom_naming_rule_input.setLabelText('请输入自定义命名规则:')
            self.custom_naming_rule_input.setWindowTitle('自定义命名规则')
            self.custom_naming_rule_input.hide()

            folder_label = QLabel('监控文件夹:')
            self.folder_button = QPushButton('选择文件夹')
            self.folder_button.clicked.connect(self.select_folder)
            self.folder_path = self.target_path
            self.folder_display = QLabel(self.folder_path)

            layout.addWidget(self.startup_checkbox)
            self.startup_checkbox.stateChanged.connect(self.set_startup)

            # 开始监控快捷键相关布局调整
            start_shortcut_widget = QWidget()
            start_shortcut_layout = QHBoxLayout(start_shortcut_widget)
            start_shortcut_label = QLabel('开始监控快捷键: ')
            current_start_shortcut_text = self.start_shortcut.key().toString()
            self.current_start_shortcut_label = QLabel(current_start_shortcut_text)
            start_shortcut_set_button = QPushButton('设置')
            start_shortcut_set_button.clicked.connect(self.set_start_shortcut)
            self.start_key_sequence_edit = QKeySequenceEdit()
            start_shortcut_layout.addWidget(start_shortcut_label)
            start_shortcut_layout.addWidget(self.current_start_shortcut_label)
            start_shortcut_layout.addWidget(self.start_key_sequence_edit)
            start_shortcut_layout.addWidget(start_shortcut_set_button)

            # 结束监控快捷键相关布局调整
            stop_shortcut_widget = QWidget()
            stop_shortcut_layout = QHBoxLayout(stop_shortcut_widget)
            stop_shortcut_label = QLabel('结束监控快捷键: ')
            current_stop_shortcut_text = self.stop_shortcut.key().toString()
            self.current_stop_shortcut_label = QLabel(current_stop_shortcut_text)
            stop_shortcut_set_button = QPushButton('设置')
            stop_shortcut_set_button.clicked.connect(self.set_stop_shortcut)
            self.stop_key_sequence_edit = QKeySequenceEdit()
            stop_shortcut_layout.addWidget(stop_shortcut_label)
            stop_shortcut_layout.addWidget(self.current_stop_shortcut_label)
            stop_shortcut_layout.addWidget(self.stop_key_sequence_edit)
            stop_shortcut_layout.addWidget(stop_shortcut_set_button)

            confirm_button = QPushButton('确认')
            confirm_button.clicked.connect(self.confirm_settings)

            save_template_button = QPushButton('保存为模板')
            save_template_button.clicked.connect(self.save_current_settings_as_template)

            # 日志显示文本框
            self.log_textedit = QTextEdit()
            self.log_textedit.setReadOnly(True)
            layout.addWidget(self.log_textedit)

            layout.addWidget(naming_rule_label)
            layout.addWidget(naming_rule_tip)
            layout.addWidget(self.naming_rule_combo)
            layout.addWidget(self.custom_naming_rule_input)
            layout.addWidget(folder_label)
            layout.addWidget(self.folder_button)
            layout.addWidget(self.folder_display)
            layout.addWidget(self.startup_checkbox)
            layout.addWidget(start_shortcut_widget)
            layout.addWidget(stop_shortcut_widget)
            layout.addWidget(confirm_button)
            layout.addWidget(save_template_button)

            self.settings_dialog.setLayout(layout)
            self.settings_dialog.closeEvent = self.handle_dialog_close

            # 连接日志更新信号
            self.log_updated.connect(self.settings_dialog.update_log_display)

            # 设置定时器，定期刷新日志显示
            self.log_timer = QTimer()
            self.log_timer.timeout.connect(self.settings_dialog.load_log_history)
            self.log_timer.start(1000)  # 每1秒刷新一次

        # 更新日志显示
        self.settings_dialog.load_log_history()
        self.settings_dialog.show()

    def handle_dialog_close(self, event):
        self.settings_dialog.hide()
        event.ignore()

    def apply_apple_style(self, dialog):
        # 设置整体背景色为淡灰色，接近苹果风格的素雅背景
        palette = dialog.palette()
        palette.setColor(QPalette.Window, QColor(245, 245, 245))
        palette.setColor(QPalette.WindowText, QColor(50, 50, 50))
        dialog.setPalette(palette)

        # 对按钮应用苹果风格的样式，去掉明显边框，设置柔和的背景色和文本颜色
        style_sheet = """
            QPushButton {
                background-color: #f8f8f8;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: #323232;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
            QLabel {
                color: #323232;
            }
            QDialog {
                background-color: #f8f8f8;
            }
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 3px;
                background-color: #f8f8f8;
            }
            QKeySequenceEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 3px;
                background-color: #f8f8f8;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f8f8f8;
            }
        """
        dialog.setStyleSheet(style_sheet)

    def handle_naming_rule_selection(self, index):
        if index == self.naming_rule_combo.count() - 1:
            self.custom_naming_rule_input.show()
        else:
            self.custom_naming_rule_input.hide()

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(None, '选择监控文件夹', '')
        if folder_path:
            self.folder_path = folder_path
            self.folder_display.setText(folder_path)
            self.log_message(f"监控文件夹已更改为: {folder_path}")

    def confirm_settings(self):
        index = self.naming_rule_combo.currentIndex()
        if index == self.naming_rule_combo.count() - 1:
            ok, rule = self.custom_naming_rule_input.getText()
            if ok:
                self.naming_rule = rule
        else:
            self.naming_rule = self.naming_rule_combo.currentText()
        self.target_path = self.folder_path
        self.log_message(f"命名规则已设置为: {self.naming_rule}")
        QMessageBox.information(None, '提示', '设置已确认')
        try:
            self.start_auto_naming()
        except Exception as e:
            self.log_message(f"启动自动命名时出现错误: {e}")

    def save_current_settings_as_template(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "保存模板文件", "", "Template Files (*.template)")
        if file_path:
            template_data = (os.path.basename(file_path), self.folder_path, self.naming_rule)
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
            template_data = (os.path.basename(self.template_path), self.target_path, self.naming_rule)
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
                    template_data = (os.path.basename(file_path), new_path, new_rule)
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

    def set_start_shortcut(self):
        new_shortcut = self.start_key_sequence_edit.keySequence()
        self.start_shortcut.setKey(new_shortcut)
        self.current_start_shortcut_label.setText(new_shortcut.toString())
        self.log_message(f"开始监控快捷键已设置为: {new_shortcut.toString()}")

    def set_stop_shortcut(self):
        new_shortcut = self.stop_key_sequence_edit.keySequence()
        self.stop_shortcut.setKey(new_shortcut)
        self.current_stop_shortcut_label.setText(new_shortcut.toString())
        self.log_message(f"结束监控快捷键已设置为: {new_shortcut.toString()}")

    def exit_app(self):
        self.stop_auto_naming()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        with open('templates.template', 'wb') as f:
            pickle.dump(self.templates, f)
        self.save_log_history()  # 退出时保存日志
        self.app.quit()

    def show_start_monitor_notification(self):
        QMessageBox.information(None, '通知', '监控已启动')


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent if parent is not None else QApplication.activeWindow()
        self.last_modified_time = 0  # 记录文件最后修改时间

        # 日志显示文本框
        self.log_textedit = QTextEdit()
        self.log_textedit.setReadOnly(True)

    def load_log_history(self):
        """从文件加载日志历史并显示到文本框中"""
        if os.path.exists('log_history.txt'):
            current_modified_time = os.path.getmtime('log_history.txt')
            if current_modified_time != self.last_modified_time:  # 仅在文件发生变化时读取
                self.last_modified_time = current_modified_time
                with open('log_history.txt', 'r', encoding='utf-8') as f:
                    log_content = f.read()
                    self.log_textedit.setPlainText(log_content)

    def update_log_display(self, log_entry):
        """更新日志显示"""
        self.log_textedit.append(log_entry)  # 追加新的日志内容

    def closeEvent(self, event):
        self.hide()
        event.ignore()


if __name__ == "__main__":
    app = TrayApp()
    sys.exit(app.app.exec_())