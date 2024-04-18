def generate_document_code(doc_prefix, year, person_code, month, day, doc_number):
    """
    根据提供的信息生成文档编号。
    
    参数:
    doc_prefix (str): 文档类型前缀，如'合'
    year (int): 四位数年份，如2023
    person_code (str): 人员特定编号，如'004'
    month (int): 月份，如1
    day (int): 日，如2
    doc_number (int): 文书份数编号，如1
    
    返回:
    str: 生成的文档编号
    """
    # 格式化月份和日
    mmdd = f"{month:02d}{day:02d}"
    
    # 格式化文书份数编号
    doc_num_str = f"{doc_number:03d}"
    
    # 组合所有部分生成完整的文档编号
    document_code = f"（{doc_prefix}字）{{{year}年}}{person_code}{mmdd}{doc_num_str}"
    
    return document_code

# 示例使用
doc_prefix = "合"
year = 2023
person_code = "004"
month = 1
day = 2
doc_number = 1

code = generate_document_code(doc_prefix, year, person_code, month, day, doc_number)
print(code)
