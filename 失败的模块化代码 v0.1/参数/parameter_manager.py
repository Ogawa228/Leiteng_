import os
import pickle

def save_parameters_to_file(params, group_name, file_name='用户配置信息.pkl'):
    try:
        # 读取现有的参数（如果文件存在）
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                data = pickle.load(f)
        else:
            data = {}

        # 如果参数组已存在，合并参数；否则，添加新参数组
        if group_name in data:
            # 合并参数，更新已有参数或添加新参数，但不覆盖整个参数组
            for key, value in params.items():
                data[group_name][key] = value
        else:
            # 创建新的参数组
            data[group_name] = params

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
