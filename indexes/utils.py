from culture_model.models import VegetationIndex
from indexes.models import ActuaVegIndex


def creating_ndvi(date, start, end, indexid):
    index = VegetationIndex.objects.get(id=indexid)
    for i in range(start, end):
        try:
            ActuaVegIndex.objects.create(contour_id=i, index=index, date=date)
            print(f'processed == {i}')
        except Exception as e:
            with open(f'report-{date}.txt', 'a') as file:
                file.write(f"{i}' = f'{e}")
                file.write(',')
                file.write('\n')
            print(f'unprocessed == {i}')
            pass
