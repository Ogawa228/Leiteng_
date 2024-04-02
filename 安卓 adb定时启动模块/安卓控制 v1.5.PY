import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit,
    QMessageBox, QInputDialog, QDialog, QCheckBox, QHBoxLayout, QTextEdit, QDialogButtonBox
)
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime, timedelta


class GuideDialog(QDialog):
    def __init__(self, parent=None):
        super(GuideDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("欢迎使用ADB控制工具")
        self.resize(800, int(800 / 1.618))  # 黄金比例
        layout = QVBoxLayout(self)

        guide_text = (
            "欢迎使用ADB控制工具！本工具旨在帮助您在安卓设备上自动执行ADB命令。\n\n"
            "【重要说明】\n"
            "1. 本工具仅适用于安卓设备。\n"
            "2. 不同的安卓版本可能需要不同版本的ADB工具，请确保您的ADB工具与设备兼容。\n"
            "3. 在使用本工具之前，请确保您的安卓设备已开启USB调试模式。\n\n"
            "【如何查看安卓版本】\n"
            "- 在设备上打开“设置” > “关于手机” > “Android版本”。\n\n"
            "【如何开启USB调试模式】\n"
            "- 在设备上打开“设置” > “系统” > “开发者选项”。\n\n"
            "【无线调试模式】\n"
            "- 安卓11及以上版本支持无线调试。在“开发者选项”中找到“无线调试”并开启。\n\n"
            "【使用步骤】\n"
            "1. 首先，程序会显示当前ADB配置（设备ID、包名、活动名）。\n"
            "2. 如果您需要更改这些参数，选择'是'以进入参数设置界面。\n"
            "3. 使用时间选择器设置您希望执行ADB命令的具体时间，并点击'确认时间'按钮。\n"
            "4. 程序将在您设定的时间自动执行预设ADB命令，实现自动化操作。\n\n"
            "请确保您的设备已连接到计算机（有线或无线），并已正确设置USB调试模式。"
        )
        self.label = QLabel(guide_text, self)
        layout.addWidget(self.label)

        self.checkbox = QCheckBox("下次不再显示", self)
        layout.addWidget(self.checkbox)

        self.close_button = QPushButton("关闭", self)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)


class ADBParametersDialog(QDialog):
    def __init__(self, parent=None, device_id="0123456789ABCDEF", package_name="com.ss.android.lark", activity_name="com.ss.android.lark.main.app.MainActivity"):
        super(ADBParametersDialog, self).__init__(parent)
        self.device_id = device_id
        self.package_name = package_name
        self.activity_name = activity_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("输入ADB参数")
        # 设置对话框大小为黄金比例
        self.resize(800, int(800 / 1.618))

        layout = QVBoxLayout(self)

        # 设备ID参数
        layout.addWidget(QLabel("设备ID:"))
        self.device_id_edit = QTextEdit(self.device_id, self)
        layout.addWidget(self.device_id_edit)

        # 包名参数
        layout.addWidget(QLabel("包名:"))
        self.package_name_edit = QTextEdit(self.package_name, self)
        layout.addWidget(self.package_name_edit)

        # 活动名参数
        layout.addWidget(QLabel("活动名:"))
        self.activity_name_edit = QTextEdit(self.activity_name, self)
        layout.addWidget(self.activity_name_edit)

        self.checkbox = QCheckBox("下次不再显示此对话框", self)
        layout.addWidget(self.checkbox)

        # 添加获取ADB参数指引按钮
        self.adb_guide_btn = QPushButton("如何获取ADB参数？", self)
        self.adb_guide_btn.clicked.connect(self.show_adb_guide)
        layout.addWidget(self.adb_guide_btn)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_parameters(self):
        params = [
            self.device_id_edit.toPlainText(),
            self.package_name_edit.toPlainText(),
            self.activity_name_edit.toPlainText()
        ]
        return params, self.checkbox.isChecked()

    def show_adb_guide(self):
        guide_text = """如何获取ADB相关参数：
1. 设备ID: 在命令行中输入 'adb devices'。
2. 包名: 在命令行中输入 'adb shell pm list packages | grep [应用名]' 来找到对应的包名。
3. 活动名: 在命令行中输入 'adb shell dumpsys activity activities | grep mResumedActivity' 来找到当前前台活动的完整名称。
确保您的设备已通过USB或无线连接到电脑，并且开启了USB调试。"""
        QMessageBox.information(self, "获取ADB参数指引", guide_text)



class ADBControlApp(QWidget):
    def __init__(self):
        super(ADBControlApp, self).__init__()
        self.device_id = "0123456789ABCDEF"
        self.package_name = "com.ss.android.lark"
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"
        self.settings_path = "user_settings.txt"
        self.load_settings()
        self.init_ui()

    def load_settings(self):
        self.settings = {"do_not_show_guide": False, "do_not_show_adb_parameters": False}
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split('=')
                    self.settings[key] = value == 'true'

        if not self.settings["do_not_show_guide"]:
            self.show_guide()
        if not self.settings["do_not_show_adb_parameters"]:
            self.show_adb_parameters_dialog()

    def save_settings(self):
        with open(self.settings_path, 'w') as file:
            for key, value in self.settings.items():
                file.write(f"{key}={str(value).lower()}\n")

    def init_ui(self):
        self.setWindowTitle('ADB命令执行器')
        layout = QVBoxLayout()

        self.time_edit = QTimeEdit(self)
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(self.time_edit)

        self.time_label = QLabel('设置执行ADB命令的时间', self)
        layout.addWidget(self.time_label)

        self.confirm_time_btn = QPushButton('确认时间', self)
        self.confirm_time_btn.clicked.connect(self.confirm_time)
        layout.addWidget(self.confirm_time_btn)

        self.setLayout(layout)

    def swipe_up(self):#上滑操作
        self.adb_command("input swipe 300 1000 300 500")

    def adb_command(self, command):
        subprocess.run(["adb", "-s", self.device_id, "shell", command], capture_output=True)

    def wake_up_device(self):
        self.adb_command("input keyevent KEYCODE_WAKEUP")

    def close_app(self):
        self.adb_command("input keyevent KEYCODE_HOME")

    def open_app(self):
        self.adb_command(f"am start -n {self.package_name}/{self.activity_name}")

    def schedule_commands(self, selected_time):
        now = datetime.now()
        target_time = now.replace(hour=selected_time.hour, minute=selected_time.minute, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        QTimer.singleShot(int(wait_seconds * 1000), self.execute_commands)

    def show_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("提醒")
        msg.setText("指定的时间已到，操作执行完毕。")
        
        # 设置 QTimer 来关闭消息框
        QTimer.singleShot(10000, msg.close) # 10秒后自动关闭, 你可以根据需要设置不同的时间
        msg.exec_()    
        # 新增：消息框关闭后，调用程序退出
        QTimer.singleShot(1000, QApplication.instance().quit)  # 给一点时间关闭消息框后再退出程序


    def execute_commands(self):
        print("开始执行ADB命令序列...")
        # 首先唤醒设备
        QTimer.singleShot(2000, self.wake_up_device)  # 2秒后执行唤醒设备
        
        # 然后执行上滑解锁（假设唤醒后需要1秒）
        QTimer.singleShot(4000, self.swipe_up)  # 继上一个命令后等待2秒执行上滑解锁
        
        # 执行关闭应用（假设上滑后需要1秒）
        QTimer.singleShot(6000, self.close_app)  # 继上一个命令后等待2秒关闭应用
        
        # 执行打开应用（假设关闭应用后需要1秒）
        QTimer.singleShot(8000, self.open_app)  # 继上一个命令后等待2秒打开应用
        
        # 再次唤醒设备，确保设备不会休眠（假设打开应用后需要5秒）
        QTimer.singleShot(13000, self.wake_up_device)  # 继上一个命令后等待5秒再次唤醒设备

        # 最后弹出提醒对话框，告知用户操作已完成（假设再次唤醒后需要1秒）
        QTimer.singleShot(15000, self.show_message)  # 继上一个命令后等待2秒显示提醒对话框

    def confirm_time(self):
        time = self.time_edit.time()
        selected_time = QTime(time.hour(), time.minute()).toPyTime()
        self.time_label.setText('操作将在: ' + selected_time.strftime('%H:%M') + ' 执行')
        self.schedule_commands(selected_time)
        self.close()


    def show_guide(self):
        guide_dialog = GuideDialog(self)
        if guide_dialog.exec_() and guide_dialog.checkbox.isChecked():
            self.settings["do_not_show_guide"] = True
            self.save_settings()

    def show_adb_parameters_dialog(self):
        adb_parameters_dialog = ADBParametersDialog(self)
        if adb_parameters_dialog.exec_() == QDialog.Accepted:
            params, do_not_show = adb_parameters_dialog.get_parameters()
            if len(params) == 3:
                self.device_id, self.package_name, self.activity_name = params
            if do_not_show:
                self.settings["do_not_show_adb_parameters"] = True
                self.save_settings()

    def save_settings(self):
        with open(self.settings_path, 'w') as file:
            for key, value in self.settings.items():
                file.write(f"{key}={str(value).lower()}\n")


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 确保关闭所有窗口时程序不会退出
    ex = ADBControlApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
