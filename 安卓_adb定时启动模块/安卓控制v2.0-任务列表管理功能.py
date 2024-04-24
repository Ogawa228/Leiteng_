import os
import pickle
import uuid
import subprocess
import sys
import time
from datetime import datetime

from PyQt5.QtCore import QDateTime, QSize, QTimer, Qt  # 核心功能，包括时间、尺寸和计时器
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDateTimeEdit,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QInputDialog)  # GUI组件
from PyQt5.QtGui import QIcon  # 图标
from PyQt5.QtWidgets import QComboBox  # 下拉列表
from 依赖库.参数.参数详情 import ParameterDetailsViewer
from PyQt5.QtWidgets import QDialog, QFormLayout, QPushButton, QTimeEdit

#自动检测ADB参数
def get_adb_info():
    adb_installed = False
    adb_version = ""
    device_id = ""
    package_name = "未检测到"
    activity_name = "未检测到"
    android_version = ""

    try:
        # 检查ADB是否安装，并获取ADB版本
        adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8').strip()
        adb_installed = True
        adb_version = adb_version_output.splitlines()[0]  # 通常是第一行输出

        # 获取连接的设备列表
        devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip()
        devices_lines = devices_output.splitlines()[1:]  # 忽略首行的提示信息

        if not devices_lines:
            raise Exception("未检测到已连接的设备或设备状态不正确。")

        if "device" not in devices_lines[0]:
            raise Exception("设备可能未完全连接或未授权调试。")

        device_id = devices_lines[0].split()[0]  # 获取第一个设备ID

        # 检查设备是否休眠
        device_state = subprocess.check_output(["adb", "-s", device_id, "shell", "dumpsys", "power"], encoding='utf-8').strip()
        if "mWakefulness=Awake" not in device_state:
            # 设备休眠中，发送唤醒命令
            subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_WAKEUP"])
            subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_MENU"])
            time.sleep(1)  # 等待设备唤醒

        # 获取设备的Android版本
        android_version = subprocess.check_output(["adb", "-s", device_id, "shell", "getprop", "ro.build.version.release"], encoding='utf-8').strip()

        # 获取当前前台活动的包名和活动名
        package_name, activity_name = get_foreground_activity(device_id)
        if package_name is None:
            raise Exception("无法检测到前台活动。请确保有应用在前台运行。")

    except subprocess.CalledProcessError as e:
        print("执行ADB命令出错:", e)
    except Exception as e:
        print("错误:", e)

    return device_id, package_name, activity_name, android_version, adb_installed, adb_version

def get_foreground_activity(device_id):
    try:
        dumpsys_output = subprocess.check_output(["adb", "-s", device_id, "shell", "dumpsys", "activity", "activities"], encoding='utf-8')
        for line in dumpsys_output.splitlines():
            if "mResumedActivity" in line:
                activity_info = line.split()[-2]
                package_name, activity_name = activity_info.split("/")
                return package_name, activity_name
    except subprocess.CalledProcessError:
        return None, None  # 返回空的元组如果发生错误

class ADBControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.device_id = "0123456789ABCDEF"
        self.package_name = "com.ss.android.lark"
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"
        self.android_version = "Android 10"
        self.adb_installed = False
        self.adb_version = "Version 1.0.41"
        self.timers = {}
        self.timer_to_task = {}
        self.init_ui()
        self.command_log = []
        self.task_details = {}  # 初始化 task_details 字典


        self.resize(600, 450)  # 设置窗口初始大小

    
    def init_ui(self):
        self.setWindowTitle('ADB控制器')
        self.stack_widget = QStackedWidget(self)

        # 创建配置界面
        config_layout = QVBoxLayout()

        # 参数组选择和操作功能的组合
        param_combo_layout = QHBoxLayout()
        self.param_combo = QComboBox()  # 配置界面的下拉列表
        param_combo_layout.addWidget(self.param_combo)

        delete_button = QPushButton('删除')
        delete_button.clicked.connect(self.delete_current_param)
        param_combo_layout.addWidget(delete_button)

        config_layout.addLayout(param_combo_layout)

        # 添加显示详情按钮
        show_details_button = QPushButton('显示详情')
        show_details_button.clicked.connect(self.show_parameters_details)
        param_combo_layout.addWidget(show_details_button)

        config_layout.addLayout(param_combo_layout)

        # 新建参数组按钮
        new_param_button = QPushButton('新建参数组')
        new_param_button.clicked.connect(self.new_param_group)
        config_layout.addWidget(new_param_button)

        # 自动检测ADB参数按钮
        detect_adb_btn = QPushButton('自动检测ADB参数')
        detect_adb_btn.clicked.connect(self.detect_adb_parameters)
        config_layout.addWidget(detect_adb_btn)

        # 保存ADB参数按钮
        save_params_btn = QPushButton('保存或更新参数组')
        save_params_btn.clicked.connect(self.prompt_save_parameters)
        config_layout.addWidget(save_params_btn)

        # 参数显示文本框
        self.params_list = QListWidget()
        config_layout.addWidget(self.params_list)

        # 切换到主界面的按钮
        to_main_btn = QPushButton('切换到主界面')
        to_main_btn.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        config_layout.addWidget(to_main_btn)

        config_widget = QWidget()
        config_widget.setLayout(config_layout)
        self.stack_widget.addWidget(config_widget)  # 添加配置界面到stack widget

        # 创建主界面
        main_layout = QVBoxLayout()
        self.task_list = QTableWidget(0, 5)  # 五列：周期类型、后台执行、任务执行时间、参数组名、操作
        self.task_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.task_list.setHorizontalHeaderLabels(["周期类型", "后台执行", "任务执行时间", "参数组名", "操作"])
        self.task_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 对后台执行复选框列进行大小调整
        self.task_list.cellClicked.connect(self.cell_was_clicked)
        self.task_list.setDragDropMode(QAbstractItemView.InternalMove)
        main_layout.addWidget(self.task_list)

        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        main_layout.addWidget(self.date_time_edit)

        self.cycle_combo = QComboBox()
        self.cycle_combo.addItem("单次执行")
        self.cycle_combo.addItem("每日")
        self.cycle_combo.addItem("每周")
        self.cycle_combo.addItem("每月")
        main_layout.addWidget(QLabel("选择执行周期:"))
        main_layout.addWidget(self.cycle_combo)

        main_layout.addWidget(QLabel("选择参数组:"))
        self.main_param_combo = QComboBox()  # 主界面的下拉列表
        main_layout.addWidget(self.main_param_combo)

        confirm_time_btn = QPushButton('执行')
        confirm_time_btn.clicked.connect(self.confirm_time)
        main_layout.addWidget(confirm_time_btn)

        # 切换到配置界面的按钮
        to_config_btn = QPushButton('切换到配置界面')
        to_config_btn.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        main_layout.addWidget(to_config_btn)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.stack_widget.addWidget(main_widget)  # 添加主界面到stack widget

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack_widget)
        self.setLayout(layout)

        # 保证先实例化 main_param_combo 后调用更新函数
        self.update_param_combo()
        self.update_main_param_combo()

        self.stack_widget.setCurrentIndex(1)  # 默认显示主界面





 




#参数组功能
    def prompt_save_parameters(self):
        group_name = self.param_combo.currentText().split(' - ')[0] if self.param_combo.currentText() else None
        if group_name:
            params = self.detect_adb_parameters()  # 获取自动检测到的ADB参数，现在包括执行的命令
            if params:
                self.save_parameters_to_file(params, group_name)  # 保存或更新参数组
                self.update_param_combo()  # 更新配置界面下拉列表
                self.update_main_param_combo()  # 更新主界面下拉列表
                self.command_log.clear()
            else:
                QMessageBox.warning(self, "ADB参数未检测到", "未检测到ADB参数，请确保ADB已正确安装并连接设备。")
        else:
            QMessageBox.warning(self, "操作错误", "请选择一个参数组。")

        

    def save_parameters_to_file(self, params, group_name, file_name='用户配置信息.pkl'):
        data = self.load_saved_parameters(file_name)
        if group_name in data:
            response = QMessageBox.question(self, "确认覆盖", f"参数组 '{group_name}' 已存在。是否覆盖？", QMessageBox.Yes | QMessageBox.No)
            if response == QMessageBox.No:
                return
        params['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Update save time
        data[group_name] = params
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        QMessageBox.information(self, "保存成功", f"参数组 '{group_name}' 已保存。")
        self.update_param_combo()  # 更新配置界面下拉列表的数据
        self.update_main_param_combo()  # 更新主界面下拉列表的数据


    def update_param_combo(self):
        self.param_combo.clear()
        saved_params = self.load_saved_parameters()
        for key, value in saved_params.items():
            self.param_combo.addItem(f"{key} - 保存于: {value.get('save_time', 'Unknown')}")
        self.update_main_param_combo()  # 确保更新主界面下拉列表

    def new_param_group(self):
        text, ok = QInputDialog.getText(self, '新建参数组', '请输入新的参数组名称:')
        if ok and text:
            self.save_parameters_to_file({}, text)  # 保存新的参数组
            self.update_param_combo()  # 更新配置界面下拉列表
            self.update_main_param_combo()  # 更新主界面下拉列表

    def delete_current_param(self):
        current_key = self.param_combo.currentText().split(' - ')[0]
        if current_key:
            self.delete_parameter_group(current_key)
            self.update_param_combo()  # 更新配置界面下拉列表
            self.update_main_param_combo()  # 更新主界面下拉列表

    def update_main_param_combo(self):
        # 清除主界面下拉列表的既有内容
        self.main_param_combo.clear()
        # 重新加载配置信息
        saved_params = self.load_saved_parameters()
        for key, value in saved_params.items():
            self.main_param_combo.addItem(f"{key} - 保存于: {value.get('save_time', 'Unknown')}")


    def load_saved_parameters(self, file_name='用户配置信息.pkl'):
        try:
            if os.path.exists(file_name):
                with open(file_name, 'rb') as f:
                    return pickle.load(f)
            else:
                print("配置文件不存在，无法加载参数。")
        except Exception as e:
            print(f"加载配置文件时出错: {e}")
        return {}

    def delete_parameter_group(self, group_name, file_name='用户配置信息.pkl'):
            try:
                if os.path.exists(file_name):
                    with open(file_name, 'rb') as f:
                        data = pickle.load(f)
                    if group_name in data:
                        del data[group_name]
                        with open(file_name, 'wb') as f:
                            pickle.dump(data, f)
                        QMessageBox.information(self, "成功", "参数组已删除。")
            except Exception as e:
                QMessageBox.warning(self, "删除失败", f"删除参数组失败: {e}")

    def show_parameters_dialog(self):
        data = self.load_saved_parameters('用户配置信息.pkl')
        items = [f"{key} ({value['save_time']})" for key, value in data.items()]
        item, ok = QInputDialog.getItem(self, "选择参数组", "选择一个参数组:", items, 0, False)
        if ok and item:
            selected_key = item.split(' (')[0]  # Remove timestamp
            params = data[selected_key]
            self.device_id = params['device_id']
            self.package_name = params['package_name']
            self.activity_name = params['activity_name']
            self.android_version = params['android_version']
            self.adb_installed = params.get('adb_installed', False)
            self.adb_version = params.get('adb_version', '')
            self.update_params_list()
    
    def cell_was_clicked(self, row, column):
        # 当单元格被点击时执行
        if column == 3:  # 假设参数组名在第三列
            param_group = self.task_list.item(row, column).text().split(' - ')[0]
            self.show_param_details(param_group)
    
    def show_parameters_details(self):
        selected_key = self.param_combo.currentText().split(' - ')[0]
        if selected_key:
            # Open the parameter details viewer dialog
            viewer = ParameterDetailsViewer(self, selected_key)
            viewer.exec_()
        else:
            QMessageBox.warning(self, "选择错误", "请先选择一个参数组。")


    def show_param_details(self, param_group):
        if param_group:
            # Load the parameters to check if the group exists
            data = self.load_saved_parameters()
            if param_group in data:
                # Open the parameter details viewer dialog
                viewer = ParameterDetailsViewer(self, param_group)
                viewer.exec_()
            else:
                QMessageBox.warning(self, "参数组不存在", f"参数组 '{param_group}' 不存在。")
        else:
            QMessageBox.warning(self, "参数组不存在", "未指定参数组。")



 

#定时任务功能 
    def confirm_time(self):
        selected_datetime = self.date_time_edit.dateTime().toPyDateTime()
        current_datetime = datetime.now()
        delay = int((selected_datetime - current_datetime).total_seconds() * 1000)
        task_key = selected_datetime.strftime('%Y-%m-%d %H:%M')
        selected_param_group = self.main_param_combo.currentText().split(' - ')[0]
        cycle_type = self.cycle_combo.currentText()  # 获取选中的周期类型

        if delay < 0:
            QMessageBox.warning(self, "错误", "选择的时间已过，请选择未来的时间。")
            return

        # 转换 task_key 为 datetime 对象
        task_datetime = datetime.strptime(task_key, "%Y-%m-%d %H:%M")

        if cycle_type == "单次执行":
            if task_key in self.timers:
                QMessageBox.warning(self, "错误", "已存在相同时间的任务，请选择其他时间。")
                return
            self.add_task_to_list(task_datetime, delay, selected_param_group, cycle_type, first_run=True)
        else:
            # 周期性任务不检查重复
            self.add_task_to_list(task_datetime, delay, selected_param_group, cycle_type, first_run=True)



    def add_task_to_list(self, task_time, delay, param_group, cycle_type, first_run=False):
        row_count = self.task_list.rowCount()
        self.task_list.insertRow(row_count)
        
        # 为每个任务生成唯一标识符
        task_id = str(uuid.uuid4())
            # 存储任务详情以便后续引用
        self.task_details[task_id] = {
            'row_index': row_count,
            'timer': None,
            'checkbox': None,
            'cycle_type': cycle_type,
            'execute_time': task_time
        }

        # 周期类型标签
        cycle_label = QTableWidgetItem(cycle_type)
        cycle_label.setTextAlignment(Qt.AlignCenter)
        self.task_list.setItem(row_count, 0, cycle_label)

        # 后台执行复选框
        checkbox = QCheckBox()
        checkbox.setToolTip("勾选此复选框将任务设置为在后台运行")
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_widget.setLayout(checkbox_layout)
        self.task_list.setCellWidget(row_count, 1, checkbox_widget)

        # 根据周期类型调整显示时间格式
        if cycle_type == "单次执行":
            task_time_display = task_time.strftime("%Y-%m-%d %H:%M")
        else:
            # 对于周期性任务，仅显示时间（不显示日期）
            task_time_display = task_time.strftime("%H:%M")

        # 任务时间标签
        task_label = QTableWidgetItem(task_time_display)
        task_label.setTextAlignment(Qt.AlignCenter)
        self.task_list.setItem(row_count, 2, task_label)

        # 参数组名标签
        param_label = QTableWidgetItem(param_group)
        param_label.setTextAlignment(Qt.AlignCenter)
        self.task_list.setItem(row_count, 3, param_label)

        # 操作列：添加删除和管理按钮
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(Qt.AlignCenter)
        manage_btn = QPushButton('🔨')
                # 管理按钮样式
        manage_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)
        manage_btn.clicked.connect(lambda: self.manage_task(row_count))
        remove_btn = QPushButton('✕')
        # 删除按钮样式
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
            QPushButton:pressed {
                background-color: #cc0000;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_task(task_id))
        btn_layout.addWidget(manage_btn)
        btn_layout.addWidget(remove_btn)
        btn_widget.setLayout(btn_layout)
        self.task_list.setCellWidget(row_count, 4, btn_widget)

        # 创建并启动定时器
        timer = QTimer(self)
        if cycle_type != "单次执行" and first_run:
            timer.timeout.connect(lambda: self.schedule_next_run(task_id, delay, cycle_type))
        else:
            timer.timeout.connect(lambda: self.execute_commands(task_id))
        timer.start(delay)
        self.timers[task_id] = timer
        self.timer_to_task[task_id] = (row_count, timer, checkbox)







    

    def schedule_next_run(self, task_id, initial_delay, cycle_type):
        # 计算下一次执行的延迟时间
        delay = initial_delay
        if cycle_type == "每日":
            delay += 86400000  # 加一天的毫秒数
        elif cycle_type == "每周":
            delay += 604800000  # 加一周的毫秒数
        elif cycle_type == "每月":
            delay += 2592000000  # 加约一个月的毫秒数 (30天)

        # 重新设置定时器
        timer = self.timers.get(task_id)
        if timer:
            timer.start(delay)
            print(f"任务 {task_id} 已重新调度，将在 {delay} 毫秒后再次执行。")





#任务列表管理功能
    def remove_task(self, task_id):
        task_detail = self.task_details.get(task_id)
        if task_detail:
            row_index = task_detail['row_index']
            # 停止并删除定时器
            timer = self.timers.get(task_id)
            if timer:
                timer.stop()
                del self.timers[task_id]
            
            # 移除表格行
            self.task_list.removeRow(row_index)
            del self.task_details[task_id]

            # 更新后续任务的行索引
            for key, value in self.task_details.items():
                if value['row_index'] > row_index:
                    value['row_index'] -= 1
        else:
            print(f"无法找到任务ID：{task_id}")
    def finish_task(self, task_id):
        # 检查是否存在对应的任务ID
        if task_id in self.task_details:
            task_info = self.task_details[task_id]
            timer = self.timers.get(task_id)
            if timer:
                timer.stop()  # 停止任务对应的定时器
                del self.timers[task_id]  # 删除定时器引用

            # 移除任务列表中的对应行
            row_index = task_info['row_index']
            self.task_list.removeRow(row_index)
            del self.task_details[task_id]  # 从任务详细信息中删除任务

            # 更新后续任务的行索引
            for key, value in self.task_details.items():
                if value['row_index'] > row_index:
                    value['row_index'] -= 1

            # 显示任务完成的消息
            self.show_auto_close_message(f"任务 {task_id} 执行完毕并已从列表中移除。")
        else:
            print(f"无法找到任务ID：{task_id}")


    def show_auto_close_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("任务完成")
        msg.setText(message)
        msg.show()
        QTimer.singleShot(1000, msg.close)  # 设置定时器在1000毫秒（1秒）后关闭消息框   


    def manage_task(self, row):
        task_time_str = self.task_list.item(row, 2).text()  # 任务时间
        task_datetime = QDateTime.fromString(task_time_str, "yyyy-MM-dd HH:mm:ss")
        
        # 提取执行的ADB命令（假设任务的ADB命令存储在某处，这里我们从命令日志中获取最新命令）
        executed_commands = self.command_log[-1] if self.command_log else ""

        task_details = {
            'device_id': self.device_id,
            'package_name': self.package_name,
            'activity_name': self.activity_name,
            'execute_time': task_datetime,
            'cycle_type': self.cycle_combo.currentText(),
            'background': self.task_list.cellWidget(row, 1).findChild(QCheckBox).isChecked(),
            'adb_command': executed_commands  # 确保传递最后执行的ADB命令
        }
        
        dialog = TaskManagerDialog(self, task_details)
        if dialog.exec_():
            print("任务已更新")



#ADB命令组
    def adb_command(self, device_id, command):
        full_command = ["adb", "-s", device_id, "shell", command]
        try:
            subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.command_log.append(f"adb -s {device_id} shell {command}")  # Log the command
        except subprocess.CalledProcessError as e:
            print(f"执行ADB命令出错: {e}")


    def wake_up_device(self):
        # 确保在调用 adb_command 时传递 device_id 和具体的命令
        self.adb_command(self.device_id, "input keyevent KEYCODE_WAKEUP")

    def close_app(self):
        # 调用 adb_command 时传递 device_id 和命令
        self.adb_command(self.device_id, "input keyevent KEYCODE_HOME")

    def swipe_up(self):
        # 调用 adb_command 时传递 device_id 和命令
        self.adb_command(self.device_id, "input swipe 300 1000 300 500")


    def open_app(self, package_name, activity_name, device_id):
        # 构造应用启动命令
        command = f"am start -n {package_name}/{activity_name}"
        # 调用 adb_command 时传递 device_id 和命令
        self.adb_command(device_id, command)



    def get_params_from_group(self, group_name):
        data = self.load_saved_parameters()
        if group_name in data:
            params = data[group_name]
            package_name = params.get('package_name', '')
            activity_name = params.get('activity_name', '')
            device_id = params.get('device_id', '')
            print(f"成功获取参数：包名-{package_name}, 活动名-{activity_name}, 设备ID-{device_id}")
            return package_name, activity_name, device_id
        else:
            print(f"未找到名为'{group_name}'的参数组。")
            return '', '', ''

    def execute_commands(self, task_id):
        if task_id in self.timers:
            row_index, timer, checkbox = self.timer_to_task[task_id]
            selected_param_group = self.task_list.item(row_index, 3).text().split(' - ')[0]  # 从第四列获取参数组名
            package_name, activity_name, device_id = self.get_params_from_group(selected_param_group)
            cycle_type = self.task_list.item(row_index, 0).text()  # 假设周期类型在第一列

            if package_name and activity_name and device_id:
                if checkbox.isChecked():
                    self.hide()  # 隐藏窗口，不关闭程序
                    print(f"任务 {task_id} 将在后台运行.")
                else:
                    print(f"呼出应用程序并执行任务 {task_id}...")
                    self.show()

                # 延迟执行ADB命令序列
                QTimer.singleShot(2000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_WAKEUP"))
                QTimer.singleShot(4000, lambda: self.adb_command(device_id, "input swipe 300 1000 300 500"))
                QTimer.singleShot(6000, lambda: self.open_app(package_name, activity_name, device_id))
                QTimer.singleShot(10000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_HOME"))
                QTimer.singleShot(12000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_WAKEUP"))

                # 根据任务类型决定是否结束任务
                if cycle_type == "单次执行":
                    QTimer.singleShot(14000, lambda: self.finish_task(task_id))
                else:
                    print(f"周期任务 {task_id} 完成一次执行，等待下次触发。")
            else:
                print("未找到有效的包名、活动名或设备ID。")








    



                


#初始对话框
    def show_initial_dialog(self):
        info_msg = QMessageBox()
        info_msg.setIcon(QMessageBox.Information)
        info_msg.setWindowTitle("当前ADB配置")
        info_msg.setText(f"设备ID: {self.device_id}\n包名: {self.package_name}\n活动名: {self.activity_name}")
        info_msg.setInformativeText("您想要更改这些参数吗？")
        info_msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        response = info_msg.exec_()
        if response == QMessageBox.Yes:
            self.change_params_dialog()

    def change_params_dialog(self):
        guide_msg = QMessageBox()
        guide_msg.setIcon(QMessageBox.Information)
        guide_msg.setWindowTitle("如何获取参数")
        guide_msg.setText("您可以使用以下ADB命令来获取所需参数：\n"
                          "- 设备ID: adb devices\n"
                          "- 包名和活动名: adb shell dumpsys window | grep mCurrentFocus")
        guide_msg.exec_()
        self.device_id, ok = QInputDialog.getText(self, "输入新的设备ID", "设备ID:")
        if ok:
            self.package_name, ok = QInputDialog.getText(self, "输入新的包名", "包名:")
        if ok:
            self.activity_name, ok = QInputDialog.getText(self, "输入新的活动名", "活动名:")


#自动检测ADB参数
    def update_params_list(self):
        # 更新显示的参数列表
        self.params_list.clear()
        self.params_list.addItem(f"设备ID: {self.device_id}")
        self.params_list.addItem(f"包名: {self.package_name}")
        self.params_list.addItem(f"活动名: {self.activity_name}")
        self.params_list.addItem(f"Android版本: {self.android_version}")
        self.params_list.addItem(f"ADB已安装: {'是' if self.adb_installed else '否'}")
        self.params_list.addItem(f"ADB版本: {self.adb_version}")
    
    
    
    def detect_adb_parameters(self):
        device_id, package_name, activity_name, android_version, adb_installed, adb_version = get_adb_info()
        executed_commands = self.command_log  # Use the stored command log
        self.update_params_list()
        return {
            "device_id": device_id,
            "package_name": package_name,
            "activity_name": activity_name,
            "android_version": android_version,
            "adb_installed": adb_installed,
            "adb_version": adb_version,
            "executed_commands": executed_commands
        }




from PyQt5.QtCore import QTime

class TaskManagerDialog(QDialog):
    def __init__(self, parent, task_details):
        super().__init__(parent)
        self.task_details = task_details
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        self.setWindowTitle('任务管理')

        # 设备ID, 包名, 应用名
        self.device_id_edit = QLineEdit(self.task_details['device_id'])
        self.package_name_edit = QLineEdit(self.task_details['package_name'])
        self.activity_name_edit = QLineEdit(self.task_details['activity_name'])
        
        # 执行时间
        self.execute_time_edit = QDateTimeEdit(self.task_details['execute_time'])
        self.execute_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.execute_time_edit.setCalendarPopup(True)
        
        # 周期类型
        self.cycle_type_combo = QComboBox()
        self.cycle_type_combo.addItems(["单次执行", "每日", "每周", "每月"])
        self.cycle_type_combo.setCurrentText(self.task_details['cycle_type'])

        # 后台执行
        self.background_check = QCheckBox("后台执行")
        self.background_check.setChecked(self.task_details['background'])

        # ADB命令
        self.adb_command_edit = QLineEdit(self.task_details['adb_command'])

        # 添加控件到表单
        layout.addRow('设备ID:', self.device_id_edit)
        layout.addRow('包名:', self.package_name_edit)
        layout.addRow('应用名:', self.activity_name_edit)
        layout.addRow('执行时间:', self.execute_time_edit)
        layout.addRow('周期类型:', self.cycle_type_combo)
        layout.addRow('ADB命令:', self.adb_command_edit)
        layout.addRow(self.background_check)

        # 保存按钮
        save_button = QPushButton('保存更改')
        save_button.clicked.connect(self.save_changes)
        layout.addRow(save_button)

    def save_changes(self):
        # 这里实现保存逻辑
        print("更改已保存")
        self.accept()



#主函数
def main():
    app = QApplication(sys.argv)
    adb_control_app = ADBControlApp()
    adb_control_app.show()
    app.exec_()

if __name__ == '__main__':
    main()
