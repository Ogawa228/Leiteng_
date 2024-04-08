from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QMessageBox
import pickle

class ParameterDetailsViewer(QDialog):
    def __init__(self, parent=None, group_name=""):
        super().__init__(parent)
        self.group_name = group_name
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"参数详情 - {self.group_name}")
        self.details_text_edit = QTextEdit(self)
        self.details_text_edit.setReadOnly(True)  # 设置为只读
        
        # 设置样式
        self.details_text_edit.setStyleSheet("""
        QTextEdit {
            background-color: #9de1f6;
            border-radius: 15px; 
            font-family: 'Microsoft YaHei'; 
            font-size: 15pt; 
            line-height: 25px;
            padding: 25px;
        }
        table { 
            border-collapse: separate; 
            border-spacing: 0 15px; 
            width: 100%;
        }
        td, th {
            padding: 10px 20px; 
            text-align: left;
            border-bottom: 2px dashed #CCC;
        }
        tr:nth-child(even) {background-color: #f2f2f2;}
        tr:hover {background-color: #f5f5f5;}
        th {
            background-color: #f9f9f9; 
            color: black;
            border-bottom: 2px dashed #CCC;
        }
        """)
        
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.details_text_edit)
        self.load_and_display_parameters_details()
    
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
        # 使用HTML表格来展示参数详情
        details_html = f"""
        <center><b><h3>参数详情 - {self.group_name}</h3></b></center>
        <br>
        <table>
            <tr>
                <th>参数名称</th>
                <th>参数内容</th>
                <th>注释</th>
            </tr>
        """
        
        # 示例数据，根据实际需要调整
        details_list = [
            ("设备ID (device_id)", params['device_id'], "设备ID是用于标识连接的Android设备的标识符"),
            ("应用包名 (package_name)", params['package_name'], "应用包名是Android应用的唯一标识，通常由开发者提供"),
            ("活动名 (activity_name)", params['activity_name'], "活动名通常对应应用中的一个界面或操作"),
            ("ADB版本 (adb_version)", params.get('adb_version', 'N/A'), "ADB版本是Android Debug Bridge的版本号，用于开发和调试"),
            ("Android版本 (android_version)", params.get('android_version', 'N/A'), "Android版本是设备操作系统的版本号")
        ]
        
        for name, content, comment in details_list:
            details_html += f"""
                <tr>
                    <td>{name}</td>
                    <td>{content}</td>
                    <td>{comment}</td>
                </tr>
            """
        details_html += "</table>"
        
        self.details_text_edit.setHtml(details_html)
