from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from parameter_manager import save_parameters_to_file  # 确保这个函数已经定义
from  style_manager import StyleManager  # 确保正确导入StyleManager
class SaveParameters(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("保存参数")
        self.init_ui()
        StyleManager.applyStyle(self)  # 应用样式
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)