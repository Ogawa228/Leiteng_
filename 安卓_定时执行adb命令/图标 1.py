import plotly.graph_objects as go
import pandas as pd

# 数据准备
data = {
    "月份": ["2023年1月", "2023年2月", "2023年3月", "2023年4月", "2023年5月", "2023年6月", 
            "2023年7月", "2023年8月", "2023年9月", "2023年10月", "2023年11月", "2023年12月"],
    "数量": [10, 15, 20, 18, 25, 23, 30, 28, 35, 32, 30, 28]
}

# 创建数据框
df = pd.DataFrame(data)

# 创建折线图
fig = go.Figure(data=go.Scatter(x=df["月份"], y=df["数量"], mode='lines+markers'))

# 更新布局
fig.update_layout(
    title="2023年每月监测的涉及接码的发卡平台数量",
    xaxis_title="月份",
    yaxis_title="涉及接码的发卡平台数量",
    yaxis=dict(showgrid=True, gridcolor='lightgray'),
    xaxis=dict(showgrid=False)
)

# 展示图表
fig.show()
