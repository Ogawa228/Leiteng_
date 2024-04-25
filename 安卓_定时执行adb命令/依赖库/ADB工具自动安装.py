import subprocess
import sys
import platform
from PyQt5.QtWidgets import QMessageBox
import urllib.request
import os

class ADBInstaller:
    def __init__(self):
        self.adb_urls = {
            'Windows': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip',
            'macOS': 'https://dl.google.com/android/repository/platform-tools-latest-darwin.zip',
            'Linux': 'https://dl.google.com/android/repository/platform-tools-latest-linux.zip'
        }

    def detect_os(self):
        os_type = platform.system()
        if os_type == 'Darwin':
            return 'macOS'
        elif os_type == 'Windows':
            return 'Windows'
        elif os_type == 'Linux':
            return 'Linux'
        else:
            return None

    def download_adb(self, os_type):
        url = self.adb_urls.get(os_type)
        if not url:
            return False
        try:
            adb_zip_path = 'platform-tools-latest.zip'
            urllib.request.urlretrieve(url, adb_zip_path)
            return adb_zip_path
        except Exception as e:
            print(f"下载ADB失败: {str(e)}")
            return None

    def install_adb(self, zip_path):
        # 这里可以解压ZIP文件并执行安装逻辑，具体实现视操作系统而定
        # 简单示例，更多的文件处理和环境配置需要具体实现
        try:
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('./platform-tools')
            os.remove(zip_path)  # 删除下载的ZIP文件
            return True
        except Exception as e:
            print(f"安装ADB失败: {str(e)}")
            return False

    def offer_installation(self):
        os_type = self.detect_os()
        reply = QMessageBox.question(None, "安装ADB", f"检测到您的操作系统为 {os_type}，是否尝试自动安装ADB？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            zip_path = self.download_adb(os_type)
            if zip_path and self.install_adb(zip_path):
                QMessageBox.information(None, "安装成功", "ADB安装成功！")
            else:
                QMessageBox.warning(None, "安装失败", "自动安装ADB失败，请手动安装。")
        else:
            QMessageBox.information(None, "手动安装", "请访问 https://developer.android.com/studio/releases/platform-tools 获取ADB安装包。")