import sys
import zipfile
import re
from openpyxl import Workbook
import os
from tkinter import filedialog, messagebox, Tk
import chardet  # 用于编码检测

# 设置环境变量以抑制Tkinter的弃用警告
os.environ['TK_SILENCE_DEPRECATION'] = '1'

root = Tk()
root.withdraw()  # 不显示Tk根窗口

def detect_encoding(byte_sequence):
    """检测字节序列的编码"""
    result = chardet.detect(byte_sequence)
    encoding = result['encoding']
    return encoding

def ensure_correct_encoding(file_name):
    """尝试以正确的编码解码文件名"""
    try:
        byte_sequence = file_name.encode('cp437')
        detected_encoding = detect_encoding(byte_sequence)
        if detected_encoding in ['GB2312', 'GBK', 'GB18030']:
            return byte_sequence.decode('gbk')
        return byte_sequence.decode(detected_encoding)
    except Exception as e:
        print(f"Error decoding filename: {e}")
        return file_name

def extract_and_process(zip_path, output_path=None):
    messagebox.showinfo("选择解压目标文件夹", "请选择要将临时内容解压到哪个文件夹。")
    extract_path = filedialog.askdirectory(title="请选择解压目标文件夹")
    if not extract_path:
        print("未选择解压目标文件夹，程序退出。")
        sys.exit(1)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            original_file_name = member.filename
            file_name_utf8 = ensure_correct_encoding(original_file_name)
            target_path = os.path.join(extract_path, file_name_utf8)
            target_dir = os.path.dirname(target_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            if not member.is_dir():
                with zip_ref.open(member) as source_file, open(target_path, 'wb') as target_file:
                    target_file.write(source_file.read())

    #初始化Excel工作簿
    wb = Workbook()
    ws = wb.active
    ws.append(["形成时间", "文档名称", "工作时长"])
    total_hours = 0

    # 遍历解压后的文件进行处理
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            match = re.match(r"(\d{4}-\d{1,2}-\d{1,2})-(.*?)-(\d+)h", file)
            if match:
                form_time, doc_name, work_hours = match.groups()
                work_hours = int(work_hours)  # 将字符串转换为整数
                total_hours += work_hours
                ws.append([form_time, doc_name, f"{work_hours}h"])

    ws.append(["总计", "", f"{total_hours}h"])

    if output_path is None:
        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not output_path:  # 如果用户取消选择
            print("未选择输出文件，程序退出。")
            sys.exit(1)

    wb.save(output_path)
    print(f"Excel文件已保存到: {output_path}")

if __name__ == "__main__":
    messagebox.showinfo("选择压缩包", "请选择需要处理的压缩包文件。")
    zip_path = filedialog.askopenfilename(title="请选择压缩包", filetypes=[("Zip files", "*.zip")])
    if not zip_path:
        print("未选择压缩包，程序退出。")
        sys.exit(1)
    
    messagebox.showinfo("保存Excel文件", "请选择输出Excel文件的保存位置。")
    output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", title="保存Excel文件", filetypes=[("Excel files", "*.xlsx")])
    if not output_path:
        print("未选择输出文件，程序退出。")
        sys.exit(1)
    
    extract_and_process(zip_path, output_path)
