import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
import re
import os
from collections import defaultdict


class MercenaryCompetitionManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("雇佣兵比赛管理工具")
        self.setGeometry(100, 100, 600, 600)

        self.status_text = QTextEdit(self)
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(100)

        self.analyze_button = QPushButton("比赛数据分析", self)
        self.apply_apple_style(self.analyze_button)
        self.analyze_button.clicked.connect(self.show_analyze_ui)

        self.screen_button = QPushButton("比赛人员筛查", self)
        self.apply_apple_style(self.screen_button)
        self.screen_button.clicked.connect(self.show_screen_ui)

        layout = QVBoxLayout()
        layout.addWidget(self.status_text)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.screen_button)

        self.function_widget = QWidget(self)
        self.function_layout = QVBoxLayout(self.function_widget)
        layout.addWidget(self.function_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.analyze_ui = None
        self.screen_ui = None

        self.show_analyze_ui()
        self.save_path = ""

    def apply_apple_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 14px;
                font-family: 'Helvetica';
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

    def log_status(self, message):
        self.status_text.append(message)

    def show_analyze_ui(self):
        self.clear_function_widget()
        self.analyze_ui = AnalyzeUI(self.function_widget, self)
        self.function_layout.addWidget(self.analyze_ui)

    def show_screen_ui(self):
        self.clear_function_widget()
        self.screen_ui = ScreenPersonnelUI(self.function_widget, self)
        self.function_layout.addWidget(self.screen_ui)

    def clear_function_widget(self):
        for i in reversed(range(self.function_layout.count())):
            widget = self.function_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()


class AnalyzeUI(QWidget):
    def __init__(self, parent, ui):
        super().__init__(parent)
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        button = QPushButton("选择文件", self)
        self.ui.apply_apple_style(button)
        button.clicked.connect(self.select_files)
        layout.addWidget(button)

        self.setLayout(layout)

    def select_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "Text files (*.txt)")
        if file_paths:
            self.ui.log_status(f"选择的文件路径: {file_paths}")
            for file_path in file_paths:
                log_data = DataAnalyzer.analyze_file(file_path, self.ui)
                ExcelSaver.save_to_excel(log_data, self.ui, file_path)


class ScreenPersonnelUI(QWidget):
    def __init__(self, parent, ui):
        super().__init__(parent)
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        button = QPushButton("选择文件进行筛查", self)
        self.ui.apply_apple_style(button)
        button.clicked.connect(self.select_file)
        layout.addWidget(button)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            self.ui.log_status(f"选择的文件路径: {file_path}")
            PersonnelScreener.screen_personnel(file_path, self.ui)


class DataAnalyzer:
    @staticmethod
    def analyze_file(file_path, ui):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()

        log_data = []
        hit_data = defaultdict(list)
        join_data = []
        leave_data = []
        round_end_data = []
        map_start_data = []
        server_settings_data = []

        patterns = [
            (re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([^\]]+)\] has joined the game with ID: (\d+) and IP: ([\d.]+)'), 'join'),
            (re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([^\]]+)\] has left the game with ID: (\d+) and IP: ([\d.]+)'), 'leave'),
            (re.compile(r'(\d{2}:\d{2}:\d{2}) - The round (\d+) has ended'), 'round_end'),
            (re.compile(r'(\d{2}:\d{2}:\d{2}) - The map has started: (.+)'), 'map_start'),
            (re.compile(r'(\d{2}:\d{2}:\d{2}) - Dynamic server settings have been (updated|reset)'), 'server_settings'),
            (re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([^\]]+)\] has hit \[([^\]]+)\] \(([^,]+), (\d+) DMG\)'), 'hit')
        ]

        for line in data:
            matched = False
            for pattern, log_type in patterns:
                match = pattern.match(line)
                if match:
                    matched = True
                    log_data.append((log_type, match.groups()))
                    if log_type == 'hit':
                        time, attacker, victim, weapon, dmg = match.groups()
                        hit_data[attacker].append((weapon, int(dmg)))
                        ui.log_status(f"Hit: {attacker} hit {victim} with {weapon} for {dmg} DMG")
                    elif log_type == 'join':
                        join_data.append(match.groups())
                    elif log_type == 'leave':
                        leave_data.append(match.groups())
                    elif log_type == 'round_end':
                        round_end_data.append(match.groups())
                    elif log_type == 'map_start':
                        map_start_data.append(match.groups())
                    elif log_type == 'server_settings':
                        server_settings_data.append(match.groups())
                    break
            if not matched:
                ui.log_status(f"未匹配行: {line.strip()}")

        ui.log_status(f"分析完成，共处理{len(log_data)}条记录")
        return {
            "hit_data": hit_data,
            "join_data": join_data,
            "leave_data": leave_data,
            "round_end_data": round_end_data,
            "map_start_data": map_start_data,
            "server_settings_data": server_settings_data
        }


class ExcelSaver:
    @staticmethod
    def save_to_excel(data, ui, file_path):
        hit_data = data['hit_data']
        if not hit_data:
            ui.log_status(f"文件 {file_path} 中没有可用的 hit 数据")
            return

        data_for_excel = []
        for player, hits in hit_data.items():
            total_dmg = sum(dmg for weapon, dmg in hits)
            weapon_dmg = defaultdict(int)
            for weapon, dmg in hits:
                weapon_dmg[weapon] += dmg
            most_used_weapon = max(weapon_dmg, key=weapon_dmg.get)
            guid = f"with ID:{file_path.split('/')[-1].split('.')[0]}"
            data_for_excel.append([player, len(hits), total_dmg, guid, most_used_weapon])

        df = pd.DataFrame(data_for_excel, columns=['Player ID', 'Hit', 'DMG', 'ID', 'Most Used Weapon'])
        if not ui.save_path:
            ui.save_path = QFileDialog.getExistingDirectory(ui, "选择保存路径")
        if ui.save_path:
            base_name = os.path.basename(file_path).replace(".txt", ".xlsx")
            output_path = os.path.join(ui.save_path, base_name)
            df.to_excel(output_path, index=False)
            QMessageBox.information(ui, "完成", "数据分析结果已保存至: " + output_path)
            ui.log_status(f"数据保存至: {output_path}")
        else:
            ui.log_status("保存路径未选择")


class PersonnelScreener:
    @staticmethod
    def screen_personnel(file_path, ui):
        # 这里添加具体的人员筛查逻辑
        ui.log_status(f"人员筛查完成，文件路径: {file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MercenaryCompetitionManager()
    main_window.show()
