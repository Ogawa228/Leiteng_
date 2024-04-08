from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from 参数 import parameter_manager
from 参数.parameter_manager import save_parameters_to_file  # 确保这个函数已经定义



class SaveParameters(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("保存参数")
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)