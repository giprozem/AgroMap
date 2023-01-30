from culture_model.models import VegetationIndex
from gip.models import Contour
from indexes.models import ActuaVegIndex


def creating_ndvi(date, start, end):
    index = VegetationIndex.objects.get(id=1)
    for i in range(start, end):
        try:
            contour = Contour.objects.get(id=i)
            ActuaVegIndex.objects.create(contour=contour, index=index, date=date)
        except Exception as e:
            with open(f'report-{date}.txt', 'a') as file:
                file.write(f"{i}' = f'{e}")
                file.write(',')
                file.write('\n')
            pass
