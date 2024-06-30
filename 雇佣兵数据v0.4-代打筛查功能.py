import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
import pandas as pd
import re
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import time
import math
import pandas as pd
import re
import os
from collections import defaultdict
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from geopy.distance import geodesic
import requests
from tkinter import Tk, filedialog

class MercenaryCompetitionManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("雇佣兵比赛管理工具")
        self.setGeometry(100, 100, 600, 600)

        self.status_text = QTextEdit(self)
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(700)

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

    def get_save_path(self, default_filename):
        """
        获取保存文件路径，默认文件名为 default_filename。
        """
        save_path, _ = QFileDialog.getSaveFileName(self, "保存文件", default_filename, "Excel files (*.xlsx)")
        return save_path if save_path else None
    


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
                if log_data:
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
        button.clicked.connect(self.select_files)
        layout.addWidget(button)

        self.setLayout(layout)

    def select_files(self):
        """
        使用tkinter实现批量选择文件。
        """
        root = Tk()
        root.withdraw()  # 隐藏主窗口
        file_paths = filedialog.askopenfilenames(title="选择日志文件", filetypes=[("Text files", "*.txt")])
        if file_paths:
            self.ui.log_status(f"选择的文件路径: {file_paths}")
            PersonnelScreener.screen_personnel(file_paths, self.ui)




class DataAnalyzer:
    @staticmethod
    def read_file(file_path, ui):
        """
        读取文件内容并返回每一行的列表。
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()
        except Exception as e:
            ui.log_status(f"读取文件时出错: {str(e)}")
            return []

    @staticmethod
    def analyze_file(file_path, ui):
        """
        分析比赛数据文件，提取玩家的击中、击杀、TK相关数据，并返回比赛数据。
        """
        data = DataAnalyzer.read_file(file_path, ui)
        if not data:
            return

        # 初始化游戏会话和统计数据的结构
        game_sessions = []
        current_session = []
        player_stats = defaultdict(lambda: {'damage': 0, 'tk_damage': 0, 'received_tk_damage': 0, 'kills': 0, 'combos': 0, 'deaths': 0, 'received_combos': 0, 'k_dmg': 0, 'received_k_dmg': 0, 'team_hits': 0, 'tk_kills': 0})
        weapon_stats = defaultdict(int)
        hit_data = defaultdict(list)
        raw_data = []
        suspicious_players = defaultdict(set)

        game_started = False
        last_hit_time = defaultdict(lambda: defaultdict(int))
        last_hit_players = defaultdict(lambda: defaultdict(str))
        last_kill_time = defaultdict(int)
        combo_processed = set()

        # 定义正则表达式模式
        start_pattern = re.compile(r'\*SERVER\*.* 开 始')
        end_pattern = re.compile(r'\*SERVER\*.* 结 束')
        hit_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - (\[.*?\])?(\w+) has hit (\[.*?\])?(\w+) \(([^,]+), (\d+) DMG\)')
        kill_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - (\[.*?\])?(\w+) <img=ico_\w+> (\[.*?\])?(\w+)')
        tk_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - (\[.*?\])?(\w+) has hit teammate (\[.*?\])?(\w+) \(([^,]+), (\d+) DMG\)')

        for line in data:
            timestamp = line[:8]

            # 处理比赛开始和结束的标志
            if start_pattern.search(line) and "刷图" in line:
                continue

            if start_pattern.search(line):
                game_started = True
                ui.log_status("比赛开始标志检测到，开始分析数据")
                if current_session:
                    game_sessions.append(current_session)
                    current_session = []
                continue

            if end_pattern.search(line):
                game_started = False
                ui.log_status("比赛结束标志检测到，停止分析数据")
                if current_session:
                    game_sessions.append(current_session)
                    current_session = []
                continue

            if re.match(r'<img=ico_headshot> \[.*?\]', line):
                continue

            if game_started:
                current_session.append(line)

        if current_session:
            game_sessions.append(current_session)

        # 将每两次会话合并为一个比赛
        matches = []
        for i in range(0, len(game_sessions), 2):
            matches.append(game_sessions[i:i+2])

        if not matches:
            ui.log_status("未检测到完整的比赛")
            return

        match_data = []
        for match in matches:
            match_stats = defaultdict(lambda: {'damage': 0, 'tk_damage': 0, 'received_tk_damage': 0, 'kills': 0, 'combos': 0, 'deaths': 0, 'received_combos': 0, 'k_dmg': 0, 'received_k_dmg': 0, 'team_hits': 0, 'tk_kills': 0})
            match_hit_data = defaultdict(list)
            match_combo_data = defaultdict(int)

            for session in match:
                for line in session:
                    raw_data.append(("log", line.strip()))

                    # 处理TK（友军伤害）数据
                    tk_match = tk_pattern.match(line)
                    if tk_match:
                        time, attacker_prefix, attacker, victim_prefix, victim, weapon, dmg = tk_match.groups()
                        dmg = int(dmg)
                        attacker = (attacker_prefix or '') + attacker
                        victim = (victim_prefix or '') + victim

                        match_stats[attacker]['tk_damage'] += dmg
                        match_stats[victim]['received_tk_damage'] += dmg
                        match_stats[attacker]['team_hits'] += 1

                        next_index = session.index(line) + 1
                        if next_index < len(session):
                            next_line = session[next_index]
                            next_time = next_line[:8]
                            if next_time == time and kill_pattern.match(next_line):
                                match_stats[attacker]['tk_kills'] += 1
                                ui.log_status(f"TK Kill: {attacker} killed teammate {victim} with {weapon} for {dmg} DMG")

                        ui.log_status(f"TK Hit: {attacker} hit teammate {victim} with {weapon} for {dmg} DMG")
                        continue

                    # 处理一般击中数据
                    hit_match = hit_pattern.match(line)
                    if hit_match:
                        time, attacker_prefix, attacker, victim_prefix, victim, weapon, dmg = hit_match.groups()
                        dmg = int(dmg)
                        attacker = (attacker_prefix or '') + attacker
                        victim = (victim_prefix or '') + victim

                        match_stats[attacker]['damage'] += dmg
                        match_hit_data[attacker].append((weapon, dmg))

                        current_time = int(timestamp.replace(':', ''))

                        if last_hit_players[victim] and (current_time - last_hit_time[victim] <= 100):
                            prev_attacker = last_hit_players[victim]
                            combo_key = (prev_attacker, attacker, victim)
                            if combo_key not in combo_processed:
                                if prev_attacker != attacker:
                                    match_stats[prev_attacker]['combos'] += 1
                                    match_stats[attacker]['combos'] += 1
                                    match_stats[attacker]['k_dmg'] += dmg
                                    match_stats[victim]['received_k_dmg'] += dmg
                                    match_stats[victim]['received_combos'] += 1
                                    match_combo_data[prev_attacker] += 1
                                    match_combo_data[attacker] += 1
                                    ui.log_status(f"Combo: {prev_attacker} and {attacker} on {victim}")
                                    combo_processed.add(combo_key)

                        last_hit_time[victim] = current_time
                        last_hit_players[victim] = attacker

                        ui.log_status(f"Hit: {attacker} hit {victim} with {weapon} for {dmg} DMG")
                        continue

                    # 处理击杀数据
                    kill_match = kill_pattern.match(line)
                    if kill_match:
                        time, attacker_prefix, attacker, victim_prefix, victim = kill_match.groups()
                        attacker = (attacker_prefix or '') + attacker
                        victim = (victim_prefix or '') + victim
                        match_stats[attacker]['kills'] += 1
                        match_stats[victim]['deaths'] += 1

                        current_time = int(timestamp.replace(':', ''))
                        if current_time - last_kill_time[attacker] <= 500:
                            match_stats[attacker]['combos'] += 1
                            match_stats[attacker]['k_dmg'] += dmg
                            match_stats[victim]['received_k_dmg'] += dmg
                            match_stats[victim]['received_combos'] += 1
                            match_combo_data[attacker] += 1
                            ui.log_status(f"Streak Combo: {attacker} on {victim}")
                        last_kill_time[attacker] = current_time

                        ui.log_status(f"Kill: {attacker} killed {victim}")

                    # 处理玩家加入和离开的数据
                    join_match = re.match(r'(\d{2}:\d{2}:\d{2}) - (\S+) has joined the game with ID: (\d+) and IP: (\d+\.\d+\.\d+\.\d+)', line)
                    leave_match = re.match(r'(\d{2}:\d{2}:\d{2}) - (\S+) has left the game with ID: (\d+) and IP: (\d+\.\d+\.\d+\.\d+)', line)
                    if join_match or leave_match:
                        time, player, player_id, ip = join_match.groups() if join_match else leave_match.groups()
                        suspicious_players[player].add((player_id, ip))
                        ui.log_status(f"Player join/leave: {player} with ID: {player_id} and IP: {ip}")

            match_data.append({
                "player_stats": match_stats,
                "hit_data": match_hit_data,
                "combo_data": match_combo_data,
                "suspicious_players": suspicious_players,
                "raw_data": raw_data
            })

        # 处理可疑玩家信息
        for player, info in suspicious_players.items():
            if len(info) > 1:
                ui.log_status(f"Suspicious player: {player}, Details: {info}")

        # 处理NaN值
        for match in match_data:
            for player in match["player_stats"]:
                for key, value in match["player_stats"][player].items():
                    if isinstance(value, float) and np.isnan(value):
                        match["player_stats"][player][key] = 0

        ui.log_status("分析完成")
        return match_data




class ExcelSaver:
    @staticmethod
    def save_to_excel(matches, ui, file_path):
        if not matches:
            ui.log_status(f"文件 {file_path} 中没有可用的比赛数据")
            return

        if not ui.save_path:
            ui.save_path = QFileDialog.getExistingDirectory(ui, "选择保存路径")
        if ui.save_path:
            try:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                base_name = os.path.basename(file_path).replace(".txt", f"_{timestamp}.xlsx")
                output_path = os.path.join(ui.save_path, base_name)

                # Initialize excel_writer if not already initialized
                ui.excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
                
                for match_index, match in enumerate(matches):
                    match_name, ok = QInputDialog.getText(ui, "比赛命名", f"为第 {match_index + 1} 场比赛命名:")
                    if not ok or not match_name:
                        match_name = f"Match {match_index + 1}"

                    df = ExcelSaver.prepare_match_dataframe(match, ui)
                    df.fillna('', inplace=True)

                    sheet_name = match_name
                    df.to_excel(ui.excel_writer, index=False, sheet_name=sheet_name)

                    workbook = ui.excel_writer.book
                    worksheet = ui.excel_writer.sheets[sheet_name]

                    header_format = workbook.add_format({
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'fg_color': '#DCE6F1',
                        'border': 1,
                        'font_name': 'Helvetica',
                        'font_size': 18,
                        'align': 'center'
                    })
                    cell_format = workbook.add_format({
                        'text_wrap': True,
                        'valign': 'top',
                        'border': 1,
                        'font_name': 'Helvetica',
                        'font_size': 12,
                        'bg_color': '#FFFFFF'
                    })
                    integer_format = workbook.add_format({
                        'text_wrap': True,
                        'valign': 'top',
                        'border': 1,
                        'font_name': 'Helvetica',
                        'font_size': 12,
                        'bg_color': '#FFFFFF',
                        'num_format': '0'
                    })
                    decimal_format = workbook.add_format({
                        'text_wrap': True,
                        'valign': 'top',
                        'border': 1,
                        'font_name': 'Helvetica',
                        'font_size': 12,
                        'bg_color': '#FFFFFF',
                        'num_format': '0.00'
                    })
                    player_id_format = workbook.add_format({
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'border': 1,
                        'font_name': 'Helvetica',
                        'font_size': 16,
                        'bg_color': '#FFFFFF'
                    })
                    top_player_format = workbook.add_format({
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'border': 1,
                        'font_name': 'Helvetica',
                        'font_size': 16,
                        'bg_color': '#00bfff'
                    })

                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                        max_len = max(df[value].astype(str).map(len).max(), len(value)) + 3
                        worksheet.set_column(col_num, col_num, max_len, cell_format)
                        if value == 'Player ID':
                            worksheet.set_column(col_num, col_num, 36, cell_format)

                    for row_num in range(1, len(df) + 1):
                        worksheet.set_row(row_num, 36, cell_format)
                        player_format = player_id_format if row_num != 1 else top_player_format
                        worksheet.write(row_num, 0, df.iloc[row_num - 1, 0], player_format)
                        for col_num in range(1, len(df.columns)):
                            value = df.columns[col_num]
                            if value in ['Hit', 'Kills', 'Combos', 'Deaths', 'Received Combos', 'Team Hits', 'TK Kills']:
                                worksheet.write(row_num, col_num, df.iloc[row_num - 1, col_num], integer_format)
                            else:
                                worksheet.write(row_num, col_num, df.iloc[row_num - 1, col_num], decimal_format)

                    comments = {
                        'Player ID': '玩家的唯一标识符',
                        'Rank Score': '根据关键补刀/击中比、关键伤害比、总关键补刀次数、关键伤害量等计算的排名分数。公式：0.485 *( 0.8 * ((combo_hits_ratio + 2 * k_dmg_damage_ratio) / 2) * 100 + 2 * (k_dmg_combo_ratio - received_k_dmg_combo_ratio) + 2 * combo_count + 0.01 * k_dmg + 2 * len(hits)) + kill_death_ratio * 2 - tk_kills * 10',
                        'Hit': '玩家的击中次数',
                        'DMG': '玩家造成的总伤害量',
                        'Most Used Weapon': '玩家最常使用的武器',
                        'Combos': '玩家的关键补刀次数',
                        'Kills': '玩家的击杀次数',
                        'Deaths': '玩家的死亡次数',
                        'TK DMG': '玩家对队友造成的伤害量',
                        'Received TK DMG': '玩家受到队友的伤害量',
                        'Kill/Death Ratio': '玩家的击杀与死亡比',
                        'Combo/Hits Ratio': '玩家的关键补刀与击中比',
                        'Received Combos': '次数越多，表明走位越差',
                        'K-DMG': '和队友配合打出combo时对敌人造成的伤害量',
                        'K-DMG/DMG': '有效伤害比，越接近1表明效率越高',
                        'K-DMG/Combos': '压制情况，数字越大压制力越强，同时也是每一次关键进攻的收益比，越大关键进攻的收益率越高',
                        'Received K-DMG': '被敌人打出combo时收到的伤害量',
                        'Received K-DMG/Combos': '被压制情况，数字越大被压制的越严重',
                        'Team Hits': '砍队友的次数',
                        'TK Kills': 'TK击杀的次数'
                    }
                    for col_num, value in enumerate(df.columns.values):
                        if value in comments:
                            worksheet.write_comment(0, col_num, comments[value], {'font_size': 12, 'font_name': 'Helvetica'})

                    chart_path = ChartPlotter.plot_data(match, ui, match_name)
                    worksheet.insert_image(f'A{len(df) + 3}', chart_path, {'x_scale': 0.5, 'y_scale': 0.5})

                if ui.excel_writer:
                    ui.excel_writer.close()  # Save and close the Excel writer
                    QMessageBox.information(ui, "完成", "数据分析结果已保存至: " + output_path)
                    ui.log_status(f"数据保存至: {output_path}")
                    ui.excel_writer = None
            except Exception as e:
                ui.log_status(f"保存数据时出错: {str(e)}")
        else:
            ui.log_status("保存路径未选择")

    @staticmethod
    def prepare_match_dataframe(match, ui):
        player_stats = match['player_stats']
        hit_data = match['hit_data']
        combo_data = match['combo_data']

        data_for_excel = []
        for player, hits in hit_data.items():
            total_dmg = sum(dmg for weapon, dmg in hits)
            weapon_dmg = defaultdict(int)
            for weapon, dmg in hits:
                weapon_dmg[weapon] += dmg
            most_used_weapon = max(weapon_dmg, key=weapon_dmg.get)
            combo_count = combo_data.get(player, 0)
            kills = player_stats[player]['kills']
            deaths = player_stats[player]['deaths']
            tk_damage = player_stats[player]['tk_damage']
            received_tk_damage = player_stats[player]['received_tk_damage']
            team_hits = player_stats[player]['team_hits']
            tk_kills = player_stats[player]['tk_kills']
            received_combos = player_stats[player]['received_combos']
            k_dmg = player_stats[player]['k_dmg']
            received_k_dmg = player_stats[player]['received_k_dmg']
            combo_hits_ratio = combo_count / len(hits) if len(hits) > 0 else 0
            kill_death_ratio = kills / deaths if deaths > 0 else 0
            k_dmg_damage_ratio = k_dmg / total_dmg if total_dmg > 0 else 0
            k_dmg_combo_ratio = k_dmg / combo_count if combo_count > 0 else 0
            received_k_dmg_combo_ratio = received_k_dmg / received_combos if received_combos > 0 else 0
            rank_score = 0.485 *( 0.8 * ((combo_hits_ratio + 2 * k_dmg_damage_ratio) / 2) * 100
                          + 2 * (k_dmg_combo_ratio - received_k_dmg_combo_ratio)
                          + 2 * combo_count
                          + 0.01 * k_dmg
                          ) + 1.8 * len(hits)+ kill_death_ratio * 1 - tk_kills * 5
            data_for_excel.append([player, rank_score, len(hits), total_dmg, most_used_weapon, combo_count, kills, deaths, tk_damage, received_tk_damage, kill_death_ratio, combo_hits_ratio, received_combos, k_dmg, k_dmg_damage_ratio, k_dmg_combo_ratio, received_k_dmg, received_k_dmg_combo_ratio, team_hits, tk_kills])

        df = pd.DataFrame(data_for_excel, columns=['Player ID', 'Rank Score', 'Hit', 'DMG', 'Most Used Weapon', 'Combos', 'Kills', 'Deaths', 'TK DMG', 'Received TK DMG', 'Kill/Death Ratio', 'Combo/Hits Ratio', 'Received Combos', 'K-DMG', 'K-DMG/DMG', 'K-DMG/Combos', 'Received K-DMG', 'Received K-DMG/Combos', 'Team Hits', 'TK Kills'])

        df = df.sort_values(by=['Rank Score'], ascending=False)

        return df



class ChartPlotter:
    @staticmethod
    def plot_data(match, ui, match_name):
        df = ExcelSaver.prepare_match_dataframe(match, ui)
        
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False

        fig, axes = plt.subplots(5, 2, figsize=(20, 30))
        fig.suptitle(match_name, fontsize=20)

        plots = [
            ('击中次数', 'Hit', 'skyblue'),
            ('击杀次数', 'Kills', 'salmon'),
            ('死亡次数', 'Deaths', 'lightgreen'),
            ('关键补刀次数', 'Combos', 'orange'),
            ('队友伤害', 'TK DMG', 'purple'),
            ('受到队友伤害', 'Received TK DMG', 'brown'),
            ('关键伤害', 'K-DMG', 'red'),
            ('受到关键伤害', 'Received K-DMG', 'blue'),
            ('排名分数', 'Rank Score', 'gold'),
        ]

        for ax, (title, column, color) in zip(axes.flatten()[:-1], plots):
            df.plot(kind='bar', x='Player ID', y=column, ax=ax, color=color)
            ax.set_title(title)
            ax.set_xlabel('玩家ID')
            ax.set_ylabel('次数' if '次数' in title else '伤害量')
            ax.tick_params(axis='x', rotation=0)

        df['Most Used Weapon'].value_counts().plot(kind='pie', ax=axes[4, 1], autopct='%1.1f%%')
        axes[4, 1].set_title('最常使用的武器')
        axes[4, 1].set_ylabel('')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        chart_path = os.path.join(ui.save_path, f"{match_name}.png")
        plt.savefig(chart_path)
        plt.close()

        ui.log_status(f"{match_name} 的图表已保存至: {chart_path}")

        return chart_path
 



import pandas as pd
import re
import os
from collections import defaultdict
from tkinter import Tk, filedialog
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from geopy.distance import geodesic
import requests
from urllib3.util.retry import Retry

class PersonnelScreener:
    @staticmethod
    def get_ip_location(ip):
        """
        调用IP地理位置API获取IP的地理位置（经纬度）。
        """
        if ip.startswith('127.'):  # 忽略本地IP地址
            return None

        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            # 禁用代理的配置
            response = session.get(f"http://ip-api.com/json/{ip}", timeout=10, proxies={"http": None, "https": None})
            response.raise_for_status()  # 检查HTTP请求状态码
            data = response.json()
            if data['status'] == 'success' and data['country'] != 'Hong Kong':
                return (data['lat'], data['lon'], data['city'], data['country'])
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching IP location: {e}")
            return None

    @staticmethod
    def screen_personnel(file_paths, ui):
        """
        读取多个日志文件，分析玩家的加入和离开信息，筛查出嫌疑玩家，并输出Excel文件。
        """
        if not file_paths:
            ui.log_status("未选择文件")
            return

        player_ips = defaultdict(list)
        suspicious_players = []

        join_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - (\S+) has joined the game with ID: (\d+) and IP: (\d+\.\d+\.\d+\.\d+)')
        leave_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - (\S+) has left the game with ID: (\d+) and IP: (\d+\.\d+\.\d+\.\d+)')

        for file_path in file_paths:
            data = DataAnalyzer.read_file(file_path, ui)
            if not data:
                continue

            for line in data:
                join_match = join_pattern.match(line)
                leave_match = leave_pattern.match(line)

                if join_match or leave_match:
                    time, player, player_id, ip = join_match.groups() if join_match else leave_match.groups()
                    player_ips[player].append((time, ip))

        for player, ips in player_ips.items():
            if len(set(ip for _, ip in ips)) > 1:  # 如果同一个玩家有多个不同的IP
                ip_details = []
                ip_locations = {}
                for time, ip in ips:
                    if ip not in ip_locations and not ip.startswith('127.'):
                        location = PersonnelScreener.get_ip_location(ip)
                        if location:
                            ip_locations[ip] = location
                    else:
                        location = ip_locations.get(ip)
                    location_str = f"{location[2]}, {location[3]}" if location else "Unknown location"
                    ip_details.append(f"{time} - {ip} ({location_str})")

                distances = []
                unique_ips = list(set(ip for _, ip in ips if not ip.startswith('127.')))
                for i in range(len(unique_ips)):
                    for j in range(i + 1, len(unique_ips)):
                        loc1 = ip_locations.get(unique_ips[i])
                        loc2 = ip_locations.get(unique_ips[j])
                        if loc1 and loc2:
                            distances.append(geodesic((loc1[0], loc1[1]), (loc2[0], loc2[1])).kilometers)

                max_distance = max(distances) if distances else 0

                if max_distance > 500:  # 你可以根据需要调整距离阈值
                    details_split = '\n'.join([f"{ip_details[i]} {'; ' + ip_details[i + 1] if i + 1 < len(ip_details) else ''}" for i in range(0, len(ip_details), 2)])
                    reason = f"IPs: {', '.join(unique_ips)}; Max Distance: {max_distance:.2f} km; Details: {details_split}"
                    suspicious_players.append((player, reason))

        if suspicious_players:
            output_path = ui.get_save_path("suspicious_players.xlsx")
            if output_path:
                df = pd.DataFrame(suspicious_players, columns=["Player ID", "Reason"])
                writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
                df.to_excel(writer, index=False)
                worksheet = writer.sheets['Sheet1']
                worksheet.set_column('B:B', 80)  # 调整 Reason 列的宽度以完全显示内容
                writer.close()
                ui.log_status(f"嫌疑玩家信息已保存至: {output_path}")
                QMessageBox.information(ui, "完成", f"嫌疑玩家信息已保存至: {output_path}")
        else:
            ui.log_status("未发现嫌疑玩家")










# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MercenaryCompetitionManager()
    main_window.show()
    sys.exit(app.exec_())
