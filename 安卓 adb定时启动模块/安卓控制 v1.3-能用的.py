import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QDateTimeEdit, QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer, QDateTime
from datetime import datetime
import  subprocess

class ADBControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.device_id = "0123456789ABCDEF"
        self.package_name = "com.ss.android.lark"
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"
        self.init_ui()
        self.show_initial_dialog()

    def init_ui(self):
        self.setWindowTitle('ADB控制器')
        layout = QVBoxLayout()
        self.date_time_edit = QDateTimeEdit(self)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.date_time_edit)
        self.time_label = QLabel('请选择操作执行日期和时间', self)
        layout.addWidget(self.time_label)
        confirm_time_btn = QPushButton('确认时间', self)
        confirm_time_btn.clicked.connect(self.confirm_time)
        layout.addWidget(confirm_time_btn)
        self.setLayout(layout)

    def adb_command(self, command):
        try:
            subprocess.run(["adb", "-s", self.device_id, "shell", command], check=True)
        except subprocess.CalledProcessError as e:
            print("执行ADB命令出错:", e)

    def wake_up_device(self):
        self.adb_command("input keyevent KEYCODE_WAKEUP")

    def close_app(self):
        self.adb_command("input keyevent KEYCODE_HOME")

    def open_app(self):
        self.adb_command(f"am start -n {self.package_name}/{self.activity_name}")

    def swipe_up(self):
        self.adb_command("input swipe 300 1000 300 500")

    def execute_commands(self):
        print("开始执行ADB命令序列...")
        self.wake_up_device()
        QTimer.singleShot(2000, self.swipe_up)
        QTimer.singleShot(4000, self.close_app)
        QTimer.singleShot(6000, self.open_app)
        QTimer.singleShot(10000, self.wake_up_device)
        QTimer.singleShot(12000, self.show_message)

    def confirm_time(self):
        selected_datetime = self.date_time_edit.dateTime().toPyDateTime()
        current_datetime = datetime.now()
        delay = int((selected_datetime - current_datetime).total_seconds() * 1000)
        if delay < 0:
            self.time_label.setText('选择的时间已过，请选择未来的时间。')
            return
        self.time_label.setText('操作将在: ' + selected_datetime.strftime('%Y-%m-%d %H:%M') + ' 执行')
        QTimer.singleShot(delay, self.execute_commands)
        self.close()

    def show_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("提醒")
        msg.setText("指定的时间已到，操作执行完毕。")
        msg.exec_()
        QTimer.singleShot(1000, QApplication.instance().quit)

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
        guide_msg.exec_()
        self.device_id, ok = QInputDialog.getText(self, "输入新的设备ID", "设备ID:")
        if ok:
            self.package_name, ok = QInputDialog.getText(self, "输入新的包名", "包名:")
        if ok:
            self.activity_name, ok = QInputDialog.getText(self, "输入新的活动名", "活动名:")

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    adb_control_app = ADBControlApp()
    adb_control_app.show()
    ret = app.exec_()
    sys.exit(ret)

if __name__ == '__main__':
    main()
