from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtWidgets import QPushButton, QLineEdit, QStackedWidget, QLabel
from PyQt5.QtGui import QPalette, QBrush, QColor, QLinearGradient

class StyleManager(QObject):
    def __init__(self):
        super().__init__()

    def applyStyle(self, widget):
        # 实例方法：根据控件类型应用相应的样式
        if isinstance(widget, QPushButton):
            self.applyButtonAndLabelStyle(widget)
        elif isinstance(widget, QLineEdit):
            self.applyLineEditStyle(widget)
        elif isinstance(widget, QStackedWidget):
            self.applyStackedWidgetStyle(widget)
        elif isinstance(widget, QLabel):
            self.applyButtonAndLabelStyle(widget)
        else:
            self.applyDefaultStyle(widget)
        widget.installEventFilter(self)  # 使用实例方法安装事件过滤器


    def applyButtonAndLabelStyle(self, widget):
        widget.setStyleSheet("""
        QPushButton, QLabel {
            background-color: #FFFFFF;
            border: 0px solid #A1A1A1;
            border-radius: 5px;
            color: #000000;
            padding: 10px 20px;
            margin: 4px 2px;
        }
        QPushButton:hover, QLabel:hover {
            background-color: #F0F0F7;
        }
        """)

    def applyLineEditStyle(self, lineEdit):
        # 设置 QLineEdit 的样式
        lineEdit.setStyleSheet("""
        QLineEdit {
            font-family: "PingFang SC";  # 使用苹方字体
            font-size: 16px;  # 设置字体大小为16号
            padding: 4px;
            margin: 2px 2px;
            border: 1px solid #D1D1D1;
            border-radius: 4px;
            background-color: #FFFFFF;
        }
        QLineEdit:focus {
            border: 2px solid #007AFF;
        }
        """)

    def applyStackedWidgetStyle(self, stackedWidget):
        # 设置 QStackedWidget 的渐变背景色
        gradient = QLinearGradient(0, 0, 0, stackedWidget.height())
        gradient.setColorAt(0.0, QColor("#FFFFFF"))
        gradient.setColorAt(1.0, QColor("#F0F0F7"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        stackedWidget.setPalette(palette)

    def applyDefaultStyle(self, widget):
        # 应用默认风格的样式
        widget.setStyleSheet("""
        QWidget {
            font-size: 16px;  # 设置字体大小为16号
            background-color: #FFFFFF;  # 白色背景
            color: #000000;  # 黑色文字
        }
        """)

    def eventFilter(self, obj, event):
        if isinstance(obj, (QPushButton, QLabel)):
            if event.type() == QEvent.Enter:
                # 保存原始样式，如果还未保存
                if not hasattr(obj, 'original_style'):
                    obj.original_style = obj.styleSheet()
                # 在鼠标悬停时只改变背景颜色
                obj.setStyleSheet(obj.original_style + " background-color: #e0ffff;")
            elif event.type() == QEvent.Leave:
                # 鼠标离开时恢复原始样式
                if hasattr(obj, 'original_style'):
                    obj.setStyleSheet(obj.original_style)
        return super().eventFilter(obj, event)

