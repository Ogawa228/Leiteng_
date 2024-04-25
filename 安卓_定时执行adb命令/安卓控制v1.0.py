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

def execute_commands():
    print("执行ADB命令...")
    close_app()
    QTimer.singleShot(5000, open_app)
    QMessageBox.information(None, "提醒", "指定的时间已到 ，打卡操作执行完毕。")  # 注意这里的None参数

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

# 主函数
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 设置为 False
    window = TimePickerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
