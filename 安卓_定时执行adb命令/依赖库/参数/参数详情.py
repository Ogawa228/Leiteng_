from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QMessageBox
import pickle

class ParameterDetailsViewer(QDialog):
    def __init__(self, parent=None, group_name=""):
        super().__init__(parent)
        self.group_name = group_name
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"参数组详情 - {self.group_name}")
        self.setStyleSheet("background-color: white; font-family: 'Microsoft YaHei'; font-size: 12pt;")
        self.details_text_edit = QTextEdit(self)
        self.details_text_edit.setReadOnly(True)

        # 设置文本编辑区的样式
        self.details_text_edit.setStyleSheet("""
        QTextEdit {
            background-color: #fff; /* 设置文本编辑区的背景颜色 */
            border: 1px solid #ccc; /* 设置边框 */
            padding: 10px; /* 设置内边距 */
        }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.details_text_edit)
        self.setLayout(layout)
        self.load_and_display_parameters_details()

        self.resize(800, 600)  # 窗口大小调整
    
    def load_and_display_parameters_details(self):
        try:
            with open('用户配置信息.pkl', 'rb') as f:
                data = pickle.load(f)
            if self.group_name in data:
                params = data[self.group_name]
                self.construct_details_html(params)
            else:
                QMessageBox.warning(self, "警告", "未找到指定的参数组。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载参数详情时发生错误: {e}")
    
    def construct_details_html(self, params):
        hardcoded_comments = {
            "device_id": "设备ID是用于标识连接的Android设备的唯一标识符。",
            "package_name": "包名用于标识Android应用程序。",
            "activity_name": "活动名是Android应用中具体界面的标识。",
            "adb_version": "ADB版本指的是安装在设备上的Android Debug Bridge版本。",
            "android_version": "Android版本指的是设备操作系统的版本号。",
            "device_model": "设备型号是设备的硬件型号。",
            "save_time": "保存时间是参数组保存到文件的时间。",
            "adb_installed": "ADB安装状态是指ADB是否已经安装在设备上。",
            "executed_commands": "执行命令是指要在设备上执行的ADB命令。",
            # 添加更多参数及其解释

        }
        details_html = "<table style='width:100%; border-collapse: collapse;'>"
        details_html += "<tr style='background-color: #ccc;'><th>参数名称</th><th>值</th><th>说明</th></tr>"
        for key, value in params.items():
            comment = hardcoded_comments.get(key, "无详细描述")
            details_html += f"<tr><td>{key}</td><td>{value}</td><td>{comment}</td></tr>"
        details_html += "</table>"
        self.details_text_edit.setHtml(details_html)
