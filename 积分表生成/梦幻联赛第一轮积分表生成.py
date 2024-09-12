import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

# 读取现有的 Excel 文件
file_path = r"C:\Users\knigh\Desktop\py\Leiteng_\2024骑马与砍杀第二届梦幻联赛.xlsx"
workbook = openpyxl.load_workbook(file_path, data_only=True)

# 获取队伍总览的 sheet
overview_sheet = workbook['队伍总览']

# 队伍信息和对应区域
team_areas = {
    "【CbHz】吃饱喝足就是玩": "B4:D18",
    "【SSR】Superior Super Rare": "G4:I18",
    "【OldH】老H犟嘴": "L4:N18",
    "【AWO】逃出生天": "Q4:S18",
    "【G2】G2": "B35:D49",
    "【TV】Team Vitality": "G35:I49",
    "【Miniworld】迷你世界": "L35:N49",
    "【NikoFC】NikoCN Fanclub": "Q35:S49"
}

# 创建一个新的工作表
new_sheet_name = '第一轮比赛'
workbook.create_sheet(title=new_sheet_name)
sheet = workbook[new_sheet_name]

# 队伍名称
teams = list(team_areas.keys())

# 初始化积分表
sheet.append(['积分表'])
sheet.append(['队伍名称', '积分', '净胜分', '得分', '失分', '胜图数', '随机'])

# 初始化积分表公式
start_row = 3
for i, team in enumerate(teams, start=start_row):
    sheet[f'A{i}'] = team
    sheet[f'B{i}'] = f'=COUNTIF(第一回合对战!$E$4:$E$11, "{team}") * 3 + COUNTIF(第一回合对战!$E$14:$E$21, "{team}") * 3'  # 计算积分
    sheet[f'C{i}'] = f'=SUMIF(第一回合对战!$E$4:$E$11, "{team}", 第一回合对战!$F$4:$F$11) - SUMIF(第一回合对战!$G$4:$G$11, "{team}", 第一回合对战!$G$4:$G$11)'  # 净胜分
    sheet[f'D{i}'] = f'=SUMIF(第一回合对战!$E$4:$E$11, "{team}", 第一回合对战!$F$4:$F$11)'  # 得分
    sheet[f'E{i}'] = f'=SUMIF(第一回合对战!$G$4:$G$11, "{team}", 第一回合对战!$G$4:$G$11)'  # 失分
    sheet[f'F{i}'] = f'=COUNTIF(第一回合对战!$F$4:$F$11, "{team}")'  # 胜图数
    sheet[f'G{i}'] = f'=RAND()'  # 随机数

# 奖励金获得情况
sheet.append([''])
sheet.append(['奖励金获得情况'])
sheet.append(['队伍名称', '小分奖励', '地图胜利奖励', '总奖励'])

# 初始化奖励金公式
start_row_reward = len(teams) + 6
for i, team in enumerate(teams, start=start_row_reward):
    sheet[f'A{i}'] = team
    sheet[f'B{i}'] = f'=D{i-start_row_reward+3} * 10'  # 小分奖励
    sheet[f'C{i}'] = f'=F{i-start_row_reward+3} * 50'  # 地图胜利奖励
    sheet[f'D{i}'] = f'=B{i} + C{i}'  # 总奖励

# 对战表 Round 1
sheet.append([''])
sheet.append(['第一回合对战'])
sheet.append(['比赛轮次', '队伍1', '对阵', '队伍2', '队伍1得分', '队伍2得分', '队伍1胜利图数', '队伍2胜利图数', '队伍1上场人员', '队伍2上场人员', '队伍1总身价', '队伍2总身价', '身价劣势队'])

# 对战安排
round1_pairs = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]
round1_start_row = len(teams) + 11

# 为上场人员设置下拉菜单
for i, pair in enumerate(round1_pairs, start=round1_start_row):
    team1, team2 = pair
    sheet.append([f'比赛{i - round1_start_row + 1}', team1, '对阵', team2, '', '', '', '', '', '', '', '', ''])

    # 数据验证（下拉菜单）设置
    dv_team1 = DataValidation(type="list", formula1=f'队伍总览!{team_areas[team1]}', allow_blank=True)
    dv_team2 = DataValidation(type="list", formula1=f'队伍总览!{team_areas[team2]}', allow_blank=True)

    # 添加数据验证到单元格
    sheet.add_data_validation(dv_team1)
    sheet.add_data_validation(dv_team2)
    dv_team1.add(sheet[f'I{i}'])
    dv_team2.add(sheet[f'J{i}'])

    # 公式：计算总身价和身价劣势队
    sheet[f'K{i}'] = f'=SUMIFS(队伍总览!$D$4:$D$18, 队伍总览!$B$4:$B$18, I{i})'
    sheet[f'L{i}'] = f'=SUMIFS(队伍总览!$D$4:$D$18, 队伍总览!$B$4:$B$18, J{i})'
    sheet[f'M{i}'] = f'=IF(ABS(K{i}-L{i})>200, IF(K{i}<L{i}, A{i}, C{i}), "均势")'

# 对战表 Round 2
sheet.append([''])
sheet.append(['第二回合对战'])
sheet.append(['比赛轮次', '队伍1', '对阵', '队伍2', '队伍1得分', '队伍2得分', '队伍1胜利图数', '队伍2胜利图数', '队伍1上场人员', '队伍2上场人员', '队伍1总身价', '队伍2总身价', '身价劣势队'])

round2_start_row = round1_start_row + len(round1_pairs) + 4
for i in range(len(round1_pairs)):
    sheet.append([f'比赛{i + 1}', '', '对阵', '', '', '', '', '', '', '', '', '', ''])

    # 数据验证（下拉菜单）设置
    dv = DataValidation(type="list", formula1=f'队伍总览!{team_areas[teams[i]]}', allow_blank=True)

    # 添加数据验证到单元格
    sheet.add_data_validation(dv)
    dv.add(sheet[f'I{round2_start_row + i}'])
    dv.add(sheet[f'J{round2_start_row + i}'])

    # 公式：计算总身价和身价劣势队
    sheet[f'K{round2_start_row + i}'] = f'=SUMIFS(队伍总览!$D$4:$D$18, 队伍总览!$B$4:$B$18, I{round2_start_row + i})'
    sheet[f'L{round2_start_row + i}'] = f'=SUMIFS(队伍总览!$D$4:$D$18, 队伍总览!$B$4:$B$18, J{round2_start_row + i})'
    sheet[f'M{round2_start_row + i}'] = f'=IF(ABS(K{round2_start_row + i}-L{round2_start_row + i})>200, IF(K{round2_start_row + i}<L{round2_start_row + i}, A{round2_start_row + i}, C{round2_start_row + i}), "均势")'

# 保存新的 Excel 文件
new_file_path = file_path.replace('.xlsx', '_xin.xlsx')
workbook.save(new_file_path)
