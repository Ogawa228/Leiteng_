# parameter_manager.py

import os
import pickle

def save_parameters_to_file(params, group_name, file_name='用户配置信息.pkl'):
    try:
        # 读取现有参数，如果文件不存在，则创建一个空字典
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                data = pickle.load(f)
        else:
            data = {}

        # 保存参数到对应的组名下
        data[group_name] = params

        # 写回文件
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"保存参数错误: {e}")
        return False

def load_parameters_from_file(group_name, file_name='用户配置信息.pkl'):
    try:
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
            if group_name in data:
                return data[group_name]
            else:
                return None
    except (FileNotFoundError, EOFError, Exception) as e:
        print(f"加载参数错误: {e}")
        return None