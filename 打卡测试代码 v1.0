import subprocess
import time

device_id = "0123456789ABCDEF"
package_name = "com.ss.android.lark"
activity_name = "com.ss.android.lark.main.app.MainActivity"

def adb_command(command):
    # 使用指定的设备ID发送ADB命令
    subprocess.run(["adb", "-s", device_id, "shell", command], capture_output=True)

def close_app():
    # 模拟按下HOME键，相当于退出当前应用
    adb_command("input keyevent KEYCODE_HOME")

def open_app():
    # 启动特定的应用
    adb_command(f"am start -n {package_name}/{activity_name}")

def test_app_control():
    print("Closing app...")
    close_app()
    time.sleep(5)  # 等待5秒
    print("Re-opening app...")
    open_app()
    print("Test completed. Check your device to see if the app was closed and reopened.")

if __name__ == "__main__":
    test_app_control()
