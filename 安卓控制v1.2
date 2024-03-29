import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QMessageBox, QInputDialog
from PyQt5.QtCore import QTime, QTimer
import subprocess
from datetime import datetime, timedelta
import random

# 设备ID，应用包名和活动名
device_id = "0123456789ABCDEF"
package_name = "com.ss.android.lark"
activity_name = "com.ss.android.lark.main.app.MainActivity"

# 执行ADB命令的函数
def adb_command(command):
    subprocess.run(["adb", "-s", device_id, "shell", command], capture_output=True)

# 增加一个唤醒设备的函数
def wake_up_device():
    adb_command("input keyevent KEYCODE_WAKEUP")

# 关闭应用的函数
def close_app():
    adb_command("input keyevent KEYCODE_HOME")

# 打开应用的函数
def open_app():
    adb_command(f"am start -n {package_name}/{activity_name}")

# 设置延时任务和执行命令的全局函数
def schedule_commands(selected_time):
    now = datetime.now()
    # 正确访问 hour 和 minute 属性，不使用括号
    target_time = now.replace(hour=selected_time.hour, minute=selected_time.minute, second=0, microsecond=0)
    if now > target_time:
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()
    QTimer.singleShot(int(wait_seconds * 1000), execute_commands)

# 修改执行命令的函数，加入唤醒手机的步骤
def execute_commands():
    print("执行ADB命令...")
    wake_up_device()  # 首先唤醒设备
    close_app()  # 然后关闭应用
    # 使用 QTimer.singleShot 来实现在关闭应用后延迟5秒再打开应用
    QTimer.singleShot(5000, open_app)
    # 弹出提醒对话框，告知用户操作已完成
    QMessageBox.information(None, "提醒", "指定的时间已到，操作执行完毕。")

# 创建一个时间选择器的窗口类
class TimePickerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
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

    def confirm_time(self):
        # 获取时间
        time = self.time_edit.time()
        selected_time = QTime(time.hour(), time.minute()).toPyTime()
        self.time_label.setText('操作将在: ' + selected_time.strftime('%H:%M') + ' 执行')
    
        # 在这里调用 schedule_commands 函数时传递的是 selected_time，确保它是正确的 datetime.time 对象
        schedule_commands(selected_time)
        self.close()  # 关闭窗口

# 新增一个函数用于在程序启动时询问用户
def show_initial_dialog():
    # 显示当前的设备信息
    info_msg = QMessageBox()
    info_msg.setIcon(QMessageBox.Information)
    info_msg.setWindowTitle("当前ADB配置")
    info_msg.setText(f"设备ID: {device_id}\n包名: {package_name}\n活动名: {activity_name}")
    info_msg.setInformativeText("您想要更改这些参数吗？")
    info_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    response = info_msg.exec_()  # 显示对话框并等待用户响应

    if response == QMessageBox.Yes:
        # 用户选择更改参数
        change_params_dialog()

def change_params_dialog():
    # 显示指导信息
    guide_msg = QMessageBox()
    guide_msg.setIcon(QMessageBox.Information)
    guide_msg.setWindowTitle("如何获取参数")
    guide_msg.setText("您可以使用以下ADB命令来获取所需参数：\n"
                      "- 设备ID: adb devices\n"
                      "- 包名和活动名: adb shell dumpsys window | grep mCurrentFocus")
    guide_msg.setStandardButtons(QMessageBox.Ok)
    guide_msg.exec_()

    # 这里可以扩展为实际让用户输入新的参数值，例如：
    global device_id, package_name, activity_name
    device_id, ok = QInputDialog.getText(None, "输入新的设备ID", "设备ID:")
    if ok:  # 如果用户点击OK，则更新设备ID
        package_name, ok = QInputDialog.getText(None, "输入新的包名", "包名:")
    if ok:  # 如果用户点击OK，则更新包名
        activity_name, ok = QInputDialog.getText(None, "输入新的活动名", "活动名:")

# 主函数
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 设置为 False
    
    show_initial_dialog()  # 在显示窗口之前询问用户

    window = TimePickerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
