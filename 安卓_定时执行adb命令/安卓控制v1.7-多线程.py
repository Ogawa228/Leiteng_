import sys
import subprocess
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer, QDateTime, QSize
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QDateTimeEdit, QMessageBox,
                             QInputDialog, QTableWidget, QTableWidgetItem,
                             QHeaderView, QCheckBox, QAbstractItemView)



class ADBControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.device_id = "0123456789ABCDEF"
        self.package_name = "com.ss.android.lark"
        self.activity_name = "com.ss.android.lark.main.app.MainActivity"
        self.timers = {}
        self.timer_to_task = {}  # 关联计时器和任务列表项
        self.init_ui()
        self.show_initial_dialog()

    def init_ui(self):
        self.setWindowTitle('ADB控制器')
        main_layout = QVBoxLayout()

        # 使用 QTableWidget
        self.task_list = QTableWidget(0, 3)  # 初始化表格，0 行 3 列
        self.task_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.task_list.setHorizontalHeaderLabels(["后台执行", "任务执行时间", "操作"])
        self.task_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 使任务时间列自动拉伸填充空间
        self.task_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 第一列和第三列根据内容调整大小
        self.task_list.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # 设置表头样式
        self.task_list.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #f0f0f0; border: 1px solid black; font-family: '微软雅黑'; font-size: 12px; text-align: center; }")
        main_layout.addWidget(self.task_list)

        self.date_time_edit = QDateTimeEdit(self)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        main_layout.addWidget(self.date_time_edit)

        confirm_time_btn = QPushButton('安排新任务', self)
        confirm_time_btn.clicked.connect(self.confirm_time)
        main_layout.addWidget(confirm_time_btn)

        self.setLayout(main_layout)

    def confirm_time(self):
        selected_datetime = self.date_time_edit.dateTime().toPyDateTime()
        current_datetime = datetime.now()
        delay = int((selected_datetime - current_datetime).total_seconds() * 1000)
        task_key = selected_datetime.strftime('%Y-%m-%d %H:%M')

        if delay < 0:
            QMessageBox.warning(self, "错误", "选择的时间已过，请选择未来的时间。")
            return
        elif delay > 2147483647:  # 最大32位整数值
            QMessageBox.warning(self, "错误", "设置的时间太远，超出了定时器的限制。")
            return

        timer = QTimer()
        if task_key in self.timers:
            QMessageBox.warning(self, "错误", "已存在相同时间的任务，请选择其他时间。")
            return

        timer.singleShot(delay, lambda: self.execute_commands(task_key))
        self.timers[task_key] = timer
        self.add_task_to_list(task_key, timer)


    def add_task_to_list(self, task_time, timer):
        row_count = self.task_list.rowCount()
        self.task_list.insertRow(row_count)  # 插入新行

        # 第一列：复选框居中
        checkbox = QCheckBox()
        checkbox.setToolTip("勾选此复选框将任务设置为在后台运行")
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_widget.setLayout(checkbox_layout)
        self.task_list.setCellWidget(row_count, 0, checkbox_widget)

        # 第二列：任务时间标签
        task_label = QTableWidgetItem(task_time)
        task_label.setTextAlignment(Qt.AlignCenter)
        self.task_list.setItem(row_count, 1, task_label)

        # 第三列：操作按钮居中
        remove_btn = QPushButton('✕')
        remove_btn.setStyleSheet("""
            QPushButton { color: white; font-weight: bold; font-size: 12px; background-color: #2D2D2D; border: none; border-radius: 10px; padding: 5px; }
            QPushButton:hover { background-color: #D32F2F; }
            QPushButton:pressed { background-color: #B71C1C; }
        """)
        remove_btn.setFixedSize(16, 16)
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.addWidget(remove_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        self.task_list.setCellWidget(row_count, 2, btn_widget)

        remove_btn.clicked.connect(lambda: self.remove_task(row_count, timer))

        # 存储任务时间到QTableWidgetItem对象和是否后台运行的状态的映射关系
        self.timer_to_task[task_time] = (row_count, timer, checkbox)








    def remove_task(self, task_time, timer):
        # 停止定时器
        timer.stop()
        
        # 从映射关系中获取行索引
        row_index = self.timer_to_task[task_time][0]

        # 移除表格行
        self.task_list.removeRow(row_index)

        # 删除映射和定时器
        del self.timer_to_task[task_time]
        del self.timers[task_time]

        # 更新行索引映射，因为删除行后，所有后续行的索引都会减少
        tasks_to_update = {k: v for k, v in self.timer_to_task.items() if v[0] > row_index}
        for key in tasks_to_update:
            self.timer_to_task[key] = (self.timer_to_task[key][0] - 1, self.timer_to_task[key][1], self.timer_to_task[key][2])



    def finish_task(self, task_time):
        if task_time in self.timers:
            timer = self.timers[task_time]
            self.remove_task(task_time, timer)
            self.show_auto_close_message(f"任务 {task_time} 执行完毕并已从列表中移除。")
    def show_auto_close_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("任务完成")
        msg.setText(message)
        msg.show()
        QTimer.singleShot(1000, msg.close)  # 设置定时器在1000毫秒（1秒）后关闭消息框







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

    def execute_commands(self, task_time):
        if task_time in self.timers:
            item, timer, checkbox = self.timer_to_task[task_time]
            if checkbox.isChecked():
                self.hide()  # 隐藏窗口，不关闭程序
                print(f"任务 {task_time} 将在后台运行.")
                print(f"开始执行ADB命令序列...")
                self.wake_up_device()
                QTimer.singleShot(2000, self.swipe_up)
                QTimer.singleShot(4000, self.close_app)
                QTimer.singleShot(6000, self.open_app)
                QTimer.singleShot(10000, self.wake_up_device)
                QTimer.singleShot(12000, lambda: self.finish_task(task_time))
            else:
                print(f"呼出应用程序并执行任务 {task_time}...")
                self.show()
                print(f"开始执行ADB命令序列...")
                self.wake_up_device()
                QTimer.singleShot(2000, self.swipe_up)
                QTimer.singleShot(4000, self.close_app)
                QTimer.singleShot(6000, self.open_app)
                QTimer.singleShot(10000, self.wake_up_device)
                QTimer.singleShot(12000, lambda: self.finish_task(task_time))





    



                



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
    adb_control_app = ADBControlApp()
    adb_control_app.show()
    app.exec_()

if __name__ == '__main__':
    main()
