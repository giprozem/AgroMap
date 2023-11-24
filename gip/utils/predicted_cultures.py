import pandas as pd
from pycaret.classification import load_model

from django.db import connection


import json

import pandas as pd

from gip.models import Contour, Culture


def get_crop_name_by_int(crop_dict, int_value):
    for key, value in crop_dict.items():
        if value == int_value:
            return key
    return None


def process_contour_data(data):
    loaded_bestmodel = load_model("./models_predicted/predicted_culture_24112023")

    crop_dict = {
        'Ячмень': 0,
        'Пшеница': 2,
        'Кукуруза': 3,
        'Свекла': 4,
    }

    df = pd.DataFrame([data])
    df2pred = df.iloc[:, :6]
    predict = loaded_bestmodel.predict(df2pred)
    int_value = predict[0]
    culture_name = get_crop_name_by_int(crop_dict, int_value)

    return culture_name


def data_contour(contour):
    if contour.type.name_en in ['Cropland'] and contour.conton.district.region.id == 10:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT
                                c.id AS contour_id,
                                EXTRACT(MONTH FROM av.date) AS month,
                                St_AsGeoJSON(c.polygon),
                                vi.name AS IndexType,
                                av.average_value AS AverageValue,
                                av.date AS "Analysis Date",
                                c.year AS "year contour",
                                c.elevation AS elevation_contour,
                                dis.name AS district_name,
                                sc.id_soil AS SOIL_ID,
                                sc.name AS SOIL_NAME,
                                cul.name AS culture_name,
                                ct.name AS type_culture_name
                            FROM
                                gip_contour c
                            JOIN indexes_actualvegindex av ON av.contour_id = c.id
                            JOIN culture_model_vegetationindex vi ON av.index_id = vi.id
                            LEFT JOIN gip_conton co ON c.conton_id = co.id
                            LEFT JOIN gip_district dis ON co.district_id = dis.id
                            LEFT JOIN gip_culture cul ON c.culture_id = cul.id
                            LEFT JOIN gip_culturetype ct ON cul.culture_type_id = ct.id
                            LEFT JOIN gip_soilclass sc ON c.soil_class_id = sc.id
                            WHERE
                                vi.name IN ('NDVI', 'NDWI', 'SAVI', 'VARI')
                                AND c.id = {contour.id}
                                AND EXTRACT(MONTH FROM av.date) BETWEEN 4 AND 8
                            ORDER BY
                                c.id, av.date;
                                """)
                rows = cursor.fetchall()
                data_dict = {}
                for row in rows:
                    month = int(row[1])
                    if 'index_data' not in data_dict:
                        data_dict['index_data'] = {
                            f"index_month_4": None,
                            f"index_month_5": None,
                            f"index_month_6": None,
                            f"index_month_7": None,
                            f"index_month_8": None,
                            "elevation": None,
                        }
                    data_dict['index_data'][f"index_month_{month}"] = float(row[4]) if row[4] is not None else None
                    data_dict['index_data']["elevation"] = float(row[7]) if row[7] is not None else None
                crop_name = process_contour_data(data_dict['index_data'])
                culture_obj = Culture.objects.filter(name_ru__iexact=crop_name).first().id
                Contour.objects.filter(id=contour.id).update(predicted_culture=culture_obj)
        except Exception as e:
            print(e)
