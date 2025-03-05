FROM python:3.11

WORKDIR /workspace

RUN apt-get update && apt-get remove -y chromium chromium-driver

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

RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable=114.0.5735.* \
    && apt-mark hold google-chrome-stable

RUN google-chrome --version && chromedriver --version

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn waitress

COPY . .
RUN python install_requirements.py

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV INTERACTION_MODE=server
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

EXPOSE 7072

CMD Xvfb :99 -screen 0 1280x1024x24 -ac +extension GLX +render -noreset & python main.py