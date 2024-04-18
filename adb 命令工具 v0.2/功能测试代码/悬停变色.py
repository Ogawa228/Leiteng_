import sys
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class HoverEffect(QObject):
    def eventFilter(self, obj, event):
        # 检测鼠标悬停事件
        if event.type() == QEvent.Enter:
            # 保存原始样式，并添加悬停背景色
            if not hasattr(obj, 'original_style'):
                obj.original_style = obj.styleSheet()
            hover_style = obj.original_style + " background-color: #e0ffff;"  # Light Cyan on hover
            obj.setStyleSheet(hover_style)
        elif event.type() == QEvent.Leave:
            # 恢复到原始样式
            if hasattr(obj, 'original_style'):
                obj.setStyleSheet(obj.original_style)
        return super().eventFilter(obj, event)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Hover Effect with Event Filter')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()
        self.hoverEffect = HoverEffect()

        # 创建按钮和标签，并设置基本样式
        btn = QPushButton('Hover Over Me', self)
        btn.setStyleSheet("background-color: white; border: 2px solid black; padding: 10px;")
        btn.installEventFilter(self.hoverEffect)

        lbl = QLabel('Hover Over Me Too', self)
        lbl.setStyleSheet("background-color: white; border: 2px solid black; padding: 10px;")
        lbl.installEventFilter(self.hoverEffect)

        layout.addWidget(btn)
        layout.addWidget(lbl)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
