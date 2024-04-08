from PyQt5.QtGui import QPalette, QBrush, QColor, QLinearGradient

class StyleManager:
    @staticmethod
    def applyStyle(widget):
        # 设置渐变色背景
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0.0, QColor("#5EFCE8"))
        gradient.setColorAt(1.0, QColor("#736EFE"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        widget.setPalette(palette)

        # 设置控件样式
        widget.setStyleSheet("""
        * {
            font-weight: bold;
        }
        QPushButton {
            background-color: #ABDCFF;
            border: 2px solid #555555;  # 加粗边框
            border-radius: 10px;  # 圆角边框
            color: black;  # 确保按钮文本颜色可见
            padding: 15px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            margin: 4px 2px;
        }
        QLineEdit, QComboBox, QDateTimeEdit {
            padding: 4px;
            margin: 2px 2px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        """)
