from PyQt5.QtCore import QTimer
import subprocess
import sys
from  PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLineEdit, QPushButton, QHBoxLayout, QWidget
import json
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from datetime import datetime
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLineEdit, QPushButton, QHBoxLayout, QWidget, QComboBox, QLabel
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QUrl

class ADBCommandExecutor:
    def __init__(self, device_id, package_name, activity_name, back_to_main_ui, back_to_config_ui):
        self.device_id = device_id
        self.package_name = package_name
        self.activity_name = activity_name
        self.back_to_main_ui = back_to_main_ui
        self.back_to_config_ui = back_to_config_ui
        self.command_log = []
        self.adb_commands_list = []
        self.commands_file = "commands.txt"
        self.commands_data = {}
        self.command_group_combo = QComboBox()  # 提前初始化
        self.commands_list_widget = QListWidget()  # 提前初始化



#UI相关
    def create_commands_ui(self):
        layout = QVBoxLayout()

        # 命令组选择下拉菜单
        self.command_group_combo = QComboBox()
        self.command_group_combo.currentIndexChanged.connect(self.load_selected_command_group)
        layout.addWidget(QLabel("选择命令组:"))
        layout.addWidget(self.command_group_combo)

        self.load_commands()

        # 命令列表显示区域
        self.commands_list_widget = QListWidget()
        layout.addWidget(self.commands_list_widget)

        # 命令输入和添加区域
        command_input_layout = QHBoxLayout()
        self.command_input_line = QLineEdit()
        command_input_layout.addWidget(self.command_input_line)

        add_command_button = QPushButton('添加命令')
        add_command_button.clicked.connect(self.add_command_to_list)
        command_input_layout.addWidget(add_command_button)

        # 自动识别ADB命令按钮
        auto_detect_button = QPushButton('自动识别命令')
        auto_detect_button.clicked.connect(self.auto_detect_command)
        command_input_layout.addWidget(auto_detect_button)

        # ADB命令格式指引按钮
        format_help_button = QPushButton('命令格式指引')
        format_help_button.clicked.connect(self.show_command_format_help)
        command_input_layout.addWidget(format_help_button)

        layout.addLayout(command_input_layout)

        # 命令操作按钮区域
        command_action_layout = QHBoxLayout()
        save_command_button = QPushButton('保存命令组')
        save_command_button.clicked.connect(self.save_commands)
        command_action_layout.addWidget(save_command_button)

        new_command_button = QPushButton('新建命令组')
        new_command_button.clicked.connect(self.new_command_group)
        command_action_layout.addWidget(new_command_button)

        delete_command_button = QPushButton('删除命令组')
        delete_command_button.clicked.connect(self.delete_command_group)
        command_action_layout.addWidget(delete_command_button)

        layout.addLayout(command_action_layout)

        # 返回按钮区域
        navigation_layout = QHBoxLayout()
        back_to_main_button = QPushButton('返回主界面')
        back_to_config_button = QPushButton('返回配置界面')
        back_to_main_button.clicked.connect(self.back_to_main_ui)
        back_to_config_button.clicked.connect(self.back_to_config_ui)
        navigation_layout.addWidget(back_to_main_button)
        navigation_layout.addWidget(back_to_config_button)
        layout.addLayout(navigation_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.apply_apple_style(add_command_button)
        self.apply_apple_style(auto_detect_button)
        self.apply_apple_style(format_help_button)
        self.apply_apple_style(save_command_button)
        self.apply_apple_style(new_command_button)
        self.apply_apple_style(delete_command_button)
        self.apply_apple_style(back_to_main_button)
        self.apply_apple_style(back_to_config_button)
        return widget




    def add_command_to_list(self):
        command = self.command_input_line.text()
        if command:
            item = QListWidgetItem(command)
            item.setFlags(item.flags() | Qt.ItemIsEditable)  # 确保设置为可编辑
            self.commands_list_widget.addItem(item)
            self.command_input_line.clear()


#命令格式指引
    def show_command_format_help(self):
        dialog = QDialog()
        dialog.setWindowTitle("ADB命令格式指引")
        dialog.resize(800, 600)  # 设置对话框的大小

        # 创建一个Web视图
        web_view = QWebEngineView()
        web_view.load(QUrl("https://cloud.tencent.com/developer/article/2342099"))  # 加载网页

        layout = QVBoxLayout()
        layout.addWidget(web_view)  # 将网页视图添加到布局中

        dialog.setLayout(layout)  # 设置对话框的布局为刚才创建的布局
        dialog.exec_()  # 显示对话框


#设置和获取命令列表
    def set_commands(self, commands):
        """设置命令列表"""
        self.adb_commands_list = commands

    def get_commands(self):
        """获取命令列表"""
        return self.adb_commands_list


#自动识别命令
    def auto_detect_command(self):
        # 假设这个方法会通过某种机制（如监听设备操作）自动识别用户在设备上的操作并转换成ADB命令
        detected_command = "input text 'example'"
        self.commands_list_widget.addItem(detected_command)



#命令组保存、新建、查看详情相关功能
    def save_commands(self):
        # 获取命令组名
        group_name, ok = QInputDialog.getText(None, "Save Command Group", "Enter the name of the command group:")
        if ok and group_name:
            command_list = [self.commands_list_widget.item(i).text() for i in range(self.commands_list_widget.count())]
            try:
                # 读取现有的命令数据
                with open(self.commands_file, "r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {}
            except FileNotFoundError:
                data = {}

            # 添加或更新命令组
            data[group_name] = {
                "commands": command_list,
                "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # 写回文件
            with open(self.commands_file, "w") as file:
                json.dump(data, file, indent=4)

            QMessageBox.information(None, "Success", "Commands saved successfully.")

    def new_command_group(self):
        # 弹出对话框让用户输入新的命令组名称
        group_name, ok = QInputDialog.getText(None, "新建命令组", "请输入新命令组的名称:")
        if ok and group_name:
            if group_name in self.commands_data:
                QMessageBox.warning(None, "警告", "该命令组已存在。")
                return
            self.commands_list_widget.clear()
            self.commands_data[group_name] = {"commands": [], "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            self.command_group_combo.addItem(group_name)
            self.command_group_combo.setCurrentText(group_name)
            self.save_command_groups_to_file()

    def delete_command_group(self):
        group_name = self.command_group_combo.currentText()
        if group_name and QMessageBox.question(None, "确认删除", f"确定要删除命令组 '{group_name}' 吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            if group_name in self.commands_data:
                del self.commands_data[group_name]
                self.save_command_groups_to_file()
                self.command_group_combo.removeItem(self.command_group_combo.currentIndex())
                self.commands_list_widget.clear()


    def save_commands(self):
        # 获取当前选中的命令组名称
        group_name = self.command_group_combo.currentText()
        if not group_name:
            QMessageBox.warning(None, "Warning", "No command group selected.")
            return

        # 从命令列表中收集所有命令
        command_list = [self.commands_list_widget.item(i).text() for i in range(self.commands_list_widget.count())]
        
        # 更新或创建命令组信息
        if group_name in self.commands_data:
            # 更新现有命令组
            self.commands_data[group_name]['commands'] = command_list
            self.commands_data[group_name]['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            # 创建新命令组（正常情况下不应触发，除非下拉菜单与数据不同步）
            self.commands_data[group_name] = {
                "commands": command_list,
                "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # 保存命令组数据到文件
        self.save_command_groups_to_file()
        QMessageBox.information(None, "Success", "Commands saved successfully to the selected group.")

    def save_command_groups_to_file(self):
        """将当前所有命令组保存到文件"""
        with open(self.commands_file, 'w') as file:
            json.dump(self.commands_data, file, indent=4)

    def load_commands(self):
        try:
            with open(self.commands_file, 'r') as file:
                self.commands_data = json.load(file)
                self.command_group_combo.clear()
                for key, value in self.commands_data.items():
                    display_text = f"{key} (保存于: {value['save_time']})"
                    self.command_group_combo.addItem(display_text, key)  # 显示文本和实际值分开
        except (FileNotFoundError, json.JSONDecodeError):
            self.commands_data = {}



    def load_selected_command_group(self):
        index = self.command_group_combo.currentIndex()
        group_name = self.command_group_combo.itemData(index)
        if group_name:
            self.commands_list_widget.clear()
            commands = self.commands_data.get(group_name, {}).get('commands', [])
            for command in commands:
                item = QListWidgetItem(command)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.commands_list_widget.addItem(item)



        


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
