FROM python:3.11

WORKDIR /workspace

# 安装基本依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libasound2

# 安装Google Chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb \
    && apt-get install -y ./google-chrome-stable_114.0.5735.198-1_amd64.deb \
    && rm google-chrome-stable_114.0.5735.198-1_amd64.deb

# 安装固定版本的ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

# 显示版本信息以验证
RUN google-chrome --version && chromedriver --version

# 复制项目文件
COPY . .
RUN python install_requirements.py

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV INTERACTION_MODE=server
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

EXPOSE 7072

# 启动Xvfb和应用
CMD Xvfb :99 -screen 0 1280x1024x24 -ac +extension GLX +render -noreset & python main.py