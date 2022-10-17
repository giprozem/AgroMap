# За базу используем официальный image питона
FROM python:3.10.6

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED 1

# Обновляем пакетный менеджер
RUN pip install --upgrade pip

# Ставим зависимости GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal
#RUN apt-get install -y gdal-bin libgdal-dev
#RUN apt-get install -y python3-gdal
#RUN apt-get install -y binutils libproj-dev
#RUN apt-get install -y postgis postgresql-13-postgis-3

# Копируем все файлы приложения в рабочую директорию в контейнере
WORKDIR /usr/src/app
ADD . /usr/src/app
RUN pip install -r req.txt
