# 非自定义模块
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, 
    QGridLayout, QSizePolicy
)
import subprocess

# 引入自定义模块
from 获取初始参数_adb_命令 import get_adb_version, get_android_version, get_foreground_activity, get_foreground_activity_with_wakeup
from style_manager import StyleManager
from 对话框管理.加载参数按钮 import LoadParametersDialog
from 对话框管理.自动执行功能按钮 import AutoExecuteADBCommandDialog
from 对话框管理.保存按钮对话框 import SaveParameters




class ADBParametersDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADB参数配置")
        self.init_ui()  # 确保这一行存在
        StyleManager.applyStyle(self)  # 应用样式

    def init_ui(self):
        layout = QGridLayout()

        layout.addWidget(QLabel("设备ID:"), 0, 0)
        self.device_id_edit = QLineEdit()
        layout.addWidget(self.device_id_edit, 0, 1)

        layout.addWidget(QLabel("包名:"), 1, 0)
        self.package_name_edit = QLineEdit()
        layout.addWidget(self.package_name_edit, 1, 1)

        layout.addWidget(QLabel("活动名:"), 2, 0)
        self.activity_name_edit = QLineEdit()
        layout.addWidget(self.activity_name_edit, 2, 1)

        self.detect_adb_version_button = QPushButton("ADB版本信息")
        self.detect_adb_version_button.clicked.connect(self.show_adb_version)
        self.detect_adb_version_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.detect_adb_version_button, 3, 0)  # 注意这里的布局位置

        self.detect_android_version_button = QPushButton("检测Android版本信息")
        self.detect_android_version_button.clicked.connect(self.detect_android_version)
        self.detect_android_version_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.detect_android_version_button, 3, 1)

        self.auto_detect_button = QPushButton("自动检测ADB参数")
        self.auto_detect_button.clicked.connect(self.detect_adb_parameters)
        self.auto_detect_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.auto_detect_button, 4, 0)

        self.manual_guide_button = QPushButton("手动获取ADB参数指引")
        self.manual_guide_button.clicked.connect(self.show_manual_guide)
        self.manual_guide_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.manual_guide_button, 4, 1)

        self.save_params_button = QPushButton("保存参数", self)
        self.save_params_button.clicked.connect(self.openSaveParametersDialog)  # 修改这里
        self.save_params_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.save_params_button, 5, 0)

        self.load_params_button = QPushButton("加载参数", self)
        self.load_params_button.clicked.connect(self.show_load_dialog)
        layout.addWidget(self.load_params_button, 5, 1)

        self.autoExecuteADBButton = QPushButton("ADB命令自动执行", self)
        self.autoExecuteADBButton.clicked.connect(self.openAutoExecuteADBCommandDialog)
        layout.addWidget(self.autoExecuteADBButton, 6, 0)  # 假设放在第6行第1列
        
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        self.setLayout(layout)
        # Existing code...



    
    def show_manual_guide(self):
        guide_text = (
            "手动获取ADB参数指引：\n"
            "1. 设备ID：在命令行中输入 'adb devices'，设备ID将在命令输出中显示。\n"
            "2. 包名和活动名：在命令行中输入 'adb shell dumpsys activity activities | grep mResumedActivity'，"
            "应用的包名和活动名将在命令输出中显示。\n\n"
            "请确保您的设备已通过USB连接到计算机，并且已在开发者选项中启用了USB调试。"
        )
        QMessageBox.information(self, "手动获取ADB参数指引", guide_text)   

    def show_adb_version(self):
        # Call the function from adb_utils to get the ADB version
        adb_version_output = get_adb_version()
        adb_version_message = f"ADB版本信息:\n\n{adb_version_output}\n\n这是Android Debug Bridge (ADB)的版本信息，它是Android开发和调试的重要工具。"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("ADB版本信息")
        msg_box.setText(adb_version_message)
        msg_box.exec_()

    def detect_android_version(self):
        # Call the function from adb_utils to get the Android version
        android_version_output = get_android_version(self.device_id_edit.text())
        if android_version_output:
            QMessageBox.information(self, "Android版本信息", f"Android版本信息:\n\n{android_version_output}")
        else:
            QMessageBox.critical(self, "错误", "无法获取Android版本信息。请确保设备已连接并且ADB正在运行。")

    def detect_adb_parameters(self):
        # 检查ADB是否安装并可访问
        try:
            adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8')
            print("ADB Version:", adb_version_output)
        except FileNotFoundError:
            QMessageBox.critical(self, "ADB未找到", "请确保ADB已安装并且环境变量设置正确。")
            return

        # 尝试获取连接的设备列表
        try:
            devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip()
            devices_lines = devices_output.splitlines()[1:]  # 跳过 'List of devices attached' 行

            if devices_lines:
                device_id = devices_lines[0].split()[0]  # 取第一个设备
                self.device_id_edit.setText(device_id)

                # 使用新的函数获取ADB参数
                package_name, activity_name = get_foreground_activity_with_wakeup(device_id)
                if package_name and activity_name:
                    self.package_name_edit.setText(package_name)
                    self.activity_name_edit.setText(activity_name)
                else:
                    QMessageBox.warning(self, "活动名检测失败", "无法检测到前台活动。")
            else:
                QMessageBox.warning(self, "未检测到设备", "请连接设备并开启USB调试。")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "执行ADB命令出错", str(e))
    def get_foreground_activity(self, device_id):
        package_name, activity_name = get_foreground_activity(device_id)
        if package_name is not None and activity_name is not None:
            self.package_name_edit.setText(package_name)
            self.activity_name_edit.setText(activity_name)
        else:
            QMessageBox.warning(self, "活动名检测失败", "无法检测到前台活动。")
    
    def show_load_dialog(self):
        # 创建并显示加载参数对话框
        self.load_dialog = LoadParametersDialog(self)
        self.load_dialog.exec_()

    def openSaveParametersDialog(self):
        saveDialog = SaveParameters(self)
        saveDialog.exec_()

    def openAutoExecuteADBCommandDialog(self):
        dialog = AutoExecuteADBCommandDialog(self)
        dialog.exec_()   



