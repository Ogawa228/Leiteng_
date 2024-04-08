from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDateTimeEdit, QComboBox, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QDateTime, QTimeZone
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import os
import pickle
from style_manager import StyleManager
from 参数 import parameter_manager
from 参数.parameter_manager import save_parameters_to_file

class DateTimeParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置时间参数")
        self.init_ui()
        StyleManager.applyStyle(self)  # 应用样式
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        
        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setCalendarPopup(True)  # 允许使用日历弹窗选择日期
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())  # 设置为当前日期和时间
        # 设置显示格式以包括日期和时间
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.layout.addWidget(self.dateTimeEdit)
   
        
        # 时区选择
        self.timeZoneComboBox = QComboBox(self)
        time_zones = [str(tz) for tz in QTimeZone.availableTimeZoneIds()]
        self.timeZoneComboBox.addItems(time_zones)
        self.timeZoneComboBox.addItems([tz.data().decode() for tz in QTimeZone.availableTimeZoneIds()])
        self.timeZoneComboBox.setCurrentText("Asia/Shanghai")
        self.layout.addWidget(self.timeZoneComboBox)
        
        # 循环规则选择
        self.repeatRuleComboBox = QComboBox(self)
        self.repeatRuleComboBox.addItems(["单次", "每天", "每周", "工作日", "节假日"])
        self.layout.addWidget(self.repeatRuleComboBox)
        
        # 参数组选择
        self.groupComboBox = QComboBox(self)
        self.load_existing_groups()
        self.layout.addWidget(self.groupComboBox)

        # 保存按钮
        self.saveButton = QPushButton("保存", self)
        self.saveButton.clicked.connect(self.save_parameters)
        self.layout.addWidget(self.saveButton)

       
        self.setLayout(self.layout)




    
    def load_existing_groups(self):
        file_name = '用户配置信息.pkl'
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                data = pickle.load(file)
            groups = list(data.keys())
        else:
            groups = []
        groups.append("新建参数组...")
        self.groupComboBox.addItems(groups)
        
    def save_parameters(self):
        selected_group = self.groupComboBox.currentText()
        if selected_group == "新建参数组...":
            # 弹出对话框让用户输入新的组名
            new_group, ok = QInputDialog.getText(self, "新建参数组", "输入新的参数组名称:")
            if ok and new_group:
                selected_group = new_group
            else:
                return  # 用户取消或未输入名称，不继续执行保存
        
        # 收集设置的时间参数
        params = {
            "dateTime": self.dateTimeEdit.dateTime().toString(Qt.ISODate),
            "timeZone": self.timeZoneComboBox.currentText(),
            "repeatRule": self.repeatRuleComboBox.currentText(),
        }
        
        # 使用用户选定或新建的参数组名来保存时间参数
        if save_parameters_to_file(params, selected_group):
            QMessageBox.information(self, "保存成功", "时间参数已保存至 \"" + selected_group + "\"")
        else:
            QMessageBox.warning(self, "保存失败", "无法保存时间参数")