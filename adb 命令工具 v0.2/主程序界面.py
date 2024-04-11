# 非自定义模块
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QSizePolicy, QStackedWidget)
import subprocess
from PyQt5.QtWidgets import QMessageBox

# 引入自定义模块
from 获取初始参数_adb_命令 import get_adb_version, get_android_version, get_foreground_activity, get_foreground_activity_with_wakeup
from style_manager import StyleManager
# 假设功能管理模块中的类已经被修改为继承自QWidget或QFrame
from 功能管理.加载参数按钮 import LoadParametersWidget
from 功能管理.自动执行功能按钮 import AutoExecuteADBCommandWidget
from 功能管理.保存按钮 import SaveParametersWidget

class ADBParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADB参数配置")
        StyleManager.applyStyle(self)
        self.init_ui()

    def init_ui(self):
        # 使用 QStackedWidget 来管理不同的功能界面
        self.stackedWidget = QStackedWidget(self)

        # 创建功能界面实例
        self.loadParametersPage = LoadParametersWidget(self)
        self.saveParametersPage = SaveParametersWidget(self)
        self.autoExecuteADBPage = AutoExecuteADBCommandWidget(self)

        # 将功能界面添加到 QStackedWidget
        self.stackedWidget.addWidget(self.loadParametersPage)
        self.stackedWidget.addWidget(self.saveParametersPage)
        self.stackedWidget.addWidget(self.autoExecuteADBPage)

        # 创建一个布局并添加 QStackedWidget
        layout = QGridLayout()
        layout.addWidget(self.stackedWidget, 0, 0)

        # 创建按钮并设置点击事件处理函数
        self.detect_adb_version_button = QPushButton("ADB版本信息")
        self.detect_adb_version_button.clicked.connect(self.show_adb_version)
        layout.addWidget(self.detect_adb_version_button, 1, 0)

        self.detect_android_version_button = QPushButton("检测Android版本信息")
        self.detect_android_version_button.clicked.connect(self.detect_android_version)
        layout.addWidget(self.detect_android_version_button, 1, 1)

        self.auto_detect_button = QPushButton("自动检测ADB参数")
        self.auto_detect_button.clicked.connect(self.detect_adb_parameters)
        layout.addWidget(self.auto_detect_button, 2, 0)

        self.manual_guide_button = QPushButton("手动获取ADB参数指引")
        self.manual_guide_button.clicked.connect(self.show_manual_guide)
        layout.addWidget(self.manual_guide_button, 2, 1)

        # 移除保存和加载参数的按钮，因为我们将在界面中直接切换
        # self.save_params_button = QPushButton("保存参数", self)
        # self.save_params_button.clicked.connect(self.openSaveParametersDialog)
        # layout.addWidget(self.save_params_button, 3, 0)

        # 移除自动执行ADB命令的按钮，因为我们将在界面中直接切换
        # self.autoExecuteADBButton = QPushButton("ADB命令自动执行", self)
        # self.autoExecuteADBButton.clicked.connect(self.openAutoExecuteADBCommandDialog)
        # layout.addWidget(self.autoExecuteADBButton, 3, 1)

        self.setLayout(layout)

    def show_manual_guide(self):
        guide_text = (
            "手动获取ADB参数指引：\n"
            "1. 设备ID：在命令行中输入 'adb devices'，设备ID将在命令输出中显示。\n"
            "2. 包名和活动名：在命令行中输入 'adb shell dumpsys activity activities | grep mResumedActivity'，"
            "应用的包名和活动名将在命令输出中显示。\n"
            "请确保您的设备已通过USB连接到计算机，并且已在开发者选项中启用了USB调试。"
        )
        QMessageBox.information(self, "手动获取ADB参数指引", guide_text)

    def show_adb_version(self):
        adb_version_output = get_adb_version()
        adb_version_message = f"ADB版本信息:\n\n{adb_version_output}\n\n这是Android Debug Bridge (ADB)的版本信息，它是Android开发和调试的重要工具。"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("ADB版本信息")
        msg_box.setText(adb_version_message)
        msg_box.exec_()

    def detect_android_version(self):
        device_id = self.device_id_edit.text()
        android_version_output = get_android_version(device_id)
        if android_version_output:
            self.android_version_edit.setText(android_version_output)
        else:
            QMessageBox.critical(self, "错误", "无法获取Android版本信息。请确保设备已连接并且ADB正在运行。")

    def detect_adb_parameters(self):
        try:
            adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8')
            print("ADB Version:", adb_version_output)
        except FileNotFoundError:
            QMessageBox.critical(self, "ADB未找到", "请确保ADB已安装并且环境变量设置正确。")
            return

        try:
            devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip().splitlines()[1:]
            device_id = devices_output[0].split()[0]  # 取第一个设备
            self.device_id_edit.setText(device_id)

            package_name, activity_name = get_foreground_activity_with_wakeup(device_id)
            if package_name and activity_name:
                self.package_name_edit.setText(package_name)
                self.activity_name_edit.setText(activity_name)
            else:
                QMessageBox.warning(self, "活动名检测失败", "无法检测到前台活动。")
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


    def openSaveParametersDialog(self):  # 保存按钮
        # 从UI组件获取参数
        params = {
            "device_id": self.device_id_edit.text(),
            "package_name": self.package_name_edit.text(),
            "activity_name": self.activity_name_edit.text(),
            "android_version": self.android_version_edit.text()  # 获取 Android 版本信息
        }
        # 创建 SaveParameters 对话框时传递参数
        saveDialog = SaveParameters(self, initial_params=params)
        saveDialog.exec_()

    def openAutoExecuteADBCommandDialog(self):#自动执行按钮
        dialog = AutoExecuteADBCommandDialog(self)
        dialog.exec_()   



