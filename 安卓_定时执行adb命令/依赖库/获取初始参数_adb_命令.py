import subprocess
import time

def get_adb_version():
    try:
        adb_version_output = subprocess.check_output(["adb", "version"], encoding='utf-8')
        return adb_version_output.strip()
    except subprocess.CalledProcessError:
        return None

def get_connected_devices():
    try:
        devices_output = subprocess.check_output(["adb", "devices"], encoding='utf-8').strip()
        devices = devices_output.split('\n')[1:]  # Skip the first line
        return devices
    except subprocess.CalledProcessError:
        return []

def get_android_version(device_id):
    try:
        android_version_output = subprocess.check_output(["adb", "shell", "getprop", "ro.build.version.release"], encoding='utf-8')
        return android_version_output.strip()
    except subprocess.CalledProcessError as e:
        print(f"无法获取Android版本信息：{e}")
        return None


def get_foreground_activity_with_wakeup(device_id):
    # 尝试唤醒设备
    wake_up_device(device_id)

    # 等待设备唤醒
    time.sleep(2)  # 给予设备足够的时间唤醒

    # 执行上滑操作以进入主界面
    swipe_to_home_screen(device_id)

    # 获取前台活动的应用信息
    return get_foreground_activity(device_id)

def wake_up_device(device_id):
    try:
        subprocess.run(["adb", "-s", device_id, "shell", "input", "keyevent", "KEYCODE_WAKEUP"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"设备唤醒失败: {e}")

def swipe_to_home_screen(device_id):
    try:
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "400", "2000", "400", "500"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"上滑操作失败: {e}")

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