from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from style_manager import StyleManager  # 确保正确导入StyleManager
from 功能管理 import 时间功能
from  功能管理.时间功能 import DateTimeParametersDialog

class AutoExecuteADBCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自动执行ADB命令设置")
        self.init_ui()

    
    def init_ui(self):
        mainLayout = QVBoxLayout(self)  # 主布局为垂直布局
        
        # 第一排的水平布局
        firstRowLayout = QHBoxLayout()
        
        # 设置时间参数按钮
        self.openDateTimeParametersButton = QPushButton("设置时间参数", self)
        self.openDateTimeParametersButton.clicked.connect(self.openDateTimeParametersDialog)
        firstRowLayout.addWidget(self.openDateTimeParametersButton)
        
        # ADB命令设置按钮
        self.adbCommandSettingsButton = QPushButton("ADB命令设置", self)
        # 这里暂时不连接到具体的函数
        firstRowLayout.addWidget(self.adbCommandSettingsButton)
        
        # 将第一排的布局添加到主布局
        mainLayout.addLayout(firstRowLayout)
        
        # 执行按钮，直接添加到主布局，会自动排列到下一行
        self.executeButton = QPushButton("执行", self)
        # 这里暂时不连接到具体的函数
        mainLayout.addWidget(self.executeButton, 0, Qt.AlignCenter)  # 使用Qt.AlignCenter来居中按钮
        
        self.setLayout(mainLayout)  # 设置对话框的布局为主布局

    
    
    def openDateTimeParametersDialog(self):
        # 实例化并显示DateTimeParametersDialog
        dateTimeDialog = DateTimeParametersDialog(self)
        dateTimeDialog.exec_() 