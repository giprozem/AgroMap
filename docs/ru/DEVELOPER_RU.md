# Для разработчиков

В этом проекте используются следующие ключевые скрипты и компоненты:

## Директория scripts содержит следующие файлы:

1. `cron_download_S2_Copernicus.py` -
   Скрипт, настроенный на автоматическое скачивание спутниковых изображений от Copernicus каждый месяц для заданных
   областей интереса, подключенный к crontab.
2. `heat_map_ndvi.py`
   Скрипт для создания тепловых карт по всей территории Кыргызстана, используя данные индекса NDVI.
3. `productivity_contour.py`
   Скрипт для модели машинного обучения, которая расчитывает производительность пастбищ на основе загруженных
   спутниковых изображений и других данных.
4. `productivity_heat_map.py`
   Скрипт для создания тепловых карт производительности пастбищ.

## Директория AI/Utils содержит следующие файлы:

1. `predicted_contour.py` -
   Этот скрипт содержит нейронную сеть, основанную на YOLOv8, для определения контуров на основе спутниковых
   изображений.

## Директория Indexes содержит следующие файлы:

1. `download_satellite_images.py` -
   Скрипт, находящийся в директории `indexes/views`, служит для загрузки спутниковых изображений по заданной дате и
   области интереса через API `v2/download_satellite_images/`