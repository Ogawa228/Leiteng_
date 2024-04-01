import os
import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit,
                             QMessageBox, QInputDialog, QDialog, QCheckBox, QHBoxLayout, QTextEdit, QDialogButtonBox)
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime, timedelta

class GuideDialog(QDialog):
    def __init__(self, parent=None):
        super(GuideDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("欢迎使用ADB控制工具")
        self.resize(800, int(800 / 1.618))  # 黄金比例
        layout = QVBoxLayout(self)

        guide_text = ("欢迎使用ADB控制工具！本工具旨在帮助您在安卓设备上自动执行ADB命令。\n\n"
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
                      "请确保您的设备已连接到计算机（有线或无线），并已正确设置USB调试模式。")
        self.label = QLabel(guide_text, self)
        layout.addWidget(self.label)

        self.checkbox = QCheckBox("下次不再显示", self)
        layout.addWidget(self.checkbox)

        self.closeButton = QPushButton("关闭", self)
        self.closeButton.clicked.connect(self.accept)
        layout.addWidget(self.closeButton)

class ADBParametersDialog(QDialog):
    def __init__(self, parent=None):
        super(ADBParametersDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("输入ADB参数")
        self.layout = QVBoxLayout(self)

        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)

        self.checkbox = QCheckBox("下次不再显示此对话框", self)
        self.layout.addWidget(self.checkbox)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

    def getParameters(self):
        return self.textEdit.toPlainText().split('\n'), self.checkbox.isChecked()

class ADBControlApp(QWidget):
    def __init__(self):
        super(ADBControlApp, self).__init__()
        self.device_id = "0123456789ABCDEF"
        self.package_name = "com.ss.android.lark"
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"
        self.settings_path = "user_settings.txt"
        self.checkUserSettings()  # 确保此方法名与其定义相匹配
        self.initUI()

    def checkUserSettings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as file:
                settings = file.read()
                do_not_show_guide = "do_not_show_guide=true" in settings
                do_not_show_adb_parameters = "do_not_show_adb_parameters=true" in settings
                if not do_not_show_guide:
                    self.showGuide()
                if not do_not_show_adb_parameters:
                    self.showADBParametersDialog()


    def showGuide(self):
        guideDialog = GuideDialog(self)
        if guideDialog.exec_() and guideDialog.checkbox.isChecked():
            with open(self.settings_path, 'a') as file:
                file.write("do_not_show_guide=true\n")

    def showADBParametersDialog(self):
        adbParametersDialog = ADBParametersDialog(self)
        if adbParametersDialog.exec_() == QDialog.Accepted:
            # 解析返回的参数
            params, doNotShow = adbParametersDialog.getParameters()
            if len(params) == 3:
                self.device_id, self.package_name, self.activity_name = params
            if doNotShow:
                with open(self.settings_path, 'a') as file:
                    file.write("do_not_show_adb_parameters=true\n")

    def initUI(self):
        self.setWindowTitle('ADB命令执行器')
        layout = QVBoxLayout()

        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setTime(QTime.currentTime())
        layout.addWidget(self.timeEdit)

        self.timeLabel = QLabel('设置执行ADB命令的时间', self)
        layout.addWidget(self.timeLabel)

        self.confirm_TimeBtn = QPushButton('确认时间', self)
        self.confirm_TimeBtn.clicked.connect(self.confirmTime)
        layout.addWidget(self.confirm_TimeBtn)

        self.setLayout(layout)
        self.confirm_TimeBtn.clicked.connect(self.confirmTime)

    def loadSettings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as file:
                lines = file.readlines()
                self.settings = {line.split('=')[0]: line.split('=')[1].strip() for line in lines}
        else:
            self.settings = {}

    def saveSettings(self):
        with open(self.settings_path, "w") as file:
            for key, value in self.settings.items():
                file.write(f"{key}={value}\n")

    def showGuideIfNeeded(self):
        if self.settings.get("do_not_show_guide", "false") == "false":
            guideDialog = GuideDialog(self)
            guideDialog.exec_()
            if guideDialog.checkbox.isChecked():
                self.settings["do_not_show_guide"] = "true"
                self.saveSettings()

    def showADBParametersIfNeeded(self):
        if self.settings.get("do_not_show_adb_parameters", "false") == "false":
            adbParametersDialog = ADBParametersDialog(self)
            if adbParametersDialog.exec_() == QDialog.Accepted:
                parameters, doNotShowAgain = adbParametersDialog.getParameters()
                if doNotShowAgain:
                    self.settings["do_not_show_adb_parameters"] = "true"
                    self.saveSettings()
                if len(parameters) == 3:
                    self.device_id, self.package_name, self.activity_name = parameters

    def adb_command(self, command):
        try:
            subprocess.run(["adb", "-s", self.device_id, "shell", command], check=True)
        except subprocess.CalledProcessError as e:
            print("执行ADB命令出错:", e)

    def wake_up_device(self):
        self.adb_command("input keyevent KEYCODE_WAKEUP")

    def swipe_up(self):
        self.adb_command("input swipe 300 1000 300 500")

    def close_app(self):
        self.adb_command("input keyevent KEYCODE_HOME")

    def open_app(self):
        self.adb_command(f"am start -n {self.package_name}/{self.activity_name}")

    def schedule_commands(self, selected_time):
        now = datetime.now()
        # 移除了 hour 和 minute 后面的括号
        target_time = now.replace(hour=selected_time.hour, minute=selected_time.minute, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        QTimer.singleShot(int(wait_seconds * 1000), self.execute_commands)


    def show_message(self):
        QMessageBox.information(self, "操作完成", "指定的时间已到，ADB命令执行完毕。")
        QApplication.quit()
        

    def execute_commands(self):
        print("开始执行ADB命令序列...")
        # 首先唤醒设备
        QTimer.singleShot(2000, self.wake_up_device)  # 2秒后执行唤醒设备
        
        # 然后执行上滑解锁（假设唤醒后需要1秒）
        QTimer.singleShot(4000, self.swipe_up)  # 继上一个命令后等待2秒执行上滑解锁
        
        # 执行关闭应用（假设上滑后需要1秒）
        QTimer.singleShot(6000, self.close_app)  # 继上一个命令后等待2秒关闭应用
        
        # 执行打开应用（假设关闭应用后需要1秒）
        QTimer.singleShot(11000, self.open_app)  # 继上一个命令后等待2秒打开应用
        print("打开应用执行完毕")

        # 最后弹出提醒对话框，告知用户操作已完成（假设再次唤醒后需要1秒）
        QTimer.singleShot(15000, self.show_message)  # 继上一个命令后等待2秒显示提醒对话框
    
    def confirmTime(self):
        selected_time = self.timeEdit.time().toPyTime()
        self.schedule_commands(selected_time)
        self.hide()  # 隐藏当前窗口，让应用在后台运行
        print("确认时间已设置，命令将在指定时间执行。")

    def confirm_time(self):
        self.showGuideIfNeeded()
        self.showADBParametersIfNeeded()
        time = self.time_edit.time()
        selected_time = QTime(time.hour(), time.minute()).toPyTime()
        self.schedule_commands(selected_time)
        print("开始执行确认时间命令...")
        self.close()
        
        

    def show_guide(self):
        guide = GuideDialog(self)
        guide.exec_()
        if guide.checkbox.isChecked():
            self.save_settings(do_not_show=True)
        self.change_params_dialog()
    
    def show_adb_parameters_guide(self):#获取 ADB 参数的指引
        message = (
            "如何获取ADB相关参数：\n"
            "1. 设备ID：在命令行中输入'adb devices'，设备ID将显示在命令输出中。\n"
            "2. 应用名称和包名称：在命令行中输入'adb shell dumpsys activity activities | grep mResumedActivity'，应用的包名和活动名将显示在命令输出中。\n"
            "确保您的设备已连接到计算机并且已开启USB调试。"
        )
        dialog = QMessageBox()
        dialog.setWindowTitle("获取ADB参数")
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Information)
        checkbox = QCheckBox("下次不再显示此指引")
        dialog.setCheckBox(checkbox)
        dialog.exec_()
    
        if checkbox.isChecked():
            self.save_settings(do_not_show_adb_guide=True)

    def show_adb_parameters_dialog(self):
        dialog = ADBParametersDialog(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            deviceId, packageName, activityName, doNotShowAgain = dialog.getParameters()
            # 更新设置
            self.device_id = deviceId
            self.package_name = packageName
            self.activity_name = activityName
            
            if doNotShowAgain:
                # 保存设置以避免再次显示对话框
                self.save_settings(do_not_show_guide=True, do_not_show_adb_guide=True)


    def load_settings(self):
        settings = {
            "do_not_show_guide": False,
            "do_not_show_adb_guide": False,
            "device_id": self.device_id,
            "package_name": self.package_name,
            "activity_name": self.activity_name
        }
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as f:
                for line in f:
                    key, value = line.strip().split('=')
                    if key in settings:
                        settings[key] = value == 'true' if value in ['true', 'false'] else value
        return settings


    def save_settings(self, do_not_show_guide=False, do_not_show_adb_guide=False):
        with open(self.settings_path, "w") as f:
            if do_not_show_guide:
                f.write("do_not_show_guide=true\n")
            else:
                f.write("do_not_show_guide=false\n")
            
            if do_not_show_adb_guide:
                f.write("do_not_show_adb_guide=true\n")
            else:
                f.write("do_not_show_adb_guide=false\n")
            
            # 保存其他ADB相关参数
            f.write(f"device_id={self.device_id}\n")
            f.write(f"package_name={self.package_name}\n")
            f.write(f"activity_name={self.activity_name}\n")


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 设置在所有窗口关闭时不退出程序
    ex = ADBControlApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
