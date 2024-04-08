##加载参数按钮对话框.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox
import os
import pickle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTextEdit,QDialog,QApplication
from style_manager import StyleManager
from 按钮管理.参数详情 import ParameterDetailsViewer

class LoadParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择应用名")
        self.init_ui()
        self.populate_combo_box()
        StyleManager.applyStyle(self)  # 应用样式

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
            viewer = ParameterDetailsViewer(self, group_name=group_name)
            viewer.exec_()
        else:
            QMessageBox.warning(self, "警告", "请选择一个应用名。")





    def exec_(self):
        # 在对话框显示之前填充下拉菜单
        self.populate_combo_box()
        super().exec_()