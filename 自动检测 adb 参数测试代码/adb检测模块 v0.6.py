import subprocess
import time
import pickle
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QSizePolicy
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel,QHBoxLayout
from PyQt5.QtWidgets import QGraphicsDropShadowEffect



class ADBParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADB参数配置")
        self.init_ui()

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

        self.detect_button = QPushButton("ADB版本信息")
        self.detect_button.clicked.connect(self.show_adb_version)
        self.detect_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.detect_button, 3, 0)

        self.detect_android_version_button = QPushButton("检测Android版本信息")
        self.detect_android_version_button.clicked.connect(self.detect_android_version)
        self.detect_android_version_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.detect_android_version_button, 3, 1)

        self.detect_button = QPushButton("自动检测ADB参数")
        self.detect_button.clicked.connect(self.detect_adb_parameters)
        self.detect_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.detect_button, 4, 0)

        self.manual_guide_button = QPushButton("手动获取ADB参数指引")
        self.manual_guide_button.clicked.connect(self.show_manual_guide)
        self.manual_guide_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.manual_guide_button, 4, 1)

        self.save_params_button = QPushButton("保存参数")
        self.save_params_button.clicked.connect(self.save_parameters)
        self.save_params_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.save_params_button, 5, 0)

        self.load_params_button = QPushButton("加载参数")
        self.load_params_button.clicked.connect(self.load_parameters)
        self.load_params_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.load_params_button, 5, 1)  # 确保所有的控件都被添加到了layout中

        self.setLayout(layout)  # 设置layout为对话框的布局

        # 设置列宽
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        # 设置渐变色背景
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#5EFCE8"))
        gradient.setColorAt(1.0, QColor("#736EFE"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # 设置按钮文字颜色
        button_style = "QPushButton { color: black; }"
        self.detect_button.setStyleSheet(button_style)
        self.detect_android_version_button.setStyleSheet(button_style)
        self.detect_button.setStyleSheet(button_style)
        self.manual_guide_button.setStyleSheet(button_style)
        self.save_params_button.setStyleSheet(button_style)
        self.load_params_button.setStyleSheet(button_style)
        
        # 设置所有控件的样式
        style = """
        * {
            font-weight: bold;
        }
        QPushButton {
            background-color: #ABDCFF;
            border: 2px solid #555555;  # 加粗边框
            border-radius: 10px;  # 圆角边框
            color: white;
            padding: 15px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            margin: 4px 2px;
        }
        """
        self.setStyleSheet(style)

        # 设置所有按钮的鼠标指针样式
        self.detect_button.setCursor(Qt.PointingHandCursor)
        self.detect_android_version_button.setCursor(Qt.PointingHandCursor)
        self.manual_guide_button.setCursor(Qt.PointingHandCursor)
        self.save_params_button.setCursor(Qt.PointingHandCursor)
        self.load_params_button.setCursor(Qt.PointingHandCursor)
        
    def detect_android_version(self):##安卓版本信息
        try:
            android_version_output = subprocess.check_output(["adb", "shell", "getprop", "ro.build.version.release"], encoding='utf-8')
            QMessageBox.information(self, "Android版本信息", "Android版本信息:\n\n" + android_version_output)
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "错误", "无法获取Android版本信息。请确保设备已连接并且ADB正在运行。")
    def show_adb_version(self):## adb版本信息
        adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8')
        adb_version_message = "ADB版本信息:\n\n" + adb_version_output + "\n\n这是Android Debug Bridge (ADB)的版本信息，它是Android开发和调试的重要工具。"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("ADB版本信息")
        msg_box.setText(adb_version_message)

        msg_box.exec_()
        

    def detect_adb_parameters(self):##当前 adb参数
        # First, check if ADB is installed and accessible
        try:
            adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8')
            print("ADB Version:", adb_version_output)
        except FileNotFoundError:
            QMessageBox.critical(self, "ADB未找到", "请确保ADB已安装并且环境变量设置正确。")
            return
        
        # Now, let's try to get the list of connected devices
        try:
            devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip()
            devices_lines = devices_output.splitlines()[1:]  # Skip the 'List of devices attached' line

            if devices_lines:
                device_id = devices_lines[0].split()[0]  # Take the first device
                self.device_id_edit.setText(device_id)

                # Try to wake up and unlock the device
                self.wake_up_device(device_id)

                # Attempt to get the foreground activity name
                self.get_foreground_activity(device_id)
            else:
                QMessageBox.warning(self, "未检测到设备", "请连接设备并开启USB调试。")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "执行ADB命令出错", str(e))

    def wake_up_device(self, device_id):
        try:
            subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_WAKEUP"], check=True)
            time.sleep(1)  # Wait for the device to wake up
            subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "400", "2000", "400", "500"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "设备唤醒失败", f"设备可能未正确连接或锁屏状态无法解锁。错误: {str(e)}")

    def get_foreground_activity(self, device_id):
        try:
            dumpsys_output = subprocess.check_output(["adb", "-s", device_id, "shell", "dumpsys", "activity", "activities"], encoding='utf-8')
            for line in dumpsys_output.splitlines():
                if "mResumedActivity" in line:
                    activity_info = line.split()[-2]
                    package_name, activity_name = activity_info.split("/")
                    self.package_name_edit.setText(package_name)
                    self.activity_name_edit.setText(activity_name)
                    return
            QMessageBox.warning(self, "活动名检测失败", "无法检测到前台活动。")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "检测前台活动出错", str(e))

    def show_manual_guide(self):
        guide_text = (
            "手动获取ADB参数指引：\n"
            "1. 设备ID：在命令行中输入 'adb devices'，设备ID将在命令输出中显示。\n"
            "2. 包名和活动名：在命令行中输入 'adb shell dumpsys activity activities | grep mResumedActivity'，"
            "应用的包名和活动名将在命令输出中显示。\n\n"
            "请确保您的设备已通过USB连接到计算机，并且已在开发者选项中启用了USB调试。"
        )
        QMessageBox.information(self, "手动获取ADB参数指引", guide_text)
    def save_parameters(self):
        params = {
            'device_id': self.device_id_edit.text(),
            'package_name': self.package_name_edit.text(),
            'activity_name': self.activity_name_edit.text(),
        }
        with open('adb_params.pkl', 'wb') as f:
            pickle.dump(params, f)
        QMessageBox.information(self, "参数已保存", "ADB参数已成功保存。")

    def load_parameters(self):
        try:
            with open('adb_params.pkl', 'rb') as f:
                params = pickle.load(f)
            self.device_id_edit.setText(params['device_id'])
            self.package_name_edit.setText(params['package_name'])
            self.activity_name_edit.setText(params['activity_name'])
        except FileNotFoundError:
            QMessageBox.warning(self, "无法加载参数", "没有找到保存的ADB参数。请先保存参数。")


if __name__ == "__main__":
    app = QApplication([])
    dialog = ADBParametersDialog()
    dialog.show()  # 显示对话框
    app.exec_()