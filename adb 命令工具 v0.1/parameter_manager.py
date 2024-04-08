import os
import pickle

def save_parameters_to_file(params, group_name, file_name='用户配置信息.pkl'):
    try:
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                data = pickle.load(f)
        else:
            data = {}

        # 将时间参数也保存到对应的组名下
        data[group_name] = params

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
