#4.26更新：
#1. 重构任务列表管理功能-任务列表中直接操作及右键显示参数详情功能
#2. 依赖库-ADB工具自动安装功能
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
from PyQt5.QtWidgets import QMenu
from 依赖库.ADB工具自动安装 import ADBInstaller


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
        try:
            adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8').strip()
            adb_installed = True
            adb_version = adb_version_output.splitlines()[0]
        except subprocess.CalledProcessError:
            installer = ADBInstaller()
            installer.offer_installation()
            return None

        # 获取连接的设备列表
        devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip()
        devices_lines = devices_output.splitlines()[1:]  # 忽略首行的提示信息

        if not devices_lines:
            QMessageBox.warning(None, "设备连接问题", "未检测到已连接的设备或设备状态不正确。")
            return None  # 返回None或相应的值，表示没有找到设备

        if "device" not in devices_lines[0]:
            QMessageBox.warning(None, "设备连接问题", "设备可能未完全连接或未授权调试。")
            return None  # 返回None或相应的值，表示设备未授权

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
        self.setWindowTitle('定时ADB任务管理器')
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
        to_main_btn = QPushButton('返回主界面')
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
        self.task_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.task_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 对后台执行复选框列进行大小调整
        self.task_list.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.task_list.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.task_list.setColumnWidth(2, 150)   # 设置任务执行时间列的宽度 
        self.task_list.setColumnWidth(0, 100)    # 设置周期类型列的宽度   
        self.task_list.setColumnWidth(3, 100)    # 设置参数组名列的宽度       
        self.task_list.setContextMenuPolicy(Qt.CustomContextMenu)



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
        to_config_btn = QPushButton('参数组管理界面')
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
                self.update_all_param_combos()  # 更新任务列表中所有行的参数组名下拉菜单
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
        self.update_all_param_combos()  # 更新任务列表中所有行的参数组名下拉菜单


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
            self.update_all_param_combos()  # 更新任务列表中所有行的参数组名下拉菜单

    def delete_current_param(self):
        current_key = self.param_combo.currentText().split(' - ')[0]
        if current_key:
            self.delete_parameter_group(current_key)
            self.update_param_combo()  # 更新配置界面下拉列表
            self.update_main_param_combo()  # 更新主界面下拉列表
            self.update_all_param_combos()  # 更新任务列表中所有行的参数组名下拉菜单

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
        row_count = self.task_list.rowCount()
        
        # 格式化任务执行时间为 "YYYY-MM-DD HH:MM" 格式
        task_time_str = task_time.strftime("%Y-%m-%d %H:%M")

        # 遍历现有任务，检查是否存在相同执行时间的任务
        for i in range(row_count):
            datetime_editor = self.task_list.cellWidget(i, 2)
            if datetime_editor and datetime_editor.dateTime().toString("yyyy-MM-dd HH:mm") == task_time_str:
                QMessageBox.warning(self, "错误", "已存在相同执行时间的任务，请选择其他时间。")
                return  # 如果找到相同执行时间的任务，则不添加新任务并返回

        # 没有找到相同执行时间的任务，可以添加新任务
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

        # 周期类型下拉框
        cycle_combo = QComboBox()
        cycle_combo.addItems(["单次执行", "每日", "每周", "每月"])
        cycle_combo.setCurrentText(cycle_type)  # 设置当前选中的周期类型
        cycle_combo.currentTextChanged.connect(lambda new_cycle, id=task_id: self.update_cycle_type(id, new_cycle))
        self.task_list.setCellWidget(row_count, 0, cycle_combo)

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

        # 任务时间编辑器，显示格式根据周期类型调整
        datetime_editor = QDateTimeEdit(task_time)
        if cycle_type == "单次执行":
            datetime_editor.setDisplayFormat("yyyy-MM-dd HH:mm")
        else:
            # 对于周期性任务，仅显示时间（不显示日期）
            datetime_editor.setDisplayFormat("HH:mm")
        datetime_editor.setCalendarPopup(True)
        self.task_list.setCellWidget(row_count, 2, datetime_editor)
        datetime_editor.dateTimeChanged.connect(lambda new_time, id=task_id: self.update_task_time(id, new_time))

        # 参数组名下拉菜单
        param_combo = QComboBox()
        param_combo.setContextMenuPolicy(Qt.CustomContextMenu)
        param_combo.customContextMenuRequested.connect(lambda point, combo=param_combo: self.param_combo_context_menu(point, combo))
        saved_params = self.load_saved_parameters()  # 加载已保存的参数组
        for key in saved_params.keys():
            param_combo.addItem(key)
        param_combo.setCurrentText(param_group)  # 设置当前选中的参数组
        param_combo.currentTextChanged.connect(lambda new_group, tid=task_id: self.update_param_group(tid, new_group))
        self.task_list.setCellWidget(row_count, 3, param_combo)

        # 操作列：添加删除按钮
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(Qt.AlignCenter)
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
    #更新任务时间
    def update_task_time(self, task_id, new_time):
        """ 更新任务的执行时间 """
        if task_id in self.task_details:
            task_details = self.task_details[task_id]
            task_details['execute_time'] = new_time.toPyDateTime()
            print(f"任务 {task_id} 的执行时间已更新为 {new_time.toString()}")

            # 计算延迟时间
            current_datetime = datetime.now()
            delay = int((new_time.toPyDateTime() - current_datetime).total_seconds() * 1000)
            
            if delay < 0:
                print(f"任务 {task_id} 的设定时间已过，将立即结束任务。")
                self.finish_task(task_id)
            else:
                # 重新设置定时器
                timer = self.timers.get(task_id)
                if timer:
                    timer.stop()
                    timer.start(delay)
                    print(f"任务 {task_id} 的定时器已更新，将在 {delay} 毫秒后执行。")
        else:
            print(f"未找到任务ID：{task_id}")

    def update_cycle_type(self, task_id, new_cycle):
        task_details = self.task_details.get(task_id)
        if task_details:
            task_details['cycle_type'] = new_cycle
            datetime_editor = self.task_list.cellWidget(task_details['row_index'], 2)
            if datetime_editor:
                # 根据新的周期类型调整日期时间编辑器的显示格式
                if new_cycle == "单次执行":
                    datetime_editor.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
                else:
                    datetime_editor.setDisplayFormat("HH:mm:ss")
                print(f"任务 {task_id} 的周期类型已更新为 {new_cycle}.")
        else:
            print(f"未找到任务ID：{task_id}")
    
    def update_param_group(self, task_id, new_group):
        """ 更新任务的参数组名 """
        if task_id in self.task_details:
            self.task_details[task_id]['param_group'] = new_group
            print(f"任务 {task_id} 的参数组已更新为 {new_group}")
    
    def update_all_param_combos(self):
        row_count = self.task_list.rowCount()
        saved_params = self.load_saved_parameters()  # 加载已保存的参数组
        for i in range(row_count):
            param_combo = self.task_list.cellWidget(i, 3)  # 假设参数组名下拉菜单在第四列
            if param_combo:
                current_param = param_combo.currentText()
                param_combo.clear()
                for key in saved_params.keys():
                    param_combo.addItem(key)
                if current_param in saved_params:
                    param_combo.setCurrentText(current_param)  # 重新设置之前选中的参数组
    def param_combo_context_menu(self, point, combo):
        menu = QMenu()
        view_details_action = menu.addAction("查看参数组详情")
        action = menu.exec_(combo.mapToGlobal(point))
        if action == view_details_action:
            self.show_param_details(combo.currentText())





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
        QTimer.singleShot(70000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_HOME"))
        QTimer.singleShot(80000, lambda: self.adb_command(device_id, "input keyevent KEYCODE_WAKEUP"))

        # 对于非周期性任务，执行完毕后移除任务
        if cycle_type == "单次执行":
            QTimer.singleShot(14000, lambda: self.finish_task(task_id))
        else:
            print(f"Periodic task {task_id} completed an execution, waiting for the next trigger.")








    



    


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
        adb_info = get_adb_info()  # 调用 get_adb_info 并接收返回值
        if adb_info is None:
            # 如果 get_adb_info 返回 None，则说明检测过程中出现了问题，弹出错误提示
            QMessageBox.warning(self, "错误", "无法获取ADB设备信息，请检查设备连接和ADB设置。")
            return None  # 可选择返回 None 或进行其他适当的错误处理

        # 如果返回有效的结果，则解包
        self.device_id, self.package_name, self.activity_name, self.android_version, self.adb_installed, self.adb_version = adb_info

        self.update_params_list()  # 更新参数列表

        return {
            "device_id": self.device_id,
            "package_name": self.package_name,
            "activity_name": self.activity_name,
            "android_version": self.android_version,
            "adb_installed": self.adb_installed,
            "adb_version": self.adb_version
        }

        
#主函数
def main():
    app = QApplication(sys.argv)
    adb_control_app = ADBControlApp()
    adb_control_app.show()
    app.exec_()

if __name__ == '__main__':
    main()
