import os
import sys
import subprocess
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QMessageBox, QInputDialog
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime, timedelta

class ADBControlApp(QWidget):
    def __init__(self):#设备和应用参数
        super().__init__()
        self.device_id = "0123456789ABCDEF"
        self.package_name = "com.ss.android.lark"
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"
        self.init_ui()
        self.show_initial_dialog()

    def init_ui(self):#时间选择器相应的代码
        self.setWindowTitle('时间选择器')
        layout = QVBoxLayout()
        self.time_edit = QTimeEdit(self)
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(self.time_edit)
        self.time_label = QLabel('请选择操作执行时间', self)
        layout.addWidget(self.time_label)
        confirm_time_btn = QPushButton('确认时间', self)
        confirm_time_btn.clicked.connect(self.confirm_time)
        layout.addWidget(confirm_time_btn)
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
        QTimer.singleShot(5000, msg.close) # 5000 毫秒后自动关闭, 你可以根据需要设置不同的时间
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
        guide_msg.setStandardButtons(QMessageBox.Ok)
        guide_msg.exec_()
        self.device_id, ok = QInputDialog.getText(None, "输入新的设备ID", "设备ID:")
        if ok:
            self.package_name, ok = QInputDialog.getText(None, "输入新的包名", "包名:")
        if ok:
            self.activity_name, ok = QInputDialog.getText(None, "输入新的活动名", "活动名:")

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 设置在所有窗口关闭时不退出程序
    adb_control_app = ADBControlApp()
    adb_control_app.show()
    ret = app.exec_()  # 运行事件循环
    sys.exit(ret)  # 主事件循环结束后退出程序

if __name__ == '__main__':
    main()
