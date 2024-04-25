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
        self.initial_params = initial_params
        self.parameter_file = '用户配置信息.pkl'
        self.init_ui()
        self.populate_combo_box()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("请选择或新建参数组名："))
        self.group_combo_box = QComboBox(self)
        self.group_combo_box.setEditable(True)
        self.group_combo_box.setInsertPolicy(QComboBox.NoInsert)
        self.group_combo_box.activated.connect(self.handle_combo_box_activation)
        self.layout.addWidget(self.group_combo_box)

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
            with open(self.parameter_file, 'rb') as f:
                data = pickle.load(f)
            for group_name in sorted(data):
                self.group_combo_box.addItem(group_name)
        except Exception as e:
            QMessageBox.critical(self, "错误", "无法加载参数文件：\n" + str(e))
        # 添加一个常驻的新建选项
        self.group_combo_box.addItem("新建参数组")

    def handle_combo_box_activation(self, index):
        # 检测是否选中了"新建参数组"
        selected_text = self.group_combo_box.currentText()
        if selected_text == "新建参数组":
            self.create_new_group()

    def create_new_group(self):
        group_name, ok = QInputDialog.getText(self, "新建参数组", "请输入新参数组名称:")
        if ok and group_name:
            if group_name not in self.group_combo_box.items():
                self.group_combo_box.insertItem(self.group_combo_box.count() - 1, group_name)
                self.group_combo_box.setCurrentText(group_name)
            else:
                QMessageBox.warning(self, "警告", "该参数组名已存在。")
    
    def setInitialParams(self, params):
        self.initial_params = params

    def save_parameters(self):
        group_name = self.group_combo_box.currentText().strip()  # 使用strip()移除可能的前后空格
        # 确保group_name不为空
        if not group_name:
            QMessageBox.warning(self, "警告", "参数组名不能为空。请输入一个有效的参数组名。")
            return

        # 使用从主界面传递来的参数
        params = self.initial_params if self.initial_params else {"示例参数": "默认值"}
        if save_parameters_to_file(params, group_name):
            QMessageBox.information(self, "成功", "参数已保存。")
        else:
            QMessageBox.critical(self, "失败", "保存参数失败。")
        self.populate_combo_box()

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
            response = QMessageBox.question(self, "删除参数", f"确定删除参数组 '{group_name}'？", QMessageBox.Yes | QMessageBox.No)
            if response == QMessageBox.Yes:
                if self.delete_parameters_from_file(group_name, self.parameter_file):
                    QMessageBox.information(self, "成功", "参数组已删除。")
                    self.populate_combo_box()  # 更新下拉菜单
                else:
                    QMessageBox.warning(self, "警告", "未找到指定的参数组。")
        else:
            QMessageBox.warning(self, "警告", "请选择一个有效的参数组。")

    def delete_parameters_from_file(self, group_name, file_name):
        try:
            if not os.path.exists(file_name):
                print("文件不存在")
                return False

            with open(file_name, 'rb') as f:
                data = pickle.load(f)

            # 尝试找到和删除指定的参数组
            keys_to_delete = [key for key in data if group_name in key]
            if keys_to_delete:
                for key in keys_to_delete:
                    del data[key]
                with open(file_name, 'wb') as f:
                    pickle.dump(data, f)
                return True
            else:
                return False
        except Exception as e:
            print(f"删除参数时发生错误: {e}")
            return False

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