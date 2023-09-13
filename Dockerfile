# За базу используем официальный image питона
FROM python:3.10.6

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED 1

# Обновляем пакетный менеджер
RUN pip install --upgrade pip

# Ставим зависимости GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal
RUN apt-get install --yes libgdal-dev
RUN apt-get install --yes gettext
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

#Скачиваем rar tools

RUN apt install -y unrar-free

# Копируем все файлы приложения в рабочую директорию в контейнере
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m pip install --upgrade --no-cache-dir setuptools==58.0
RUN pip install -r requirements.txt
COPY . .
