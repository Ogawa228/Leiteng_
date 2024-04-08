from PyQt5.QtWidgets import QApplication
from 程序主界面 import ADBParametersDialog

class Application(QApplication):
    def __init__(self):
        # 正确地传递命令行参数给 QApplication
        argv = ['main.py'] # 这里的参数可以根据需要修改
        super().__init__(argv)
        self.dialog = ADBParametersDialog()
        self.dialog.show()

if __name__ == "__main__":
    app = Application()
    app.exec_()