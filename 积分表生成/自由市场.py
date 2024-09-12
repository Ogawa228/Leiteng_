import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

# 加载现有的工作簿
file_path = r"C:\Users\knigh\Desktop\py\Leiteng_\2024骑马与砍杀第二届梦幻联赛-功能测试.xlsx"
wb = openpyxl.load_workbook(file_path)

# 获取拍卖列表表来获取格式和数据源
auction_sheet = wb["拍卖列表"]

# 创建新的工作表并设置特定的标题和格式
def create_sheet_with_headers(wb, sheet_name, headers):
    # 删除现有的同名工作表（如果有）
    if sheet_name in wb.sheetnames:
        wb.remove(wb[sheet_name])
    # 创建新的工作表
    ws = wb.create_sheet(sheet_name)
    ws.append(headers)
    return ws

# 定义标题
headers = ["球员昵称", "交易价格", "买入队伍", "卖出队伍", "交易窗口"]

# 创建交易历史工作表
transaction_history_sheet = create_sheet_with_headers(wb, "交易历史", headers)

# 将数据从拍卖列表表复制到首次交易表，并保留格式
def copy_data_to_first_trading_sheet(ws_auction, ws_history):
    for row in range(12, 145):
        player_name = ws_auction.cell(row=row, column=1).value
        highest_price = ws_auction.cell(row=row, column=3).value
        current_team = ws_auction.cell(row=row, column=4).value
        
        # 复制数据
        ws_history.cell(row=row-10, column=1, value=player_name)  # 复制到交易历史表的A2:A144
        ws_history.cell(row=row-10, column=2, value=highest_price)  # 复制到交易历史表的B2:B144
        ws_history.cell(row=row-10, column=3, value=current_team)  # 复制到交易历史表的C2:C144
        
        # 复制格式
        auction_cell = ws_auction.cell(row=row, column=1)
        history_cell = ws_history.cell(row=row-10, column=1)
        history_cell.font = openpyxl.styles.Font(
            name=auction_cell.font.name,
            size=auction_cell.font.size,
            bold=auction_cell.font.bold,
            italic=auction_cell.font.italic,
            vertAlign=auction_cell.font.vertAlign,
            underline=auction_cell.font.underline,
            strike=auction_cell.font.strike,
            color=auction_cell.font.color
        )
        history_cell.fill = openpyxl.styles.PatternFill(
            fill_type=auction_cell.fill.fill_type,
            start_color=auction_cell.fill.start_color,
            end_color=auction_cell.fill.end_color
        )
        history_cell.border = openpyxl.styles.Border(
            left=auction_cell.border.left,
            right=auction_cell.border.right,
            top=auction_cell.border.top,
            bottom=auction_cell.border.bottom
        )
        history_cell.alignment = openpyxl.styles.Alignment(
            horizontal=auction_cell.alignment.horizontal,
            vertical=auction_cell.alignment.vertical,
            text_rotation=auction_cell.alignment.text_rotation,
            wrap_text=auction_cell.alignment.wrap_text,
            shrink_to_fit=auction_cell.alignment.shrink_to_fit,
            indent=auction_cell.alignment.indent
        )

        # Repeat for other cells
        for col in range(3, 5):  # C and D columns in auction_sheet
            auction_cell = ws_auction.cell(row=row, column=col)
            history_cell = ws_history.cell(row=row-10, column=col-1)
            history_cell.font = openpyxl.styles.Font(
                name=auction_cell.font.name,
                size=auction_cell.font.size,
                bold=auction_cell.font.bold,
                italic=auction_cell.font.italic,
                vertAlign=auction_cell.font.vertAlign,
                underline=auction_cell.font.underline,
                strike=auction_cell.font.strike,
                color=auction_cell.font.color
            )
            history_cell.fill = openpyxl.styles.PatternFill(
                fill_type=auction_cell.fill.fill_type,
                start_color=auction_cell.fill.start_color,
                end_color=auction_cell.fill.end_color
            )
            history_cell.border = openpyxl.styles.Border(
                left=auction_cell.border.left,
                right=auction_cell.border.right,
                top=auction_cell.border.top,
                bottom=auction_cell.border.bottom
            )
            history_cell.alignment = openpyxl.styles.Alignment(
                horizontal=auction_cell.alignment.horizontal,
                vertical=auction_cell.alignment.vertical,
                text_rotation=auction_cell.alignment.text_rotation,
                wrap_text=auction_cell.alignment.wrap_text,
                shrink_to_fit=auction_cell.alignment.shrink_to_fit,
                indent=auction_cell.alignment.indent
            )

        ws_history.cell(row=row-10, column=5, value="首次交易")  # 添加交易窗口

# 复制初始数据到“交易历史”工作表
copy_data_to_first_trading_sheet(auction_sheet, transaction_history_sheet)

# 从拍卖列表表A3:A10应用买入和卖出队伍的下拉菜单
team_list = ",".join([auction_sheet[f"A{row}"].value for row in range(3, 11) if auction_sheet[f"A{row}"].value is not None])
team_validation = DataValidation(type="list", formula1=f'"{team_list}"', allow_blank=True)

# 从拍卖列表表A12:A144应用球员昵称的下拉菜单
player_list = ",".join([auction_sheet[f"A{row}"].value for row in range(12, 145) if auction_sheet[f"A{row}"].value is not None])
player_validation = DataValidation(type="list", formula1=f'"{player_list}"', allow_blank=True)

# 添加交易窗口下拉列表
trading_windows = ["首次交易", "二次交易", "三次交易", "四次交易"]
window_validation = DataValidation(type="list", formula1=f'"{",".join(trading_windows)}"', allow_blank=True)

# 应用数据验证到交易历史工作表
transaction_history_sheet.add_data_validation(player_validation)
player_validation.add(f"A2:A200")

transaction_history_sheet.add_data_validation(team_validation)
for col in ['C', 'D']:
    team_validation.add(f"{col}2:{col}200")

transaction_history_sheet.add_data_validation(window_validation)
window_validation.add(f"E2:E200")

# 更新拍卖列表中的最高身价和当前队伍
def update_highest_price_and_current_team(ws_auction, ws_history):
    for row in range(12, 145):
        player_name = ws_auction.cell(row=row, column=1).value
        highest_price_formula = f"=MAXIFS(交易历史!B:B, 交易历史!A:A, A{row})"
        ws_auction.cell(row=row, column=3).value = highest_price_formula
        
        current_team_formula = f"=INDEX(交易历史!C:C, MATCH(A{row}, 交易历史!A:A, 0))"
        ws_auction.cell(row=row, column=4).value = current_team_formula

update_highest_price_and_current_team(auction_sheet, transaction_history_sheet)

# 更新拍卖列表中的剩余资金公式
def update_remaining_funds(ws_auction, ws_history):
    for row in range(3, 11):
        team_name = ws_auction.cell(row=row, column=1).value
        formula = (
            f"=B{row} "
            f"- SUMIFS(交易历史!B:B, 交易历史!C:C, A{row}, 交易历史!E:E, \"首次交易\") "
            f"+ SUMIFS(交易历史!B:B, 交易历史!D:D, A{row}, 交易历史!E:E, \"首次交易\") "
            f"- SUMIFS(交易历史!B:B, 交易历史!C:C, A{row}, 交易历史!E:E, \"二次交易\") "
            f"+ SUMIFS(交易历史!B:B, 交易历史!D:D, A{row}, 交易历史!E:E, \"二次交易\") "
            f"- SUMIFS(交易历史!B:B, 交易历史!C:C, A{row}, 交易历史!E:E, \"三次交易\") "
            f"+ SUMIFS(交易历史!B:B, 交易历史!D:D, A{row}, 交易历史!E:E, \"三次交易\") "
            f"- SUMIFS(交易历史!B:B, 交易历史!C:C, A{row}, 交易历史!E:E, \"四次交易\") "
            f"+ SUMIFS(交易历史!B:B, 交易历史!D:D, A{row}, 交易历史!E:E, \"四次交易\")"
        )
        ws_auction.cell(row=row, column=3).value = formula

update_remaining_funds(auction_sheet, transaction_history_sheet)

# 保存工作簿
save_path = r"C:\Users\knigh\Desktop\py\Leiteng_\2024骑马与砍杀第二届梦幻联赛-功能测试_更新.xlsx"
wb.save
