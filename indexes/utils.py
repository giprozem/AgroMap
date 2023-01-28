from culture_model.models import VegetationIndex
from gip.models import Contour
from indexes.models import ActuaVegIndex
from datetime import datetime


def creating_ndvi(date, start, end):
    index = VegetationIndex.objects.get(id=1)
    for i in range(start, end):
        try:
            contour = Contour.objects.get(id=i)
            ActuaVegIndex.objects.create(contour=contour, index=index, date=date)
        except Exception as e:
            with open(f'report-{datetime.now()}.txt', 'a') as file:
                file.write(f"{contour.id}'] = f'{e}")
                file.write(',')
                file.write('\n')
            print(contour.id)
            pass
