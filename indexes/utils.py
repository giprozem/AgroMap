from culture_model.models import VegetationIndex
from gip.models import ContourYear
from indexes.models import ActualVegIndex
import matplotlib.pyplot as plt


def creating_ndvi(date, start, end, indexid):
    index = VegetationIndex.objects.get(id=indexid)
    for i in range(start, end):
        try:
            ActualVegIndex.objects.create(contour_id=i, index=index, date=date)
            print(f'processed == {i}')
        except Exception as e:
            with open(f'report-{date}.txt', 'a') as file:
                file.write(f"{i}' = f'{e}")
                file.write(',')
                file.write('\n')
            print(f'unprocessed == {i}')
            plt.close()
            pass


def creating_indexes(date):
    for contour in range(1, (ContourYear.objects.all().count() + 1)):
    # for contour in range(1, 3):
        for index in range(1, (VegetationIndex.objects.all().count() + 1)):
            try:
                ActualVegIndex.objects.create(contour_id=contour, index_id=index, date=date)
                print(f'processed == {contour}')
            except Exception as e:
                with open(f'creating_indexes report-{date}.txt', 'a') as file:
                    file.write(f"{contour}' = f'{e}")
                    file.write(',')
                    file.write('\n')
                print(f'unprocessed == {contour}')
                plt.close()
                print(e)
                pass
