from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
import subprocess
import threading
import time
from PyQt5.QtWidgets import QMessageBox
from 依赖库.ADB工具自动安装 import ADBInstaller


#自动检测设备参数
def get_adb_info():
    adb_installed = False
    adb_version = ""
    device_id = ""
    package_name = "未检测到"
    activity_name = "未检测到"
    android_version = ""

    try:
        # 检查ADB是否安装，并获取ADB版本
        try:
            adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8').strip()
            adb_installed = True
            adb_version = adb_version_output.splitlines()[0]
        except subprocess.CalledProcessError:
            installer = ADBInstaller()
            installer.offer_installation()
            return None

        # 获取连接的设备列表
        devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip()
        devices_lines = devices_output.splitlines()[1:]  # 忽略首行的提示信息

        if not devices_lines:
            QMessageBox.warning(None, "设备连接问题", "未检测到已连接的设备或设备状态不正确。")
            return None  # 返回None或相应的值，表示没有找到设备

        if "device" not in devices_lines[0]:
            QMessageBox.warning(None, "设备连接问题", "设备可能未完全连接或未授权调试。")
            return None  # 返回None或相应的值，表示设备未授权

        device_id = devices_lines[0].split()[0]  # 获取第一个设备ID

        # 检查设备是否休眠
        device_state = subprocess.check_output(["adb", "-s", device_id, "shell", "dumpsys", "power"], encoding='utf-8').strip()
        if "mWakefulness=Awake" not in device_state:
            # 设备休眠中，发送唤醒命令
            subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_WAKEUP"])
            subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_MENU"])
            time.sleep(1)  # 等待设备唤醒

        # 获取设备的Android版本
        android_version = subprocess.check_output(["adb", "-s", device_id, "shell", "getprop", "ro.build.version.release"], encoding='utf-8').strip()

        # 获取当前前台活动的包名和活动名
        package_name, activity_name = get_foreground_activity(device_id)
        if package_name is None:
            raise Exception("无法检测到前台活动。请确保有应用在前台运行。")

    except subprocess.CalledProcessError as e:
        print("执行ADB命令出错:", e)
    except Exception as e:
        print("错误:", e)

    return device_id, package_name, activity_name, android_version, adb_installed, adb_version

def get_foreground_activity(device_id):
    try:
        dumpsys_output = subprocess.check_output(["adb", "-s", device_id, "shell", "dumpsys", "activity", "activities"], encoding='utf-8')
        for line in dumpsys_output.splitlines():
            if "mResumedActivity" in line:
                activity_info = line.split()[-2]
                package_name, activity_name = activity_info.split("/")
                return package_name, activity_name
    except subprocess.CalledProcessError:
        return None, None  # 返回空的元组如果发生错误
    


class CommandDetector(QObject):
    new_command_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.adb_process = None
        self.is_listening = False

    def show_control_dialog(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('命令检测控制')
        self.dialog.resize(300, 150)

        layout = QVBoxLayout()

        self.status_label = QLabel("准备开始监听...")
        layout.addWidget(self.status_label)

        start_button = QPushButton("开始监听", self.dialog)
        start_button.clicked.connect(self.start_listening)
        layout.addWidget(start_button)

        stop_button = QPushButton("停止监听", self.dialog)
        stop_button.clicked.connect(self.stop_listening)
        layout.addWidget(stop_button)

        self.dialog.setLayout(layout)
        self.dialog.exec_()

    def start_listening(self):
        # 检查ADB环境
        adb_info = get_adb_info()
        if adb_info is None:
            QMessageBox.warning(None, "ADB错误", "未能检测到ADB安装或设备连接。请确保ADB正常安装并连接了设备。")
            return

        # 如果设备信息有效，继续执行
        if adb_info[4]:  # 判断adb_installed是否为True
            self.status_label.setText("正在监听...")
            self.is_listening = True
            self.adb_process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE, bufsize=1)
            threading.Thread(target=self.process_events, daemon=True).start()
        else:
            QMessageBox.warning(None, "ADB错误", "ADB未安装或设备未连接。")

    def stop_listening(self):
        if self.is_listening:
            self.status_label.setText("监听已停止。")
            self.is_listening = False
            if self.adb_process:
                self.adb_process.terminate()

    def process_events(self):
        """处理从设备捕获的事件"""
        try:
            while self.is_listening:
                line = self.adb_process.stdout.readline()
                if 'MotionEvent' in line:
                    command = self.convert_to_command(line)
                    self.new_command_signal.emit(command)
        except Exception as e:
            self.status_signal.emit(f"监听错误: {str(e)}")

    def convert_to_command(self, log_line):
        """将日志行转换为ADB命令"""
        parts = log_line.split()
        x, y = parts[1], parts[2]  # 假设坐标在第2和第3位
        command = f"adb shell input tap {x} {y}"
        return f"Generated command: {command}"

