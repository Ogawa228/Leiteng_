# 部署 Streamlit 应用到 Windows Server 并通过公网 IP 访问

本文档将指导您如何在 Windows Server 上部署 Streamlit 应用，并通过公网 IP 访问该应用。随后，将公网 IP 绑定到阿里云域名，并配置二级路径（如 `www.example.com/xxx`）。

---

## 1. 准备工作

### 1.1 环境要求
- **Windows Server**（建议使用 Windows Server 2016 或更高版本）
- **Python 3.7 或更高版本**
- **Streamlit 库**
- **Nginx**（用于反向代理）
- **阿里云域名**
- **公网 IP 地址**（确保服务器已分配公网 IP）

### 1.2 安装 Python 和 Streamlit
1. 下载并安装 Python：[Python 官网](https://www.python.org/downloads/)
2. 安装 Streamlit：
   ```bash
   pip install streamlit
   ```

### 1.3 安装 Nginx
1. 下载 Nginx for Windows：[Nginx 官网](http://nginx.org/en/download.html)
2. 解压到指定目录，例如 `C:\nginx`

---

## 2. 部署 Streamlit 应用

### 2.1 创建 Streamlit 应用
1. 在服务器上创建一个目录，例如 `C:\streamlit_app`
2. 在该目录下创建你的 Streamlit 应用文件，例如 `app.py`

### 2.2 运行 Streamlit 应用
1. 打开命令提示符，导航到 `C:\streamlit_app` 目录
2. 运行 Streamlit 应用：
   ```bash
   streamlit run app.py
   ```
3. 默认情况下，Streamlit 会在 `localhost:8501` 上运行

---

## 3. 配置 Nginx 反向代理

### 3.1 配置 Nginx
1. 打开 Nginx 配置文件 `C:\nginx\conf\nginx.conf`
2. 添加以下配置：
   ```nginx
   server {
       listen 80;
       server_name your_public_ip;  # 替换为你的公网 IP

       location /xxx {
           proxy_pass http://127.0.0.1:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. 保存并关闭配置文件

### 3.2 启动 Nginx
1. 打开命令提示符，导航到 `C:\nginx` 目录
2. 启动 Nginx：
   ```bash
   start nginx
   ```

---

## 4. 通过公网 IP 访问 Streamlit 应用

### 4.1 开放防火墙端口
1. 打开 Windows 防火墙设置
2. 添加入站规则，允许 TCP 端口 `80` 和 `8501` 的流量

### 4.2 访问应用
1. 在浏览器中输入 `http://<你的公网IP>/xxx`，例如 `http://203.0.113.1/xxx`
2. 如果配置正确，你应该能够看到 Streamlit 应用

---

## 5. 绑定阿里云域名

### 5.1 配置域名解析
1. 登录阿里云控制台，进入域名管理页面
2. 找到你的域名，点击“解析设置”
3. 添加一条 A 记录：
   - 记录类型：`A`
   - 主机记录：`www`（或其他子域名）
   - 记录值：你的公网 IP 地址
   - TTL：默认值

### 5.2 修改 Nginx 配置
1. 打开 Nginx 配置文件 `C:\nginx\conf\nginx.conf`
2. 修改 `server_name` 为你的域名：
   ```nginx
   server {
       listen 80;
       server_name www.example.com;  # 替换为你的域名

       location /xxx {
           proxy_pass http://127.0.0.1:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. 保存并重启 Nginx：
   ```bash
   nginx -s reload
   ```

---

## 6. 配置二级路径

### 6.1 二级路径说明
- 通过配置 Nginx 的 `location` 块，可以将 Streamlit 应用绑定到二级路径，例如 `www.example.com/xxx`

### 6.2 验证配置
1. 在浏览器中输入 `http://www.example.com/xxx`
2. 如果配置正确，你应该能够看到 Streamlit 应用

---

## 7. 配置 SSL（可选）

### 7.1 申请 SSL 证书
1. 在阿里云控制台申请 SSL 证书
2. 下载证书文件（包含 `.crt` 和 `.key` 文件）

### 7.2 配置 Nginx 支持 HTTPS
1. 将证书文件上传到服务器，例如 `C:\nginx\conf\ssl`
2. 修改 Nginx 配置文件：
   ```nginx
   server {
       listen 443 ssl;
       server_name www.example.com;

       ssl_certificate C:/nginx/conf/ssl/your_certificate.crt;
       ssl_certificate_key C:/nginx/conf/ssl/your_private.key;

       location /xxx {
           proxy_pass http://127.0.0.1:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

   server {
       listen 80;
       server_name www.example.com;
       return 301 https://$host$request_uri;  # 强制跳转到 HTTPS
   }
   ```
3. 保存并重启 Nginx：
   ```bash
   nginx -s reload
   ```

---

## 8. 访问应用

现在，你可以通过以下方式访问你的 Streamlit 应用：
- 公网 IP：`http://<公网IP>/xxx`
- 域名：`http://www.example.com/xxx`
- HTTPS（如果配置了 SSL）：`https://www.example.com/xxx`

---

## 9. 常见问题

### 9.1 Nginx 无法启动
- 检查端口是否被占用
- 检查配置文件语法是否正确

### 9.2 域名无法访问
- 检查域名解析是否正确
- 检查服务器防火墙是否开放了 80 和 443 端口

### 9.3 Streamlit 应用无法访问
- 检查 Streamlit 是否正常运行
- 检查 Nginx 配置是否正确

---

## 10. 参考文档
- [Streamlit 官方文档](https://docs.streamlit.io/)
- [Nginx 官方文档](http://nginx.org/en/docs/)
- [阿里云域名管理](https://www.aliyun.com/product/domains)

---

通过以上步骤，你应该能够成功在 Windows Server 上部署 Streamlit 应用，并通过公网 IP 和阿里云域名访问该应用，同时支持二级路径配置。