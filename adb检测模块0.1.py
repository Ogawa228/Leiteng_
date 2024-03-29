from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QDialogButtonBox, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QProcess
import sys
import subprocess

class ADBParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADB 参数配置")
        self.setFixedSize(800, int(800 / 1.618))  # Set window size based on the golden ratio
        
        self.device_id = "0123456789ABCDEF"  # Default device ID
        self.package_name = "com.ss.android.lark"  # Default package name
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"  # Default activity name

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("设备ID:"))
        self.device_id_line_edit = QLineEdit(self.device_id)
        layout.addWidget(self.device_id_line_edit)

        layout.addWidget(QLabel("包名:"))
        self.package_name_line_edit = QLineEdit(self.package_name)
        layout.addWidget(self.package_name_line_edit)

        layout.addWidget(QLabel("活动名:"))
        self.activity_name_line_edit = QLineEdit(self.activity_name)
        layout.addWidget(self.activity_name_line_edit)

        self.detect_button = QPushButton("自动检测 ADB 参数")
        self.detect_button.clicked.connect(self.auto_detect_parameters)
        layout.addWidget(self.detect_button)

        self.adb_guide_button = QPushButton("手动获取 ADB 参数指引")
        self.adb_guide_button.clicked.connect(self.show_adb_guide)
        layout.addWidget(self.adb_guide_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)  # Initially hide the progress bar
        layout.addWidget(self.progress_bar)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def auto_detect_parameters(self):
    # 检查ADB命令是否可用
        try:
            subprocess.check_output(["adb", "version"])
        except (subprocess.CalledProcessError, FileNotFoundError):
            QMessageBox.warning(self, "错误", "无法找到ADB。请确保ADB已安装，并且路径已添加到系统环境变量中。")
            return
        self.progress_bar.setVisible(True)
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.finished.connect(lambda: self.on_detect_devices_finished(process))
        process.start("adb", ["devices"])
    
    def on_detect_devices_finished(self, process):
        output = process.readAllStandardOutput().data().decode()
        devices = [line for line in output.splitlines() if "\tdevice" in line]
        if devices:
            self.device_id = devices[0].split("\t")[0]
            self.device_id_line_edit.setText(self.device_id)
            # 获取前台活动名称
            self.get_foreground_activity()
        else:
            QMessageBox.information(self, "自动检测失败", "未检测到任何设备。")
            self.progress_bar.setVisible(False)

    def get_foreground_activity(self):
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.finished.connect(lambda: self.on_get_foreground_activity_finished(process))
        process.start("adb", ["-s", self.device_id, "shell", "dumpsys", "activity", "activities", "|", "grep", "mResumedActivity"])

    def on_get_foreground_activity_finished(self, process):
        output = process.readAllStandardOutput().data().decode()
        # 解析输出以获取前台活动的包名和活动名
        # 注意：这里的解析逻辑可能需要根据实际输出调整
        if "mResumedActivity" in output:
            try:
                # 通常mResumedActivity后面会跟着包名和活动名，格式如：ComponentInfo{包名/活动名}
                activity_info = output.split("ComponentInfo{")[1].split("}")[0]
                package_name, activity_name = activity_info.split("/")
                self.package_name_line_edit.setText(package_name)
                self.activity_name_line_edit.setText(activity_name)
            except IndexError:
                QMessageBox.warning(self, "解析失败", "无法解析前台活动名称。")
        self.progress_bar.setVisible(False)



    def show_adb_guide(self):
        guide_text = ("获取 ADB 参数指引：\n\n"
                      "1. 设备 ID：在命令行中输入 'adb devices'，设备 ID 将在命令输出中显示。\n"
                      "2. 包名和活动名：在命令行中输入 'adb shell dumpsys activity activities | grep mResumedActivity'，"
                      "应用的包名和活动名将在命令输出中显示。\n\n"
                      "请确保您的设备已通过 USB 连接到计算机，并且已在开发者选项中启用了 USB 调试。")
        QMessageBox.information(self, "ADB 参数获取指引", guide_text)

    def get_parameters(self):
        return (self.device_id_line_edit.text(), self.package_name_line_edit.text(), self.activity_name_line_edit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ADBParametersDialog()
    if dialog.exec_():
        device_id, package_name, activity_name = dialog.get_parameters()
        print("Device ID:", device_id)
        print("Package Name:", package_name)
        print("Activity Name:", activity_name)
