import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import re
import os
from datetime import datetime

class LegalDocProcessor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("法律服务汇总表格生成器")
        # 增加窗口大小
        self.window.geometry("900x650")
        self.window.resizable(True, True)
        
        # 设置苹果风格
        self.configure_style()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self.main_frame, text="法律服务汇总表格生成器", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)
        
        # 添加字体和字号选择框
        self.font_frame = ttk.Frame(self.main_frame)
        self.font_frame.pack(fill=tk.X, pady=5)
        
        # 字体选择
        ttk.Label(self.font_frame, text="表格字体:").pack(side=tk.LEFT, padx=5)
        self.font_var = tk.StringVar(value="仿宋_GB2312")
        self.font_combo = ttk.Combobox(self.font_frame, textvariable=self.font_var, width=15)
        self.font_combo['values'] = ("仿宋_GB2312", "宋体", "黑体", "楷体_GB2312", "微软雅黑", "Times New Roman")
        self.font_combo.pack(side=tk.LEFT, padx=5)
        
        # 字号选择
        ttk.Label(self.font_frame, text="字号:").pack(side=tk.LEFT, padx=5)
        self.font_size_var = tk.StringVar(value="四号(14磅)")
        self.font_size_combo = ttk.Combobox(self.font_frame, textvariable=self.font_size_var, width=10)
        self.font_size_combo['values'] = ("初号(42磅)", "小初(36磅)", "一号(26磅)", "小一(24磅)", 
                                         "二号(22磅)", "小二(18磅)", "三号(16磅)", "小三(15磅)", 
                                         "四号(14磅)", "小四(12磅)", "五号(10.5磅)", "小五(9磅)")
        self.font_size_combo.pack(side=tk.LEFT, padx=5)
        
        # 创建选项卡
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # 第一个选项卡：法律咨询、意见及行政复议、信息公开事务
        self.tab1 = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(self.tab1, text="法律咨询与意见")
        
        # 第二个选项卡：公平竞争审核类
        self.tab2 = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(self.tab2, text="公平竞争审核")
        
        # 第三个选项卡：合同审查
        self.tab3 = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(self.tab3, text="合同审查")
        
        self.tab_control.pack(expand=1, fill="both")
        
        # 设置各选项卡的内容
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        
        # 底部按钮区域
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.X, pady=20)
        
        # 生成文档按钮 - 调整大小和位置
        self.generate_btn = ttk.Button(bottom_frame, text="生成文档", command=self.generate_document, 
                                      style="Accent.TButton", width=15)
        self.generate_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 数据存储
        self.data = {
            "tab1": [],
            "tab2": [],
            "tab3": []
        }
    
    def configure_style(self):
        # 配置苹果风格的样式
        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f7")
        style.configure("TLabel", background="#f5f5f7", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TNotebook", background="#f5f5f7")
        style.configure("TNotebook.Tab", padding=[12, 4], font=("Helvetica", 10))
        
        # 创建强调按钮样式
        style.configure("Accent.TButton", background="#0071e3", foreground="black")
        style.map("Accent.TButton",
                 background=[('active', '#0077ed')],
                 foreground=[('active', 'black')])
        
        # 上传按钮样式
        style.configure("Upload.TButton", padding=5)
        style.map("Upload.TButton",
                 background=[('active', '#e6e6e6')],
                 relief=[('active', 'sunken')])
    
    def setup_tab1(self):
        # 法律咨询、意见及行政复议、信息公开事务
        frame = ttk.Frame(self.tab1)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 说明标签
        ttk.Label(frame, text="法律咨询、意见及行政复议、信息公开事务", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Label(frame, text="表格标题: 序号、事务名称、日期、备注").pack(anchor=tk.W, pady=2)
        
        # 文本区域
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_area1 = tk.Text(text_frame, height=15, width=70, font=("Helvetica", 10))
        self.text_area1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area1.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area1.configure(yscrollcommand=scrollbar.set)
        
        # 按钮区域
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        upload_btn = ttk.Button(btn_frame, text="上传Excel文件", command=lambda: self.upload_excel(1), style="Upload.TButton")
        upload_btn.pack(side=tk.RIGHT)
    
    def setup_tab2(self):
        # 公平竞争审核类
        frame = ttk.Frame(self.tab2)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 说明标签
        ttk.Label(frame, text="公平竞争审核类", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Label(frame, text="表格标题: 序号、送审文件名称、送审时间、审结时间").pack(anchor=tk.W, pady=2)
        
        # 文本区域
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_area2 = tk.Text(text_frame, height=15, width=70, font=("Helvetica", 10))
        self.text_area2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area2.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area2.configure(yscrollcommand=scrollbar.set)
        
        # 按钮区域
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        upload_btn = ttk.Button(btn_frame, text="上传Excel文件", command=lambda: self.upload_excel(2), style="Upload.TButton")
        upload_btn.pack(side=tk.RIGHT)
    
    def setup_tab3(self):
        # 合同审查
        frame = ttk.Frame(self.tab3)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 说明标签
        ttk.Label(frame, text="合同审查", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Label(frame, text="表格标题: 序号、送审合同/协议名称、送审时间、审结时间、备注").pack(anchor=tk.W, pady=2)
        
        # 文本区域
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_area3 = tk.Text(text_frame, height=15, width=70, font=("Helvetica", 10))
        self.text_area3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area3.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area3.configure(yscrollcommand=scrollbar.set)
        
        # 按钮区域
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        upload_btn = ttk.Button(btn_frame, text="上传Excel文件", command=lambda: self.upload_excel(3), style="Upload.TButton")
        upload_btn.pack(side=tk.RIGHT)
    
    def upload_excel(self, tab_index):
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx;*.xls")]
        )
        
        if not file_path:
            return
        
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 根据不同的选项卡处理数据
            if tab_index == 1:
                # 法律咨询、意见及行政复议、信息公开事务
                self.process_tab1_data(df)
            elif tab_index == 2:
                # 公平竞争审核类
                self.process_tab2_data(df)
            elif tab_index == 3:
                # 合同审查
                self.process_tab3_data(df)
                
            messagebox.showinfo("成功", f"Excel文件已成功导入到选项卡{tab_index}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导入Excel文件时出错: {str(e)}")
    
    def process_tab1_data(self, df):
        # 处理第一个选项卡的数据
        # 清空现有数据
        self.data["tab1"] = []
        self.text_area1.delete(1.0, tk.END)
        
        # 假设Excel中的列名为：事务名称、日期、备注
        # 如果列名不同，需要进行映射
        required_columns = ["事务名称", "日期", "备注"]
        
        # 检查必要的列是否存在
        for col in required_columns:
            if col not in df.columns and col.lower() not in [c.lower() for c in df.columns]:
                # 尝试智能匹配列名
                if col == "事务名称":
                    possible_cols = [c for c in df.columns if "名称" in c or "事务" in c or "内容" in c]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "事务名称"}, inplace=True)
                elif col == "日期":
                    possible_cols = [c for c in df.columns if "日期" in c or "时间" in c or "date" in c.lower()]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "日期"}, inplace=True)
                elif col == "备注":
                    possible_cols = [c for c in df.columns if "备注" in c or "说明" in c or "note" in c.lower()]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "备注"}, inplace=True)
        
        # 再次检查必要的列是否存在
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            # 如果缺少列，使用默认值
            for col in missing_cols:
                df[col] = ""
        
        # 处理数据
        for index, row in df.iterrows():
            # 提取事务名称并移除日期
            name = str(row["事务名称"]) if not pd.isna(row["事务名称"]) else ""
            # 使用正则表达式识别并删除日期
            name = self.remove_date_from_text(name)
            
            # 获取日期和备注
            date = str(row["日期"]) if not pd.isna(row["日期"]) else ""
            remark = str(row["备注"]) if not pd.isna(row["备注"]) else ""
            
            # 添加到数据列表
            self.data["tab1"].append({
                "事务名称": name,
                "日期": date,
                "备注": remark
            })
            
            # 更新文本区域
            self.text_area1.insert(tk.END, f"事务名称: {name}\n日期: {date}\n备注: {remark}\n\n")
    
    def process_tab2_data(self, df):
        # 处理第二个选项卡的数据
        # 清空现有数据
        self.data["tab2"] = []
        self.text_area2.delete(1.0, tk.END)
        
        # 假设Excel中的列名为：送审文件名称、送审时间、审结时间
        required_columns = ["送审文件名称", "送审时间", "审结时间"]
        
        # 检查必要的列是否存在
        for col in required_columns:
            if col not in df.columns and col.lower() not in [c.lower() for c in df.columns]:
                # 尝试智能匹配列名
                if col == "送审文件名称":
                    possible_cols = [c for c in df.columns if "名称" in c or "文件" in c or "送审" in c]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "送审文件名称"}, inplace=True)
                elif col == "送审时间":
                    possible_cols = [c for c in df.columns if "送审" in c and ("时间" in c or "日期" in c)]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "送审时间"}, inplace=True)
                elif col == "审结时间":
                    possible_cols = [c for c in df.columns if "审结" in c and ("时间" in c or "日期" in c)]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "审结时间"}, inplace=True)
        
        # 再次检查必要的列是否存在
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            # 如果缺少列，使用默认值
            for col in missing_cols:
                df[col] = ""
        
        # 处理数据
        for index, row in df.iterrows():
            # 提取送审文件名称并移除日期
            name = str(row["送审文件名称"]) if not pd.isna(row["送审文件名称"]) else ""
            # 使用正则表达式识别并删除日期
            name = self.remove_date_from_text(name)
            
            # 获取送审时间和审结时间
            submit_date = str(row["送审时间"]) if not pd.isna(row["送审时间"]) else ""
            complete_date = str(row["审结时间"]) if not pd.isna(row["审结时间"]) else ""
            
            # 添加到数据列表
            self.data["tab2"].append({
                "送审文件名称": name,
                "送审时间": submit_date,
                "审结时间": complete_date
            })
            
            # 更新文本区域
            self.text_area2.insert(tk.END, f"送审文件名称: {name}\n送审时间: {submit_date}\n审结时间: {complete_date}\n\n")
    
    def process_tab3_data(self, df):
        # 处理第三个选项卡的数据
        # 清空现有数据
        self.data["tab3"] = []
        self.text_area3.delete(1.0, tk.END)
        
        # 假设Excel中的列名为：送审合同/协议名称、送审时间、审结时间、备注
        required_columns = ["送审合同/协议名称", "送审时间", "审结时间", "备注"]
        
        # 检查必要的列是否存在
        for col in required_columns:
            if col not in df.columns and col.lower() not in [c.lower() for c in df.columns]:
                # 尝试智能匹配列名
                if col == "送审合同/协议名称":
                    possible_cols = [c for c in df.columns if "名称" in c or "合同" in c or "协议" in c or "送审" in c]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "送审合同/协议名称"}, inplace=True)
                elif col == "送审时间":
                    possible_cols = [c for c in df.columns if "送审" in c and ("时间" in c or "日期" in c)]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "送审时间"}, inplace=True)
                elif col == "审结时间":
                    possible_cols = [c for c in df.columns if "审结" in c and ("时间" in c or "日期" in c)]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "审结时间"}, inplace=True)
                elif col == "备注":
                    possible_cols = [c for c in df.columns if "备注" in c or "说明" in c or "note" in c.lower()]
                    if possible_cols:
                        df.rename(columns={possible_cols[0]: "备注"}, inplace=True)
        
        # 再次检查必要的列是否存在
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            # 如果缺少列，使用默认值
            for col in missing_cols:
                df[col] = ""
        
        # 处理数据
        for index, row in df.iterrows():
            # 提取送审合同/协议名称并移除日期
            name = str(row["送审合同/协议名称"]) if not pd.isna(row["送审合同/协议名称"]) else ""
            # 使用正则表达式识别并删除日期
            name = self.remove_date_from_text(name)
            
            # 获取送审时间、审结时间和备注
            submit_date = str(row["送审时间"]) if not pd.isna(row["送审时间"]) else ""
            complete_date = str(row["审结时间"]) if not pd.isna(row["审结时间"]) else ""
            remark = str(row["备注"]) if not pd.isna(row["备注"]) else ""
            
            # 添加到数据列表
            self.data["tab3"].append({
                "送审合同/协议名称": name,
                "送审时间": submit_date,
                "审结时间": complete_date,
                "备注": remark
            })
            
            # 更新文本区域
            self.text_area3.insert(tk.END, f"送审合同/协议名称: {name}\n送审时间: {submit_date}\n审结时间: {complete_date}\n备注: {remark}\n\n")
    
    def remove_date_from_text(self, text):
        # 使用正则表达式识别并删除日期
        # 匹配常见的日期格式，如：2023年1月1日、2023-01-01、2023/01/01、2023.01.01等
        date_patterns = [
            r'\d{4}[-/年\.](\d{1,2}[-/月\.](\d{1,2}[日]?)?)?(\s*-\s*\d{4}[-/年\.](\d{1,2}[-/月\.](\d{1,2}[日]?)?)?)?',  # 2023年1月1日 或 2023-01-01
            r'\d{2}[-/年\.](\d{1,2}[-/月\.](\d{1,2}[日]?)?)?(\s*-\s*\d{2}[-/年\.](\d{1,2}[-/月\.](\d{1,2}[日]?)?)?)?',  # 23年1月1日 或 23-01-01
            r'(\d{1,2}月\d{1,2}日)(\s*-\s*(\d{1,2}月\d{1,2}日)?)?',  # 1月1日
            r'\(\d{4}\.\d{1,2}\.\d{1,2}\)',  # (2023.01.01)
            r'【\d{4}\.\d{1,2}\.\d{1,2}】'   # 【2023.01.01】
        ]
        
        # 应用所有日期模式
        for pattern in date_patterns:
            text = re.sub(pattern, '', text)
        
        # 删除时间戳后面的连字符及其前后空格
        text = re.sub(r'\s*-\s*', '', text)  # 删除连字符及其前后的空格
        
        # 删除文件扩展名 - 扩展词库
        extensions = [
            # 文档格式
            r'docx?', r'xlsx?', r'pptx?', r'pdf', r'txt', r'rtf', r'odt', r'ods', r'odp', r'csv', r'md', r'tex',
            # 图像格式
            r'jpg', r'jpeg', r'png', r'gif', r'bmp', r'tiff?', r'svg', r'webp', r'psd', r'ai', r'eps',
            # 音视频格式
            r'mp3', r'wav', r'ogg', r'flac', r'mp4', r'avi', r'mov', r'wmv', r'mkv', r'flv', r'webm',
            # 压缩格式
            r'zip', r'rar', r'7z', r'tar', r'gz', r'bz2', r'xz',
            # 编程和脚本格式
            r'py', r'js', r'html?', r'css', r'php', r'java', r'c', r'cpp', r'cs', r'go', r'rb', r'pl', r'sh', r'bat',
            # 其他常见格式
            r'exe', r'dll', r'iso', r'img', r'dmg', r'apk', r'ipa'
        ]
        extension_pattern = r'\.(' + '|'.join(extensions) + r')$'
        text = re.sub(extension_pattern, '', text, flags=re.IGNORECASE)
        
        # 删除多余的空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def generate_document(self):
        try:
            # 打开模板文件
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "模板.docx")
            doc = Document(template_path)
            
            # 获取所有表格
            tables = doc.tables
            
            # 确保有足够的表格
            if len(tables) < 3:
                messagebox.showerror("错误", "模板文件中的表格数量不足")
                return
            
            # 处理第一个表格：法律咨询、意见及行政复议、信息公开事务
            self.fill_table1(tables[0])
            
            # 处理第二个表格：公平竞争审核类
            self.fill_table2(tables[1])
            
            # 处理第三个表格：合同审查
            self.fill_table3(tables[2])
            
            # 保存新文件
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            save_path = filedialog.asksaveasfilename(
                title="保存文件",
                initialfile=f"法律服务汇总表格_{now}.docx",
                filetypes=[("Word文档", "*.docx")]
            )
            
            if save_path:
                if not save_path.endswith(".docx"):
                    save_path += ".docx"
                doc.save(save_path)
                messagebox.showinfo("成功", f"文档已成功生成并保存至: {save_path}")
                
                # 询问是否打开文件
                if messagebox.askyesno("打开文件", "是否立即打开生成的文件?"):
                    os.startfile(save_path)
        except Exception as e:
            messagebox.showerror("错误", f"生成文档时出错: {str(e)}")
    
    def fill_table1(self, table):
        # 填充第一个表格：法律咨询、意见及行政复议、信息公开事务
        data = self.data["tab1"]
        if not data:
            return
        
        # 获取表格的行数和列数
        rows = len(table.rows)
        cols = len(table.columns)
        
        # 第一行是标题行，从第二行开始填充数据
        start_row = 1
        
        # 如果数据行数超过表格行数，需要添加行
        while len(data) + start_row > rows:
            table.add_row()
            rows += 1
        
        # 填充数据
        for i, item in enumerate(data):
            row_idx = i + start_row
            
            # 序号
            cell = table.cell(row_idx, 0)
            cell.text = str(i + 1)
            self.set_cell_font(cell)
            
            # 事务名称
            cell = table.cell(row_idx, 1)
            cell.text = item["事务名称"]
            self.set_cell_font(cell)
            
            # 日期
            cell = table.cell(row_idx, 2)
            cell.text = item["日期"]
            self.set_cell_font(cell)
            
            # 备注
            if cols > 3:  # 确保表格有备注列
                cell = table.cell(row_idx, 3)
                cell.text = item["备注"]
                self.set_cell_font(cell)
    
    def fill_table2(self, table):
        # 填充第二个表格：公平竞争审核类
        data = self.data["tab2"]
        if not data:
            return
        
        # 获取表格的行数和列数
        rows = len(table.rows)
        cols = len(table.columns)
        
        # 第一行是标题行，从第二行开始填充数据
        start_row = 1
        
        # 如果数据行数超过表格行数，需要添加行
        while len(data) + start_row > rows:
            table.add_row()
            rows += 1
        
        # 填充数据
        for i, item in enumerate(data):
            row_idx = i + start_row
            
            # 序号
            cell = table.cell(row_idx, 0)
            cell.text = str(i + 1)
            self.set_cell_font(cell)
            
            # 送审文件名称
            cell = table.cell(row_idx, 1)
            cell.text = item["送审文件名称"]
            self.set_cell_font(cell)
            
            # 送审时间
            cell = table.cell(row_idx, 2)
            cell.text = item["送审时间"]
            self.set_cell_font(cell)
            
            # 审结时间
            if cols > 3:  # 确保表格有审结时间列
                cell = table.cell(row_idx, 3)
                cell.text = item["审结时间"]
                self.set_cell_font(cell)
    
    def fill_table3(self, table):
        # 填充第三个表格：合同审查
        data = self.data["tab3"]
        if not data:
            return
        
        # 获取表格的行数和列数
        rows = len(table.rows)
        cols = len(table.columns)
        
        # 第一行是标题行，从第二行开始填充数据
        start_row = 1
        
        # 如果数据行数超过表格行数，需要添加行
        while len(data) + start_row > rows:
            table.add_row()
            rows += 1
        
        # 填充数据
        for i, item in enumerate(data):
            row_idx = i + start_row
            
            # 序号
            cell = table.cell(row_idx, 0)
            cell.text = str(i + 1)
            self.set_cell_font(cell)
            
            # 送审合同/协议名称
            cell = table.cell(row_idx, 1)
            cell.text = item["送审合同/协议名称"]
            self.set_cell_font(cell)
            
            # 送审时间
            cell = table.cell(row_idx, 2)
            cell.text = item["送审时间"]
            self.set_cell_font(cell)
            
            # 审结时间
            if cols > 3:  # 确保表格有审结时间列
                cell = table.cell(row_idx, 3)
                cell.text = item["审结时间"]
                self.set_cell_font(cell)
            
            # 备注
            if cols > 4:  # 确保表格有备注列
                cell = table.cell(row_idx, 4)
                cell.text = item["备注"]
                self.set_cell_font(cell)
    
    def set_cell_font(self, cell):
        """设置单元格字体和字号"""
        # 获取用户选择的字体
        font_name = self.font_var.get()
        
        # 获取用户选择的字号并提取磅值
        font_size_str = self.font_size_var.get()
        # 从字符串中提取磅值，例如从"四号(14磅)"提取14
        font_size_match = re.search(r'(\d+\.?\d*)磅', font_size_str)
        font_size = 14  # 默认值
        if font_size_match:
            font_size = float(font_size_match.group(1))
        
        # 设置段落属性
        for paragraph in cell.paragraphs:
            # 先保存文本内容
            text = paragraph.text
            # 清空段落内容
            paragraph.clear()
            # 设置段落对齐方式
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # 居中对齐
            
            # 创建新的文本运行并设置字体
            if text:
                run = paragraph.add_run(text)
                # 设置西文字体
                run.font.name = font_name
                # 设置字号
                run.font.size = Pt(font_size)
                # 设置中文字体
                run.font.east_asia_name = font_name
                
                # 特殊处理仿宋_GB2312字体
                if font_name == "仿宋_GB2312":
                    run.font.cs_name = "仿宋"
                    
                # 确保应用字体设置
                run._element.rPr.xml

    def run(self):
        """运行应用程序"""
        self.window.mainloop()

if __name__ == "__main__":
    app = LegalDocProcessor()
    app.run()