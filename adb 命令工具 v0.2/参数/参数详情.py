from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QMessageBox
import pickle

class ParameterDetailsViewer(QDialog):
    def __init__(self, parent=None, group_name=""):
        super().__init__(parent)
        self.group_name = group_name
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"参数详情 - {self.group_name}")
        self.setStyleSheet("background-color: white")  # 对话框背景色设置为白色
        self.details_text_edit = QTextEdit(self)
        self.details_text_edit.setReadOnly(True)

        # 设置文本编辑区的样式
        self.details_text_edit.setStyleSheet("""
        QTextEdit {
            background-color: white ; /* 设置文本编辑区的背景颜色 */
            border: none; /* 移除文本编辑区的边框 */
            font-family: 'Microsoft YaHei'; /* 设置字体为微软雅黑 */
            font-size: 15pt; /* 设置字号为15磅 */
        }
        """)


        # 添加布局并将文本编辑器添加到布局中
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.details_text_edit)
        self.load_and_display_parameters_details()

        # 调整窗口大小以符合黄金比例
        width = 1080
        golden_ratio = 1.618
        height = int(width / golden_ratio)
        self.resize(width, height)
    
    def load_and_display_parameters_details(self):
        if not self.group_name:
            QMessageBox.warning(self, "警告", "请选择一个应用名。")
            return
        
        try:
            with open('用户配置信息.pkl', 'rb') as f:
                data = pickle.load(f)
            if self.group_name in data:
                params = data[self.group_name]
                # 构造HTML展示参数详情
                self.construct_details_html(params)
            else:
                QMessageBox.warning(self, "警告", "找不到指定的应用名。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载参数详情时发生错误: {e}")
    
    def construct_details_html(self, params):
        # 硬编码注释，用于展示。您可以根据需要修改这些注释
        hardcoded_comments = {
            "device_id": "设备ID是用于标识连接的Android设备的标识符",
            "package_name": "应用包名是Android应用的唯一标识，通常由开发者提供",
            "activity_name": "活动名通常对应应用中的一个界面或操作",
            "adb_version": "ADB版本是Android Debug Bridge的版本号，用于开发和调试",
            "android_version": "Android版本是设备操作系统的版本号",
            "dateTime": "日期时间是保存参数时的时间戳",
            "repeatRule":"重复规则是用于设置定时任务的规则",
            "timeZone":"时区是用于设置定时任务的时区",

        }

        # 使用HTML样式直接在内容中定义表格样式
        details_html = f"""
        <style>
        table {{
            border-collapse: collapse;  /* 所有边框合并为一个边框 */
            width: 100%;  /* 表格宽度为100% */
            border: none; /* 移除外边框 */
            margin: auto; /* 表格水平居中 */
        }}
        th, td {{
            padding: 10px;  /* 单元格内边距为10像素 */
            border: 2px solid black;  /* 单元格边框为黑色实线 */
            text-align: center;  /* 文本居中对齐 */
        }}
        th {{
            background-color: #9de1f6;  /* 标题行背景颜色为浅蓝色 */
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;  /* 偶数行背景颜色为浅灰色 */
        }}
        </style>
        <table>
        <thead>
            <tr>
                <th>参数名称</th>
                <th>参数内容</th>
                <th>注释</th>
            </tr>
        </thead>
        <tbody>
        """

        for key, value in params.items():
            # 注释是根据参数内容动态添加的
            comment = hardcoded_comments.get(key, "无注释")  # 如果没有找到注释，默认为"无注释"
            details_html += f"""
            <tr>
                <td>{key}</td>
                <td>{value}</td>
                <td>{comment}</td>
            </tr>
            """
        details_html += """
        </tbody>
        </table>
        """
        self.details_text_edit.setHtml(details_html)
