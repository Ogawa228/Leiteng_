from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox, QInputDialog
import os
import pickle
from style_manager import StyleManager  # 确保正确导入StyleManager
from 参数.参数详情 import ParameterDetailsViewer
from 参数 import parameter_manager
from 参数.parameter_manager import save_parameters_to_file


class SaveParameters(QDialog):
    def __init__(self, parent=None, initial_params=None):
        super().__init__(parent)
        self.setWindowTitle("保存参数")
        self.initial_params = initial_params  # 初始化initial_params，即使为None
        self.init_ui()
        self.populate_combo_box()
        StyleManager.applyStyle(self)  # 应用样式

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        width = 300
        golden_ratio = 1.618
        height = int(width/golden_ratio)
        self.resize(width, height)
        
        self.layout.addWidget(QLabel("请选择要保存的参数组名："))
        self.group_combo_box = QComboBox(self)
        self.group_combo_box.setEditable(True)
        self.group_combo_box.setInsertPolicy(QComboBox.NoInsert)
        self.layout.addWidget(self.group_combo_box)

        self.new_group_button = QPushButton("新建参数组", self)
        self.new_group_button.clicked.connect(self.create_new_group)
        self.layout.addWidget(self.new_group_button)

        self.save_button = QPushButton("保存参数", self)
        self.save_button.clicked.connect(self.save_parameters)
        self.layout.addWidget(self.save_button)

        self.delete_button = QPushButton("删除参数", self)
        self.delete_button.clicked.connect(self.delete_parameters)
        self.layout.addWidget(self.delete_button)

        self.view_button = QPushButton("查看参数详情", self)
        self.view_button.clicked.connect(self.view_parameters_details)
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

    def create_new_group(self):
        group_name, ok = QInputDialog.getText(self, "新建参数组", "请输入新参数组名称:")
        if ok and group_name:
            # 这里检查是否已经存在该名称的参数组
            if group_name in self.group_combo_box.items():
                QMessageBox.warning(self, "警告", "该参数组已存在。")
                return
            self.group_combo_box.addItem(group_name)
            self.group_combo_box.setCurrentText(group_name)

    def save_parameters(self):
        group_name = self.group_combo_box.currentText()
        # 使用从主界面传递来的参数
        params = self.initial_params if self.initial_params else {"示例参数": "默认值"}
        if save_parameters_to_file(params, group_name):
            QMessageBox.information(self, "成功", "参数已保存。")
        else:
            QMessageBox.critical(self, "失败", "保存参数失败。")
        self.populate_combo_box()

    def delete_parameters(self):
        group_name = self.group_combo_box.currentText()
        if group_name:
            response = QMessageBox.question(self, "删除参数", f"确定删除参数组 '{group_name}'？", QMessageBox.Yes | QMessageBox.No)
            if response == QMessageBox.Yes:
                try:
                    with open(self.parameter_file, 'rb') as f:
                        data = pickle.load(f)
                    if group_name in data:
                        del data[group_name]
                        with open(self.parameter_file, 'wb') as f:
                            pickle.dump(data, f)
                        QMessageBox.information(self, "成功", "参数组已删除。")
                        self.populate_combo_box()
                    else:
                        QMessageBox.warning(self, "警告", "找不到指定的参数组。")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"删除参数时发生错误: {e}")
        else:
            QMessageBox.warning(self, "警告", "请选择一个有效的参数组。")

    def view_parameters_details(self):
        group_name = self.group_combo_box.currentText()
        if group_name:
            viewer = ParameterDetailsViewer(self, group_name)
            viewer.exec_()
        else:
            QMessageBox.warning(self, "警告", "请选择一个有效的参数组。")

    def exec_(self):
        self.populate_combo_box()
        super().exec_()