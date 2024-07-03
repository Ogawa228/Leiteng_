import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# 各小组排名
teams = {
    "A组": ["X1队", "水果沙拉队", "疯狂星期四队"],
    "B组": ["DK小伙子和老朋友队", "圣殿哈哈队", "刚铎队"],
    "C组": ["DK&YQS海军四大将队", "乐观王国队", "DK瘦巴巴的老爷队"],
    "D组": ["MINI队", "DK红薯骑士队", "DK神猪无敌小偷队"]
}

# 淘汰赛对位顺序
matches_round1 = [
    ("A1", "D3"), ("B1", "C3"), ("C1", "B3"), ("D1", "A3"),
    ("A2", "D2"), ("B2", "C2")
]

# 根据小组排名获取队伍名称
def get_team_name(group_rank):
    group, rank = group_rank[0], int(group_rank[1])
    return teams[f"{group}组"][rank - 1]

def create_excel_file():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "赛程和积分表"

    # 标题样式
    header_font = Font(bold=True, size=14)
    header_fill = PatternFill("solid", fgColor="DDEBF7")
    center_alignment = Alignment(horizontal="center", vertical="center")

    # 第一轮赛程表标题行
    ws.append(["第一轮（12进8）赛程表"])
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=6)

    # 赛程表表头
    schedule_headers = ["比赛对阵", "队伍1得分", "队伍2得分", "队伍1", "队伍2", "比赛结果"]
    ws.append(schedule_headers)
    for cell in ws[2]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment

    # 填写第一轮赛程表内容
    match_rows = []
    for match in matches_round1:
        team1 = get_team_name(match[0])
        team2 = get_team_name(match[1])
        row = [f"{team1} vs {team2}", "", "", team1, team2, ""]
        ws.append(row)
        match_rows.append(ws.max_row)

    # 调整第一轮赛程表列宽
    for col in range(1, 7):
        ws.column_dimensions[get_column_letter(col)].width = 20

    # 创建积分表标题行
    ws.append([])
    ws.append(["积分表"])
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=5)

    # 积分表表头
    points_headers = ["队伍名称", "小局得分", "小局失分", "净胜分", "胜者组或者败者组"]
    ws.append(points_headers)
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment

    # 填写积分表内容
    qualified_teams = [get_team_name(match[0]) for match in matches_round1] + [get_team_name(match[1]) for match in matches_round1]
    team_rows = {}
    for team in sorted(set(qualified_teams)):  # 使用集合去重并排序
        row = [team, 0, 0, "=B{}-C{}".format(ws.max_row + 1, ws.max_row + 1), ""]
        ws.append(row)
        team_rows[team] = ws.max_row

    # 下拉菜单
    dv = DataValidation(type="list", formula1='"胜者组,败者组"', allow_blank=True)
    ws.add_data_validation(dv)
    for row in range(ws.max_row - len(qualified_teams) + 1, ws.max_row + 1):
        dv.add(f"E{row}")

    # 动态更新积分表公式
    for match_row in match_rows:
        team1 = ws.cell(row=match_row, column=4).value
        team2 = ws.cell(row=match_row, column=5).value
        ws.cell(row=match_row, column=6).value = f'=IF(B{match_row}>C{match_row}, "{team1}", IF(B{match_row}<C{match_row}, "{team2}", "平局"))'
        ws.cell(row=team_rows[team1], column=2).value = f'=SUMIF($D${match_rows[0]}:$D${match_rows[-1]},"{team1}",$B${match_rows[0]}:$B${match_rows[-1]})+SUMIF($E${match_rows[0]}:$E${match_rows[-1]},"{team1}",$C${match_rows[0]}:$C${match_rows[-1]})'
        ws.cell(row=team_rows[team1], column=3).value = f'=SUMIF($D${match_rows[0]}:$D${match_rows[-1]},"{team1}",$C${match_rows[0]}:$C${match_rows[-1]})+SUMIF($E${match_rows[0]}:$E${match_rows[-1]},"{team1}",$B${match_rows[0]}:$B${match_rows[-1]})'
        ws.cell(row=team_rows[team2], column=2).value = f'=SUMIF($D${match_rows[0]}:$D${match_rows[-1]},"{team2}",$B${match_rows[0]}:$B${match_rows[-1]})+SUMIF($E${match_rows[0]}:$E${match_rows[-1]},"{team2}",$C${match_rows[0]}:$C${match_rows[-1]})'
        ws.cell(row=team_rows[team2], column=3).value = f'=SUMIF($D${match_rows[0]}:$D${match_rows[-1]},"{team2}",$C${match_rows[0]}:$C${match_rows[-1]})+SUMIF($E${match_rows[0]}:$E${match_rows[-1]},"{team2}",$B${match_rows[0]}:$B${match_rows[-1]})'

    # 调整积分表列宽
    for col in range(1, 6):
        ws.column_dimensions[get_column_letter(col)].width = 20

    # 八分之一决赛
    ws.append([])
    ws.append(["八分之一决赛（8进4）赛程表"])
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)

    # 八分之一决赛赛程表表头
    ws.append(schedule_headers)
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment

    # 八分之一决赛内容（待确定队伍）
    for i in range(1, 5):
        row = [f"胜者{i} vs 胜者{i+1}", "", "", f"胜者{i}", f"胜者{i+1}", ""]
        ws.append(row)

    # 半决赛
    ws.append([])
    ws.append(["半决赛（4进2）赛程表"])
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)

    # 半决赛赛程表表头
    ws.append(schedule_headers)
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment

    # 半决赛内容（待确定队伍）
    for i in range(1, 3):
        row = [f"半决赛胜者{i} vs 半决赛胜者{i+1}", "", "", f"半决赛胜者{i}", f"半决赛胜者{i+1}", ""]
        ws.append(row)

    # 第三名争夺战
    ws.append([])
    ws.append(["第三名争夺战"])
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)

    # 第三名争夺战赛程表表头
    ws.append(schedule_headers)
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment

    # 第三名争夺战内容（待确定队伍）
    row = ["半决赛失败者1 vs 半决赛失败者2", "", "", "半决赛失败者1", "半决赛失败者2", ""]
    ws.append(row)

    # 决赛
    ws.append([])
    ws.append(["决赛"])
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)

    # 决赛赛程表表头
    ws.append(schedule_headers)
    for cell in ws[ws.max_row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment

    # 决赛内容（待确定队伍）
    row = ["半决赛胜者1 vs 半决赛胜者2", "", "", "半决赛胜者1", "半决赛胜者2", ""]
    ws.append(row)

    # 调整所有列宽
    for col in range(1, 7):
        ws.column_dimensions[get_column_letter(col)].width = 20

    # 保存文件
    wb.save("淘汰赛和积分表.xlsx")

create_excel_file()
