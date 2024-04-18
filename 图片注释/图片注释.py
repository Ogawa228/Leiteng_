from PIL import Image, ImageDraw, ImageFont

# 用户上传图像的路径（请替换为您的图像文件路径）
img_path = '/Users/jinjiangshan/Downloads/image-83-1024x597.png'
image = Image.open(img_path)

# 创建绘图对象
draw = ImageDraw.Draw(image)

# 定义注释字体和大小
# 请替换为您的微软雅黑字体的实际路径
font_path = "/Users/jinjiangshan/Downloads/msyh.ttf"
font = ImageFont.truetype(font_path, 12)

# 定义注释及其位置
annotations = {
    (440, 40): "一级网络服务提供商 (Tier 1 Networks)",
    (220, 150): "二级网络服务提供商 (Tier 2 Networks)",
    (270, 550): "三级网络服务提供商（多线ISP）(Tier 3 Network - multi-homed ISP)",
    (730, 630): "三级网络服务提供商（单线ISP）(Tier 3 Network - single homed ISP)",
    (800, 100): "二级网络服务提供商ISP (Tier 2 ISP)",
    (190, 250): "接入点1 (PoP #1)",
    (150, 330): "接入点2 (PoP #2)",
    (120, 410): "接入点3 (PoP #3)",
    (490, 90): "对等互联 (Peering)",
    (490, 160): "互联网交换点 (IXP)",
    (270, 750): "互联网用户（企业、消费者等）(Internet - business, consumers, etc)"
}

# 添加注释到图像
for position, text in annotations.items():
    draw.text(position, text, fill="black", font=font, anchor="mm")

# 保存带注释的图像
annotated_img_path = '/Users/jinjiangshan/Downloads/annotated_image.png'
image.save(annotated_img_path)