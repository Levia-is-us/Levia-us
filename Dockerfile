FROM python:3.11

WORKDIR /workspace

RUN echo "Initial workspace contents:" && ls -la

# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg \
#     unzip \
#     xvfb \
#     libxi6 \
#     libgconf-2-4 \
#     chromium \
#     chromium-driver

RUN echo "\nWorkspace after installing dependencies:" && ls -la

RUN echo "\nBefore copying requirements.txt:" && ls -la

COPY requirements.txt .
RUN echo "\nAfter copying requirements.txt:" && ls -la

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN echo "\nAfter installing Python dependencies:" && ls -la

RUN echo "\nBefore copying project files:" && ls -la

COPY . .

RUN echo "\nFinal workspace contents:" && ls -la

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV INTERACTION_MODE=server

RUN echo "Files in workspace:" && ls -la

EXPOSE 7072

CMD ["python", "test_app.py"]