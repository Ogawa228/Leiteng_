
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
        self.task_list = QTableWidget(0, 6)  # 六列：周期类型、后台执行、任务执行时间、参数组名、操作、任务ID
        self.task_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.task_list.setHorizontalHeaderLabels(["周期类型", "后台执行", "任务执行时间", "参数组名", "操作", "任务ID"])
        self.task_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 对后台执行复选框列进行大小调整
        self.task_list.cellClicked.connect(self.cell_was_clicked)
        self.task_list.setDragDropMode(QAbstractItemView.InternalMove)
        main_layout.addWidget(self.task_list)

        # 隐藏任务ID列
        self.task_list.setColumnHidden(5, True)  # 隐藏第六列，索引为5

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

        # 应用样式
        self.apply_apple_style(delete_button)  
        self.apply_apple_style(new_param_button)
        self.apply_apple_style(detect_adb_btn)
        self.apply_apple_style(save_params_btn)
        self.apply_apple_style(show_details_button)
        self.apply_apple_style(to_main_btn)
        self.apply_apple_style(confirm_time_btn)
        self.apply_apple_style(to_config_btn)
    


        # 保证先实例化 main_param_combo 后调用更新函数
        self.update_param_combo()
        self.update_main_param_combo()

        self.stack_widget.setCurrentIndex(1)  # 默认显示主界面




#按钮样式
    def apply_apple_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 14px;
                font-family: 'Helvetica';
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
 




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
        cycle_type = self.cycle_combo.currentText()

        if delay < 0:
            QMessageBox.warning(self, "错误", "选择的时间已过，请选择未来的时间。")
            return

        task_datetime = datetime.strptime(task_key, "%Y-%m-%d %H:%M")

        if cycle_type == "单次执行":
            if task_key in self.timers:
                QMessageBox.warning(self, "错误", "已存在相同时间的任务，请选择其他时间。")
                return
            self.add_task_to_list(task_datetime, delay, selected_param_group, cycle_type, first_run=True)
        else:
            self.add_task_to_list(task_datetime, delay, selected_param_group, cycle_type, first_run=True)



    def add_task_to_list(self, task_time, delay, param_group, cycle_type, first_run=False):
        # 格式化任务执行时间为 "YYYY-MM-DD HH:MM" 格式
        task_time_str = task_time.strftime("%Y-%m-%d %H:%M")
        
        # 遍历现有任务，检查是否存在相同执行时间的任务
        for i in range(self.task_list.rowCount()):
            if self.task_list.item(i, 2).text() == task_time_str:
                QMessageBox.warning(self, "错误", "已存在相同执行时间的任务，请选择其他时间。")
                return  # 如果找到相同执行时间的任务，则不添加新任务并返回

        # 没有找到相同执行时间的任务，可以添加新任务
        row_count = self.task_list.rowCount()
        self.task_list.insertRow(row_count)

        # 生成任务 ID
        task_id = str(uuid.uuid4())

        # 存储任务详情
        self.task_details[task_id] = {
            'row_index': row_count,
            'timer': None,
            'checkbox': None,
            'cycle_type': cycle_type,
            'execute_time': task_time,
            'delay': delay,
            'param_group': param_group,
            'first_run': first_run
        }

        # 在表格中设置 task_id（假设为第 5 列，此列将设置为隐藏）
        task_id_item = QTableWidgetItem(task_id)
        self.task_list.setItem(row_count, 5, task_id_item)  # 第 5 列存储 task_id
        print(f"Task ID {task_id} set for row {row_count}")  # 调试输出
        self.task_list.setColumnHidden(5, True)  # 隐藏存储 task_id 的列

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
                border: none;
                padding: 5px 10px;
                border-radius: 11px;  /* 更圆润的边角 */
                font-size: 13 px;  /* 字体大小调整 */
                font-family: 'Helvetica';  /* 使用Helvetica字体，接近Apple的风格 */
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);  /* 添加简单的阴影效果 */
            }
            QPushButton:hover {
                background-color: #f0f0f0;  /* 鼠标悬停时的颜色，更柔和 */
            }
            QPushButton:pressed {
                background-color: #e0e0e0;  /* 鼠标按下时的颜色，更深 */
            }
        """)
        manage_btn.clicked.connect(lambda row=row_count: self.manage_task(row))
        remove_btn = QPushButton('✕')
        # 删除按钮样式
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 11px;  /* 更圆润的边角 */
                font-size: 12px;  /* 字体大小调整 */
                font-family: 'Helvetica';  /* 使用Helvetica字体，接近Apple的风格 */
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);  /* 添加简单的阴影效果 */
            }
            QPushButton:hover {
                background-color: #ff6666;  /* 鼠标悬停时的颜色，更柔和 */
            }
            QPushButton:pressed {
                background-color: #cc0000;  /* 鼠标按下时的颜色，更深 */
            }
        """)
        remove_btn.clicked.connect(lambda row=row_count, task_id=task_id: self.remove_task(task_id))
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
        print(f"Adding manage button for row {row_count} with task ID {task_id}")

    def remove_task(self, task_id):
        # 尝试从任务详情中获取与任务ID对应的行索引
        row_index_to_remove = None
        for task_id_key, task_info in self.task_details.items():
            if task_id_key == task_id:
                row_index_to_remove = task_info['row_index']
                break

        # 如果找到了对应的任务ID，执行删除操作
        if row_index_to_remove is not None:
            print(f"Attempting to remove task with ID: {task_id}")

            # 停止并删除定时器
            timer = self.timers.get(task_id)
            if timer:
                timer.stop()
                del self.timers[task_id]

            # 移除任务详情
            del self.task_details[task_id]

            # 移除表格行
            self.task_list.removeRow(row_index_to_remove)

            # 更新后续任务的行索引
            for task_id, task_info in self.task_details.items():
                if task_info['row_index'] > row_index_to_remove:
                    task_info['row_index'] -= 1

            self.show_auto_close_message(f"任务 {task_id} 已被移除。")
        else:
            print(f"无法找到任务ID：{task_id}")
    def finish_task(self, task_id):
        if task_id in self.timers:
            timer = self.timers[task_id]
            timer.stop()
            del self.timers[task_id]
            
            task_detail = self.task_details[task_id]
            del self.task_details[task_id]
            
            row_index = task_detail['row_index']
            self.task_list.removeRow(row_index)
            
            # 更新后续任务的行索引
            for key, value in self.task_details.items():
                if value['row_index'] > row_index:
                    value['row_index'] -= 1

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


    #周期执行函数
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


    def manage_task(self, row):
        if row >= 0 and row < self.task_list.rowCount():
            task_item = self.task_list.item(row, 5)
            if task_item is not None:
                task_id = task_item.text()
            # 提取执行的ADB命令（假设任务的ADB命令存储在某处，这里我们从命令日志中获取最新命令）
            executed_commands = self.command_log[-1] if self.command_log else ""

            task_details = {
                'device_id': self.device_id,
                'package_name': self.package_name,
                'activity_name': self.activity_name,
                'execute_time': self.task_list.item(row, 2).text(),  # 任务时间
                'cycle_type': self.cycle_combo.currentText(),
                'background': self.task_list.cellWidget(row, 1).findChild(QCheckBox).isChecked(),
                'adb_command': executed_commands  # 确保传递最后执行的ADB命令
            }
            
            
            dialog = TaskManagerDialog(self, task_details, task_id)
            if dialog.exec_():
                print("任务已更新")
        else:
            print(f"Error: Task ID not found for row {row}")
            QMessageBox.warning(self, "错误", "无法找到任务ID。")

    def update_task_detail(self, task_id, task_info):
            """更新或添加任务详情到字典中。"""
            self.task_details[task_id] = task_info
            print(f"Task {task_id} has been updated/added with info: {task_info}")




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
        if task_id not in self.timers:
            print(f"Error: Task ID {task_id} not found in timers.")
            return

        # 从 timers 获取任务的详细信息
        row_index, timer, checkbox = self.timer_to_task[task_id]
        task_detail = self.task_details.get(task_id)

        if not task_detail:
            print(f"Error: Task details not found for task ID {task_id}.")
            return

        # 直接从任务详情中获取参数组名、周期类型等信息
        param_group = task_detail.get('param_group')
        cycle_type = task_detail.get('cycle_type')

        # 获取选中的参数组的参数
        package_name, activity_name, device_id = self.get_params_from_group(param_group)
        if not (package_name and activity_name and device_id):
            print("Error: Failed to retrieve package name, activity name, or device ID.")
            return

        # 检查复选框是否选中，以决定是否在后台执行任务
        if checkbox.isChecked():
            self.hide()  # 隐藏窗口，不关闭程序
        else:
            self.show()  # 显示窗口

        # 延迟执行ADB命令序列
        QTimer.singleShot(2000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_WAKEUP"))
        QTimer.singleShot(4000, lambda: self.adb_command(device_id, "input swipe 300 1000 300 500"))
        QTimer.singleShot(6000, lambda: self.open_app(package_name, activity_name, device_id))
        QTimer.singleShot(10000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_HOME"))
        QTimer.singleShot(12000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_WAKEUP"))

        # 对于非周期性任务，执行完毕后移除任务
        if cycle_type == "单次执行":
            QTimer.singleShot(14000, lambda: self.finish_task(task_id))
        else:
            print(f"Periodic task {task_id} completed an execution, waiting for the next trigger.")








    



                


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
        self.device_id, self.package_name, self.activity_name, self.android_version, self.adb_installed, self.adb_version = get_adb_info()
        self.update_params_list()
        return {
            "device_id": self.device_id,
            "package_name": self.package_name,
            "activity_name": self.activity_name,
            "android_version": self.android_version,
            "adb_installed": self.adb_installed,
            "adb_version": self.adb_version
        }
        
       




from PyQt5.QtCore import QTime


class TaskManagerDialog(QDialog):
    def __init__(self, parent, task_details, task_id):
        super().__init__(parent)
        self.parent = parent  # 存储对父窗口的引用
        self.task_details = task_details
        self.task_id = task_id  # 存储 task_id

        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        self.setWindowTitle('任务管理')

        # 设备ID, 包名, 应用名
        self.device_id_edit = QLineEdit(self.task_details['device_id'])
        self.package_name_edit = QLineEdit(self.task_details['package_name'])
        self.activity_name_edit = QLineEdit(self.task_details['activity_name'])
        
        


         # 尝试从 task_details 获取 execute_time
        execute_time_str = self.task_details.get('execute_time', '')
        if execute_time_str:
            # 如果是字符串，尝试解析为 QDateTime 对象
            execute_time = QDateTime.fromString(execute_time_str, "yyyy-MM-dd HH:mm")
            if execute_time.isValid():
                self.execute_time_edit = QDateTimeEdit(execute_time)
            else:
                print("Error - Invalid QDateTime parsed from string")
                self.execute_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        else:
            self.execute_time_edit = QDateTimeEdit(QDateTime.currentDateTime())

        self.execute_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.execute_time_edit.setCalendarPopup(True)

        # 设置 QDateTimeEdit 控件
        self.execute_time_edit = QDateTimeEdit(execute_time)
        self.execute_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.execute_time_edit.setCalendarPopup(True)

        # 设置 QDateTimeEdit 控件
        self.execute_time_edit = QDateTimeEdit(execute_time)
        self.execute_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.execute_time_edit.setCalendarPopup(True)

        
        # 周期类型
        self.cycle_type_combo = QComboBox()
        self.cycle_type_combo.addItems(["单次执行", "每日", "每周", "每月"])
        self.cycle_type_combo.setCurrentText(self.task_details['cycle_type'])

        # 后台执行
        self.background_check = QCheckBox("后台执行")
        self.background_check.setChecked(self.task_details['background'])


        # 添加控件到表单
        layout.addRow('设备ID:', self.device_id_edit)
        layout.addRow('包名:', self.package_name_edit)
        layout.addRow('应用名:', self.activity_name_edit)
        layout.addRow('执行时间:', self.execute_time_edit)
        layout.addRow('周期类型:', self.cycle_type_combo)
        layout.addRow(self.background_check)


        #自动识别按钮
        auto_detect_app_btn = QPushButton('自动识别活动应用')
        auto_detect_app_btn.clicked.connect(self.detect_adb_parameters)
        layout.addRow(auto_detect_app_btn)


        # 保存按钮
        save_button = QPushButton('保存更改')
        save_button.clicked.connect(self.save_changes)
        layout.addRow(save_button)


        self.setLayout(layout)

    
    def detect_adb_parameters(self):
        # 调用 get_adb_info 并接收多个返回值
        self.device_id, self.package_name, self.activity_name, self.android_version, self.adb_installed, self.adb_version = get_adb_info()

        # 更新界面控件
        self.device_id_edit.setText(self.device_id)
        self.package_name_edit.setText(self.package_name)
        self.activity_name_edit.setText(self.activity_name)
    
    def save_changes(self):
        # 获取界面控件中的值
        device_id = self.device_id_edit.text()
        package_name = self.package_name_edit.text()
        activity_name = self.activity_name_edit.text()
        execute_time = self.execute_time_edit.dateTime().toPyDateTime()
        cycle_type = self.cycle_type_combo.currentText()
        background = self.background_check.isChecked()


        # 构建更新的任务详情字典
        updated_task_info = {
            'device_id': device_id,
            'package_name': package_name,
            'activity_name': activity_name,
            'execute_time': execute_time,
            'cycle_type': cycle_type,
            'background': background,
        }

        # 调用外部类（parent）的方法更新任务详情

        self.parent.update_task_detail(self.task_id, updated_task_info)

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
