#其他函数
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel, QLineEdit, QGridLayout, QMessageBox, QFrame
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush
from PyQt5.QtCore import Qt
import subprocess


#自定义的函数
from 获取初始参数_adb_命令 import get_adb_version, get_android_version, get_foreground_activity, get_foreground_activity_with_wakeup
from style_manager import StyleManager
from 功能管理.自动执行功能按钮 import AutoExecuteADBCommandDialog
from 功能管理.参数详情按钮 import SaveParameters
from 参数.parameter_manager import load_latest_parameters

class MainApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADB参数配置")
        self.styleManager = StyleManager()  # 创建 StyleManager 实例
        self.initUI()
        self.resize(800, 600)  # 设置窗口初始大小

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.stackedWidget = QStackedWidget()
        self.saveParametersDialog = SaveParameters()
        self.autoExecuteADBCommandDialog = AutoExecuteADBCommandDialog()
        self.stackedWidget.addWidget(self.saveParametersDialog)
        self.stackedWidget.addWidget(self.autoExecuteADBCommandDialog)
        self.layout.addWidget(self.stackedWidget)
        
        self.styleManager.applyStyle(self.stackedWidget)  # 使用实例调用 applyStyle

        self.addSeparator()

        self.setupTextBoxArea()

        self.addSeparator()

        self.setupButtonArea()

    def addSeparator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)


    def setupButtonArea(self):
        self.buttonLayout = QHBoxLayout()  # Directly using self.buttonLayout for the layout

        # Initialize buttons and apply styles
        self.saveParamsButton = QPushButton("参数详情")
        self.autoExecuteButton = QPushButton("自动执行ADB命令")
        self.autoDetectADBParamsButton = QPushButton("自动检测ADB参数")
        self.adbVersionInfoButton = QPushButton("ADB版本信息")
        self.androidVersionInfoButton = QPushButton("检测Android版本信息")
        self.manualADBParamsGuideButton = QPushButton("手动获取ADB参数指引")

        # Connecting buttons to their respective slots
        self.saveParamsButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.saveParametersDialog))
        self.autoExecuteButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.autoExecuteADBCommandDialog))
        self.autoDetectADBParamsButton.clicked.connect(self.detect_adb_parameters)
        self.adbVersionInfoButton.clicked.connect(self.show_adb_version)
        self.androidVersionInfoButton.clicked.connect(self.detect_android_version)
        self.manualADBParamsGuideButton.clicked.connect(self.show_manual_guide)

        buttons = [self.saveParamsButton, self.autoExecuteButton, self.autoDetectADBParamsButton,
                self.adbVersionInfoButton, self.androidVersionInfoButton, self.manualADBParamsGuideButton]

        for button in buttons:
            self.styleManager.applyStyle(button)
            self.buttonLayout.addWidget(button)

        buttonWidget = QWidget()  # Create a container Widget
        buttonWidget.setLayout(self.buttonLayout)  # Apply the layout to the container Widget
        self.layout.addWidget(buttonWidget)  # Add the container Widget to the main layout



    def setupTextBoxArea(self):
        # 确保在此之前已经定义了 self.styleManager 作为 StyleManager 的一个实例
        self.textBoxLayout = QGridLayout()

        last_params = load_latest_parameters() if load_latest_parameters() else {}

        self.device_id_edit = QLineEdit(last_params.get("device_id", ""))
        self.package_name_edit = QLineEdit(last_params.get("package_name", ""))
        self.activity_name_edit = QLineEdit(last_params.get("activity_name", ""))
        self.android_version_edit = QLineEdit(last_params.get("android_version", ""))
        self.android_version_edit.setReadOnly(True)

        # 为每个 QLineEdit 应用样式
        self.styleManager.applyStyle(self.device_id_edit)
        self.styleManager.applyStyle(self.package_name_edit)
        self.styleManager.applyStyle(self.activity_name_edit)
        self.styleManager.applyStyle(self.android_version_edit)

        # 将 QLineEdit 添加到布局
        # 注意：以下是假设的布局代码，您需要根据实际布局调整
        self.textBoxLayout.addWidget(QLabel("设备ID:"), 0, 0)
        self.textBoxLayout.addWidget(self.device_id_edit, 0, 1)
        self.textBoxLayout.addWidget(QLabel("包名:"), 1, 0)
        self.textBoxLayout.addWidget(self.package_name_edit, 1, 1)
        self.textBoxLayout.addWidget(QLabel("活动名:"), 2, 0)
        self.textBoxLayout.addWidget(self.activity_name_edit, 2, 1)
        self.textBoxLayout.addWidget(QLabel("Android版本:"), 3, 0)
        self.textBoxLayout.addWidget(self.android_version_edit, 3, 1)

        textBoxWidget = QWidget()
        textBoxWidget.setLayout(self.textBoxLayout)
        self.layout.addWidget(textBoxWidget)

    def showLoadParametersDialog(self):
        self.stackedWidget.setCurrentWidget(self.loadParametersDialog)

    def showSaveParametersDialog(self):
        # 从UI组件获取当前的参数
        params = {
            "device_id": self.device_id_edit.text(),
            "package_name": self.package_name_edit.text(),
            "activity_name": self.activity_name_edit.text(),
            "android_version": self.android_version_edit.text()
        }
        # 检查SaveParameters对话框是否已经存在并设置参数
        # 注意: 根据您的实现，这里可能需要调整
        if hasattr(self, 'saveParametersDialog') and self.saveParametersDialog:
            self.saveParametersDialog.setInitialParams(params)
        else:
            # 如果没有实例，创建它并传入参数
            self.saveParametersDialog = SaveParameters(self, initial_params=params)

        # 切换到SaveParameters对话框
        self.stackedWidget.setCurrentWidget(self.saveParametersDialog)
        

    def showAutoExecuteADBCommandDialog(self):
        self.stackedWidget.setCurrentWidget(self.autoExecuteADBCommandDialog)


    
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
        # 假设 self.device_id_edit 是设备ID的 QLineEdit 控件
        device_id = self.device_id_edit.text()
        android_version_output = get_android_version(device_id)  # 调用函数获取 Android 版本信息

        if android_version_output:
            self.android_version_edit.setText(android_version_output)  # 更新编辑框文本
            
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
    


