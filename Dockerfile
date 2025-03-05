FROM python:3.11

WORKDIR /workspace

RUN echo "Initial workspace contents:" && ls -la

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    chromium \
    chromium-driver \
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

RUN echo "\nWorkspace after installing dependencies:" && ls -la

RUN echo "\nBefore copying requirements.txt:" && ls -la

COPY requirements.txt .
RUN echo "\nAfter copying requirements.txt:" && ls -la

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install waitress

RUN echo "\nAfter installing Python dependencies:" && ls -la

RUN echo "\nBefore copying project files:" && ls -la

COPY . .
RUN python install_requirements.py

RUN echo "\nFinal workspace contents:" && ls -la

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV INTERACTION_MODE=server
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/

RUN echo "Files in workspace:" && ls -la

EXPOSE 7072

CMD ["python", "main.py"]