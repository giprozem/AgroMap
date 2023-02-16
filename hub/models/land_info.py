from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords

from hub.models import PropertyTypeList, DocumentTypeList, CategoryTypeList, LandTypeList
from hub.models.base import BaseModel


class LandInfo(BaseModel):
    history = HistoricalRecords(verbose_name="История", inherit=True)
    ink_code = models.CharField(max_length=100, verbose_name='Код ИНК')
    main_map = models.GeometryField(verbose_name='Контур', blank=True, null=True)
    inn_pin = models.IntegerField(blank=True, null=True, verbose_name='ИНН')
    # name = models.CharField(max_length=100, blank=True, null=True)
    bonitet = models.IntegerField(blank=True, null=True, verbose_name='Бонитет')
    culture = models.CharField(max_length=255, blank=True, null=True, verbose_name='Культура')
    crop_yield = models.DecimalField(decimal_places=2, max_digits=100, blank=True, null=True,
                                     verbose_name='Урожайность')
    property_type = models.ForeignKey(PropertyTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name='данные о собственности')
    document_type = models.ForeignKey(DocumentTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name='правоустанавливающие документы')
    document_link = models.FileField(upload_to='document', blank=True, null=True, verbose_name='Ссылка на документ')
    category_type = models.ForeignKey(CategoryTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name='категории земель')
    land_type = models.ForeignKey(LandTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='land_info', verbose_name='данные по типам угодьев')
    square = models.DecimalField(decimal_places=2, max_digits=100, blank=True, null=True,
                                 verbose_name='Фактическая площадь')
    """Zem Balance"""
    longitude = models.CharField(max_length=100, blank=True, null=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, blank=True, null=True, verbose_name='Широта')
    land_no = models.CharField(max_length=100, blank=True, null=True, verbose_name='Земля №')
    territorial_outline = models.CharField(max_length=100, blank=True, null=True,
                                           verbose_name='Административно-территориальное деление')
    number_realestateunits = models.CharField(max_length=100, blank=True, null=True,
                                              verbose_name='Количество единиц недвижимости')
    circuit_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Номер контура')
    doc_enttitlement = models.CharField(max_length=255, blank=True, null=True, verbose_name='Право на документ')
    use_period = models.CharField(max_length=55, blank=True, null=True, verbose_name='Срок пользования (год/лет)')
    certifying_act = models.CharField(max_length=55, blank=True, null=True,
                                      verbose_name='Удостоверяющий акт (прикрепить файл)')
    use_end = models.CharField(max_length=55, blank=True, null=True, verbose_name='Дата завершения пользования')
    agroland_purposes = models.CharField(max_length=55, blank=True, null=True,
                                         verbose_name='Земли сельскохозяйственного назначения')
    gfsu = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name='Государственный фонд сельскохозяйственных угодий')
    lands_pop_areas = models.CharField(max_length=55, blank=True, null=True, verbose_name='Земли населенных пунктов')
    othertypes_lands = models.CharField(max_length=55, blank=True, null=True, verbose_name='Другие виды угодий')
    type_of_land = models.CharField(max_length=255, blank=True, null=True, verbose_name='Земельные угодья')
    agro_type_land = models.CharField(max_length=255, blank=True, null=True,
                                      verbose_name='Сельскохозяйственный вид угодий')
    desc_brd = models.TextField(blank=True, null=True, verbose_name='Описания ограничения')
    date_of_completion = models.CharField(max_length=55, blank=True, null=True, verbose_name='Дата заполнения')
    perrenial_plant = models.CharField(max_length=255, blank=True, null=True, verbose_name='Многолетние насаждения')
    forest_areas = models.CharField(max_length=255, blank=True, null=True, verbose_name='Лесные площади')
    underwater = models.CharField(max_length=255, blank=True, null=True, verbose_name='Под водой')
    otherlands = models.CharField(max_length=255, blank=True, null=True, verbose_name='Прочие земли')
    collective_gardens_and_veg = models.CharField(max_length=255, blank=True, null=True,
                                                  verbose_name='Коллективные сады и огороды')
    irrigated = models.CharField(max_length=3, blank=True, null=True, verbose_name='Орошаемые')
    rainfed = models.CharField(max_length=3, blank=True, null=True, verbose_name='Богарные')
    improved_radical = models.CharField(max_length=3, blank=True, null=True,
                                        verbose_name='Улучшенные (коренного улучшения)')
    inaccessible = models.CharField(max_length=3, blank=True, null=True,
                                    verbose_name='Неиспользуемый из-за труднодоступности')
    intensive_use = models.CharField(max_length=3, blank=True, null=True, verbose_name='Интенсивное использование')
    pasture = models.CharField(max_length=255, blank=True, null=True, verbose_name='Пастбище')
    plant_not_forestfund = models.CharField(max_length=255, blank=True, null=True,
                                            verbose_name='Древесно кустарниковые насаждения, не входящие в государственный лесной фонд')
    property_form = models.CharField(max_length=255, blank=True, null=True, verbose_name='Форма собственности')
    disturbed_lands = models.CharField(max_length=255, blank=True, null=True, verbose_name='Нарушенные земли')
    lot_number = models.CharField(max_length=55, blank=True, null=True, verbose_name='Номер участка')
    elementary_sectionnumber = models.CharField(max_length=55, blank=True, null=True,
                                                verbose_name='Номер элементарного участка')

    descriptiom_doc = models.TextField(blank=True, null=True, verbose_name='Описание (в случае необходимости)')
    udp = models.CharField(max_length=255, blank=True, null=True, verbose_name='Угодья длительного пользования')
    limite = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ограничения')

    haushold_land = models.CharField(max_length=55, blank=True, null=True,
                                     verbose_name='Приусадебные земли и служебные наделы граждан')
    number_of_yards = models.CharField(max_length=55, blank=True, null=True, verbose_name='Число дворов')
    number_of_families = models.CharField(max_length=55, blank=True, null=True, verbose_name='Число семей')
    total_land = models.CharField(max_length=55, blank=True, null=True, verbose_name='Всего земель')
    crmid = models.CharField(max_length=55, blank=True, null=True)
    smcreatorid = models.CharField(max_length=55, blank=True, null=True)
    smownerid = models.CharField(max_length=55, blank=True, null=True)
    modifiedby = models.CharField(max_length=55, blank=True, null=True)
    setype = models.CharField(max_length=55, blank=True, null=True)
    description = models.CharField(max_length=55, blank=True, null=True)
    land_ctg = models.CharField(max_length=100, blank=True, null=True, verbose_name='Категории Земли (Зем. Баланс)')
    status = models.CharField(max_length=55, blank=True, null=True)
    """Kadastr"""
    eni_code = models.CharField(max_length=35, blank=True, null=True, verbose_name='ЕНИ Код')
    asr_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Адрес участка (АСР)')
    special_purpose_asr = models.CharField(max_length=100, blank=True, null=True,
                                           verbose_name='Целевое назначение (АСР)')
    land_factarea_asr = models.CharField(max_length=255, blank=True, null=True,
                                         verbose_name='Фактическая площадь (АСР)')
    form_using_asr = models.CharField(max_length=55, blank=True, null=True, verbose_name='Форма использования (АСР)')
    land_legalarea = models.CharField(max_length=100, blank=True, null=True, verbose_name='Юридическая площадь (АСР)')
    owner_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='Данные о собственнике (АСР)')

    class Meta:
        verbose_name = 'Главная таблица'
        verbose_name_plural = "Главная таблица"

    def __str__(self):
        return self.ink_code
