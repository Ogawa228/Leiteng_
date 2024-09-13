from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
import subprocess
import threading
import time
from PyQt5.QtWidgets import QMessageBox
from 依赖库.ADB工具自动安装 import ADBInstaller
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QListWidget


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
    
    return None, None  # 返回空的元组如果没有找到前台活动







class CommandDetector(QObject):
    new_command_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.adb_process = None
        self.is_listening = False
        self.devices = self.get_connected_devices()

    def show_control_dialog(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('命令检测控制')
        self.dialog.resize(400, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel("选择设备并准备开始监听...")
        layout.addWidget(self.status_label)

        # 设备选择下拉菜单
        self.device_combo = QComboBox()
        for device in self.devices:
            self.device_combo.addItem(device)
        layout.addWidget(self.device_combo)

        start_button = QPushButton("开始监听")
        start_button.clicked.connect(self.start_listening)
        layout.addWidget(start_button)

        stop_button = QPushButton("停止监听")
        stop_button.clicked.connect(self.stop_listening)
        layout.addWidget(stop_button)

        self.dialog.setLayout(layout)
        self.dialog.exec_()

    def get_connected_devices(self):
        try:
            output = subprocess.check_output(['adb', 'devices'], encoding='utf-8').strip()
            lines = output.splitlines()[1:]  # 忽略首行的标题信息
            devices = [line.split('\t')[0] for line in lines if "device" in line.split('\t')[1]]
            return devices
        except subprocess.CalledProcessError:
            QMessageBox.warning(None, "ADB错误", "无法获取设备列表。请确保ADB正常运行。")
            return []

    def start_listening(self):
        selected_device = self.device_combo.currentText()
        if not selected_device:
            QMessageBox.warning(None, "设备选择错误", "未选择设备或未连接设备。")
            return

        self.status_label.setText(f"正在监听设备: {selected_device}...")
        self.is_listening = True
        self.adb_process = subprocess.Popen(['adb', '-s', selected_device, 'logcat'], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE, bufsize=1)
        threading.Thread(target=self.process_events, daemon=True).start()

    def stop_listening(self):
        if self.is_listening:
            self.status_label.setText("监听已停止。")
            self.is_listening = False
            if self.adb_process:
                self.adb_process.terminate()

    def process_events(self):
        try:
            while self.is_listening:
                line = self.adb_process.stdout.readline()
                if 'MotionEvent' in line or "KeyEvent" in line:
                    command = self.convert_to_command(line)
                    self.new_command_signal.emit(command)
        except Exception as e:
            self.status_signal.emit(f"监听错误: {str(e)}")

    def convert_to_command(self, log_line):
        parts = log_line.split()
        command = "未识别的事件类型"

        if "MotionEvent" in log_line:
            action = parts[1]  # 示例中假设动作类型在第二个位置
            x, y = parts[2], parts[3]  # 示例中假设坐标在第三和第四位置

            if "ACTION_DOWN" in action:
                command = f"adb shell input tap {x} {y}"
            elif "ACTION_MOVE" in action:
                x_end, y_end = parts[4], parts[5]  # 假设结束坐标在第五和第六位置
                command = f"adb shell input swipe {x} {y} {x_end} {y_end}"
            elif "ACTION_LONG_PRESS" in action:
                command = f"adb shell input swipe {x} {y} {x} {y} 1000"  # 长按1秒

        elif "KeyEvent" in log_line:
            key_code = parts[1]  # 假设键码在第二个位置
            command = f"adb shell input keyevent {key_code}"

        elif "input" in log_line and "text" in parts:
            text_index = parts.index("text") + 1  # 文本通常在"text"关键字后
            text = parts[text_index]
            command = f"adb shell input text '{text}'"

        elif "rotation" in log_line:
            rotation = parts[1]  # 假设旋转角度在第二个位置
            command = f"adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:{rotation}"

        elif "am start" in log_line or "Starting" in log_line:
            for part in parts:
                if part.startswith("cmp="):
                    component = part.split("=")[1]  # 获取组件名称，格式通常为 package_name/activity_name
                    package_name, activity_name = component.split("/")
                    command = f"adb shell am start -n {package_name}/{activity_name}"
                    break

        return command


