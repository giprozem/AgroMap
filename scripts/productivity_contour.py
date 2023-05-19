from pickle5 import pickle
from gip.models import Contour
from django.db.models import Avg


def run():
    # Получаем среднее значение average_value для каждого контура
    contours = Contour.objects.filter(
        type_id=2,
        actual_veg_index__index_id=1,
        actual_veg_index__date__range=('2022-04-01', '2022-11-01')
    ).annotate(avg_value=Avg('actual_veg_index__average_value'))

    with open(f'K_Nearest_Neighbors_Regressor_model_65.pkl', 'rb') as f:
        model = pickle.load(f)

    for contour in contours:
        avg_value = contour.avg_value if contour.avg_value is not None else 0  # or some default value
        elevation = contour.elevation if contour.elevation is not None else 0  # or some default value
        soil_class_id = contour.soil_class_id if contour.soil_class_id is not None else 0  # or some default value

        Contour.objects.filter(id=contour.id).update(
            predicted_productivity=round(
                model.predict([[avg_value, elevation, soil_class_id]])[0], 2
            ),
        )
