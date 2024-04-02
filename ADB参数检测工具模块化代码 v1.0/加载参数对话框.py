##加载参数对话框.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox
import os
import pickle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTextEdit,QDialog,QApplication

class LoadParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择应用名")
        self.init_ui()
        self.populate_combo_box()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.group_combo_box = QComboBox(self)
        self.group_combo_box.setEditable(True)
        self.group_combo_box.setInsertPolicy(QComboBox.NoInsert)

        self.load_button = QPushButton("加载参数", self)
        self.load_button.clicked.connect(self.load_parameters)

        self.delete_button = QPushButton("删除参数", self)
        self.delete_button.clicked.connect(self.delete_parameters)

        self.view_button = QPushButton("查看参数详情", self)
        self.view_button.clicked.connect(self.view_parameters_details)

        self.layout.addWidget(QLabel("请选择要加载的应用名："))
        self.layout.addWidget(self.group_combo_box)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.view_button)

    def populate_combo_box(self):
        self.group_combo_box.clear()
        try:
            with open('用户配置信息.pkl', 'rb') as f:
                data = pickle.load(f)
                for group_name in data.keys():
                    self.group_combo_box.addItem(group_name)
        except Exception as e:
            QMessageBox.error(self, "错误", "无法加载参数文件。")

    def load_parameters(self):
        group_name = self.group_combo_box.currentText()
        if group_name:
            self.parent().loaded_parameters(group_name)
            self.accept()
        else:
            QMessageBox.warning(self, "警告", "请选择一个应用名。")

    def delete_parameters(self):
        group_name = self.group_combo_box.currentText()
        if group_name:
            try:
                with open('用户配置信息.pkl', 'rb') as f:
                    data = pickle.load(f)
                if group_name in data:
                    del data[group_name]
                    with open('用户配置信息.pkl', 'wb') as f:
                        pickle.dump(data, f)
                    QMessageBox.information(self, "成功", "参数已删除。")
                    self.populate_combo_box()
                else:
                    QMessageBox.warning(self, "警告", "找不到指定的应用名。")
            except Exception as e:
                QMessageBox.error(self, "错误", "删除参数时发生错误。")
        else:
            QMessageBox.warning(self, "警告", "请选择一个应用名。")

    def view_parameters_details(self):
        group_name = self.group_combo_box.currentText()
        if group_name:
            try:
                with open('用户配置信息.pkl', 'rb') as f:
                    data = pickle.load(f)
                if group_name in data:
                    params = data[group_name]

                    # 创建一个富文本编辑器来显示参数详情
                    details_text_edit = QTextEdit(self)
                    details_text_edit.setReadOnly(True)  # 设置为只读

                    # 设置字体、大小和行间距
                    details_text_edit.setStyleSheet("""
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
                        border-bottom: 2px dashed #CCC; /* 添加虚线边框到单元格底部 */
                    }
                    tr:nth-child(even) {background-color: #f2f2f2;}
                    tr:hover {background-color: #f5f5f5;}
                    th {
                        background-color: #f9f9f9; 
                        color: black;
                        border-bottom: 2px dashed #CCC; /* 表头底部使用更粗的虚线 */
                    }
                """)


                    # 使用HTML表格来展示参数详情
                    details_html = f"""
                    <center><b><h3>参数详情 - {group_name}</h3></b></center>
                    <br>
                    <table>
                        <tr>
                            <th>参数名称</th>
                            <th>参数内容</th>
                            <th>注释</th>
                        </tr>
                    """

                    # 添加每一行参数的HTML代码
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

                    details_text_edit.setHtml(details_html)

                    # 显示富文本编辑器对话框
                    dialog = QDialog(self)
                    dialog.setWindowTitle("参数详情")
                    width = 800  # 直接指定宽度
                    height = int(width / 1.618)  # 根据黄金比例计算高度
                    dialog.setFixedSize(width, height)
                    dialog.setLayout(QVBoxLayout())
                    dialog.layout().addWidget(details_text_edit)
                    dialog.exec_()
                else:
                    QMessageBox.critical(self, "警告", "找不到指定的应用名。")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载参数详情时发生错误: {e}")
        else:
            QMessageBox.critical(self, "警告", "请选择一个应用名。")





    def exec_(self):
        # 在对话框显示之前填充下拉菜单
        self.populate_combo_box()
        super().exec_()