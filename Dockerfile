# За базу используем официальный image питона
FROM python:3.10.6

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED 1

# Обновляем пакетный менеджер
RUN pip install --upgrade pip

# Ставим зависимости GDAL
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        binutils \
        libproj-dev \
        gdal-bin \
        python3-gdal \
        libgdal-dev \
        gettext \
        ffmpeg \
        libsm6 \
        libxext6 \
        unrar-free && \
    rm -rf /var/lib/apt/lists/*

# Копируем все файлы приложения в рабочую директорию в контейнере
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m pip install --upgrade --no-cache-dir setuptools==58.0
RUN pip install -r requirements.txt
COPY . .
