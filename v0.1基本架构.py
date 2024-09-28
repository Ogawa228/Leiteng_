import tkinter as tk
from tkinter import ttk
import os
import time
import onnxruntime as ort

# 新的 Lua 文件生成路径
LUA_FILE_PATH = os.path.join(os.path.expanduser('~'), "Desktop", "mouse_config.lua")

# 模型文件夹路径
MODEL_FOLDER = os.path.join(os.getcwd(), "models")

# 初始化文件夹
if not os.path.exists(MODEL_FOLDER):
    os.makedirs(MODEL_FOLDER)

# 扫描模型文件夹中的所有 ONNX 文件
def scan_model_files():
    models = [f for f in os.listdir(MODEL_FOLDER) if f.endswith(".onnx")]
    return models

# 创建或更新 mouse_config.lua 文件
def create_lua_file(mouse_x, mouse_y):
    lua_content = f"""
    config = {{
        keys = {{
            ["move"] = {{
                button = 1,  -- 左键
                funcPress = "move_mouse"
            }}
        }}
    }}
    vars = {{
        mouse_x = {mouse_x},
        mouse_y = {mouse_y}
    }}

    function move_mouse(vars)
        MoveMouseTo(vars.mouse_x, vars.mouse_y)
    end
    """
    with open(LUA_FILE_PATH, "w") as lua_file:
        lua_file.write(lua_content)
    print(f"Lua file created at: {LUA_FILE_PATH}")

# 模拟鼠标移动，根据X,Y坐标更新Lua文件
def simulate_mouse_move():
    mouse_x = int(offset_slider.get() * 65535)
    mouse_y = int(confidence_slider.get() * 65535)
    
    create_lua_file(mouse_x, mouse_y)

# 在主界面上创建一个Canvas，展示FOV示意图
def draw_fov(canvas, fov_value):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    rect_x0 = (width / 2) - (fov_value / 2)
    rect_y0 = (height / 2) - (fov_value / 2)
    rect_x1 = (width / 2) + (fov_value / 2)
    rect_y1 = (height / 2) + (fov_value / 2)
    canvas.create_rectangle(rect_x0, rect_y0, rect_x1, rect_y1, outline="red", width=2)

def update_fov():
    fov_value = range_slider.get()
    draw_fov(fov_canvas, fov_value)

# GPU推理
def load_model_with_gpu(onnx_path):
    providers = ort.get_available_providers()
    if "CUDAExecutionProvider" in providers:
        session = ort.InferenceSession(onnx_path, providers=['CUDAExecutionProvider'])
        print("Using GPU for inference.")
    else:
        session = ort.InferenceSession(onnx_path)
        print("Using CPU for inference.")
    return session

# 启动AI的功能
def start_ai():
    print("AI 启动中...")
    simulate_mouse_move()
    time.sleep(1)
    print("AI 已启动。")

# 停止AI的功能
def stop_ai():
    print("AI 已停止。")
    # 鼠标平滑度和速度设置
def create_mouse_settings(window):
    mouse_frame = tk.LabelFrame(window, text="鼠标移动设置", padx=10, pady=10)
    mouse_frame.pack(pady=10, fill="both", expand="yes")

    # 平滑度
    tk.Label(mouse_frame, text="平滑度").pack(anchor="w")
    smoothness_slider = tk.Scale(mouse_frame, from_=1, to=10, orient="horizontal")
    smoothness_slider.pack(fill="x", padx=20)

    # 速度
    tk.Label(mouse_frame, text="速度").pack(anchor="w")
    speed_slider = tk.Scale(mouse_frame, from_=1, to=10, orient="horizontal")
    speed_slider.pack(fill="x", padx=20)

    # 随机度
    tk.Label(mouse_frame, text="随机度").pack(anchor="w")
    randomness_slider = tk.Scale(mouse_frame, from_=0, to=5, orient="horizontal")
    randomness_slider.pack(fill="x", padx=20)

    return smoothness_slider, speed_slider, randomness_slider

# 定义主窗口
def create_advanced_ui():
    window = tk.Tk()
    window.title("高级AI检测工具")
    window.geometry('600x800')

    # 模型文件选择部分
    model_frame = tk.LabelFrame(window, text="模型文件", padx=10, pady=10)
    model_frame.pack(pady=10, fill="both", expand="yes")
    
    model_label = tk.Label(model_frame, text="选择 ONNX 模型文件:")
    model_label.pack(side="left")
    
    model_var = tk.StringVar()
    models_dropdown = ttk.Combobox(model_frame, textvariable=model_var)
    models_dropdown['values'] = scan_model_files()  # 加载模型文件
    models_dropdown.pack(side="left", padx=10)

    # 刷新模型按钮，用户可以手动刷新模型文件列表
    def refresh_models():
        models_dropdown['values'] = scan_model_files()

    refresh_button = tk.Button(model_frame, text="刷新模型", command=refresh_models)
    refresh_button.pack(side="left")

    # GPU编码复选框
    gpu_var = tk.BooleanVar()
    gpu_check = tk.Checkbutton(window, text="GPU 编码", variable=gpu_var)
    gpu_check.pack(pady=10)

    # 偏移量、置信度和范围滑动条
    slider_frame = tk.LabelFrame(window, text="检测参数", padx=10, pady=10)
    slider_frame.pack(pady=10, fill="both", expand="yes")

    tk.Label(slider_frame, text="偏移量").pack(anchor="w")
    global offset_slider
    offset_slider = tk.Scale(slider_frame, from_=0.0, to=1.0, resolution=0.01, orient="horizontal")
    offset_slider.pack(fill="x", padx=20)

    tk.Label(slider_frame, text="置信度").pack(anchor="w")
    global confidence_slider
    confidence_slider = tk.Scale(slider_frame, from_=0.0, to=1.0, resolution=0.01, orient="horizontal")
    confidence_slider.pack(fill="x", padx=20)

    tk.Label(slider_frame, text="范围").pack(anchor="w")
    global range_slider
    range_slider = tk.Scale(slider_frame, from_=0, to=500, orient="horizontal", command=lambda x: update_fov())
    range_slider.pack(fill="x", padx=20)

    # FOV 示意图
    global fov_canvas
    fov_canvas = tk.Canvas(window, width=300, height=300, bg="white")
    fov_canvas.pack(pady=20)

    # 创建FOV示意图的Canvas
    update_fov()

    # 鼠标设置（平滑度、速度、随机度）
    smoothness_slider, speed_slider, randomness_slider = create_mouse_settings(window)

    # 分类启用复选框
    classification_var = tk.BooleanVar()
    classification_check = tk.Checkbutton(window, text="启用分类", variable=classification_var)
    classification_check.pack(pady=10)

    # 下拉菜单选择 Ghub 模式
    mode_frame = tk.LabelFrame(window, text="Ghub 模式", padx=10, pady=10)
    mode_frame.pack(pady=10, fill="both", expand="yes")

    tk.Label(mode_frame, text="选择模式:").pack(side="left")
    mode_var = tk.StringVar()
    mode_dropdown = ttk.Combobox(mode_frame, textvariable=mode_var)
    mode_dropdown['values'] = ('LG-NO', 'LG-YES', 'LG-Maybe')
    mode_dropdown.pack(side="left", padx=10)

    # 启动和停止按钮
    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    start_button = tk.Button(button_frame, text="启动AI", width=20, command=start_ai)
    start_button.pack(side="left", padx=10)

    stop_button = tk.Button(button_frame, text="停止AI", width=20, command=stop_ai)
    stop_button.pack(side="left", padx=10)

    # 显示窗口并启动
    window.mainloop()

# 启动程序
if __name__ == "__main__":
    create_advanced_ui()
