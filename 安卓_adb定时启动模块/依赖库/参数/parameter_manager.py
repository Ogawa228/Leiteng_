import os
import pickle
from datetime import datetime

def save_parameters_to_file(params, group_name, file_name='用户配置信息.pkl'):
    try:
        # 读取现有的参数（如果文件存在）
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                data = pickle.load(f)
        else:
            data = {}

        # 获取当前时间，并格式化为"-yyyy/MM/dd HH:mm"
        timestamp = datetime.now().strftime("-%Y/%m/%d %H:%M")
        
        # 检查是否存在该组名（忽略时间戳）
        updated = False
        for existing_group_name in list(data.keys()):
            if group_name in existing_group_name.split('-')[0]:
                # 更新时间戳
                new_group_name = f"{group_name}{timestamp}"
                data[new_group_name] = params
                # 删除旧的记录
                del data[existing_group_name]
                updated = True
                break
        
        if not updated:
            # 如果没有更新，则添加新的记录
            group_name_with_timestamp = f"{group_name}{timestamp}"
            data[group_name_with_timestamp] = params

        # 写入更新后的参数到文件
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"保存参数失败: {e}")
        return False


def load_parameters_from_file(group_name, file_name='用户配置信息.pkl'):
    try:
        if not os.path.exists(file_name):
            return None

        with open(file_name, 'rb') as f:
            data = pickle.load(f)

        # 返回指定组名的参数，包括时间参数
        return data.get(group_name)
    except Exception as e:
        print(f"加载参数失败: {e}")
        return None
    
def load_latest_parameters(file_name='用户配置信息.pkl'):
    try:
        if not os.path.exists(file_name):
            return None

        with open(file_name, 'rb') as f:
            data = pickle.load(f)
        
        if not data:
            return None

        # 将参数组的键（组名+时间戳）分割并解析时间戳，找到最新的参数组
        latest_group = None
        latest_time = None
        for group_name in data.keys():
            try:
                # 假设时间戳格式为“-yyyy/mm/dd hh:mm”，并且总是位于参数组名的末尾
                time_str = group_name.split('-')[-1]  # 获取最后一个'-'后的时间戳部分
                group_time = datetime.strptime(time_str, "%Y/%m/%d %H:%M")
                
                if latest_time is None or group_time > latest_time:
                    latest_time = group_time
                    latest_group = group_name
            except ValueError:
                # 如果时间戳解析失败，跳过当前参数组
                continue
        
        if latest_group:
            return data[latest_group]
        else:
            return None
    except Exception as e:
        print(f"加载最新参数失败: {e}")
        return None
    
