import requests
from datetime import datetime, timedelta

def get_workdays(year):
    """
    获取指定年份的工作日总数
    :param year: 年份，例如 2024
    :return: 工作日总数
    """
    # 构造 API URL
    url = f"http://timor.tech/api/holiday/year/{year}?type=Y&week=Y"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # 发送请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        # 检查返回的数据
        if data.get("code") == 0:
            holidays = data.get("holiday", {})
            workdays = 0

            # 遍历每一天，判断是否为工作日
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            current_date = start_date

            while current_date <= end_date:
                date_str = current_date.strftime("%m-%d")
                is_workday = True

                if date_str in holidays:
                    holiday_info = holidays[date_str]
                    if holiday_info.get("holiday"):  # 节假日
                        is_workday = False
                    elif holiday_info.get("type") == 3:  # 调休补班
                        is_workday = True
                elif current_date.weekday() >= 5:  # 周末
                    is_workday = False

                if is_workday:
                    workdays += 1

                current_date += timedelta(days=1)

            print(f"{year} 年的工作日总数：{workdays}")
            return workdays
        else:
            print(f"获取节假日信息失败: {data.get('msg')}")
            return 0
    except requests.exceptions.HTTPError as e:
        print(f"调用节假日API失败: {e}")
        return 0
    except Exception as e:
        print(f"发生未知错误: {e}")
        return 0

if __name__ == "__main__":
    # 测试 2024 年的工作日总数
    year = 2024
    workdays = get_workdays(year)
    print(f"{year} 年的工作日总数：{workdays}")