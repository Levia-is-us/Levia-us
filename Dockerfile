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
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 获取已安装的Chrome版本
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F. '{print $1}') \
    && echo "Chrome version: $CHROME_VERSION" \
    && wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION" -O chrome_driver_version \
    && CHROMEDRIVER_VERSION=$(cat chrome_driver_version) \
    && echo "ChromeDriver version: $CHROMEDRIVER_VERSION" \
    && wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip chrome_driver_version \
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