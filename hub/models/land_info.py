from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from hub.models import PropertyTypeList, DocumentTypeList, CategoryTypeList, LandTypeList
from hub.models.base import BaseModel


class LandInfo(BaseModel):
    history = HistoricalRecords(verbose_name=_("История"), inherit=True)
    ink_code = models.CharField(max_length=100, verbose_name=_('Код ИНК'))
    main_map = models.GeometryField(verbose_name=_('Контур'), blank=True, null=True)
    inn_pin = models.IntegerField(blank=True, null=True, verbose_name=_('ИНН'))
    # name = models.CharField(max_length=100, blank=True, null=True)
    bonitet = models.IntegerField(blank=True, null=True, verbose_name=_('Бонитет'))
    culture = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Культура'))
    crop_yield = models.DecimalField(decimal_places=2, max_digits=100, blank=True, null=True,
                                     verbose_name=_('Урожайность'))
    property_type = models.ForeignKey(PropertyTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name=_('Данные о собственности'))
    document_type = models.ForeignKey(DocumentTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name=_('Правоустанавливающие документы'))
    document_link = models.FileField(upload_to='document', blank=True, null=True, verbose_name=_('Ссылка на документ'))
    category_type = models.ForeignKey(CategoryTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name=_('Категории земель'))
    land_type = models.ForeignKey(LandTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='land_info', verbose_name=_('Данные по типам угодьев'))
    square = models.DecimalField(decimal_places=2, max_digits=100, blank=True, null=True,
                                 verbose_name=_('Фактическая площадь'))
    """Zem Balance"""
    longitude = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Долгота'))
    latitude = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Широта'))
    land_no = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Земля №'))
    territorial_outline = models.CharField(max_length=100, blank=True, null=True,
                                           verbose_name=_('Административно-территориальное деление'))
    number_realestateunits = models.CharField(max_length=100, blank=True, null=True,
                                              verbose_name=_('Количество единиц недвижимости'))
    circuit_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Номер контура'))
    doc_enttitlement = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Право на документ'))
    use_period = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Срок пользования (год/лет)'))
    certifying_act = models.CharField(max_length=55, blank=True, null=True,
                                      verbose_name=_('Удостоверяющий акт (прикрепить файл)'))
    use_end = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Дата завершения пользования'))
    agroland_purposes = models.CharField(max_length=55, blank=True, null=True,
                                         verbose_name=_('Земли сельскохозяйственного назначения'))
    gfsu = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_('Государственный фонд сельскохозяйственных угодий'))
    lands_pop_areas = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Земли населенных пунктов'))
    othertypes_lands = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Другие виды угодий'))
    type_of_land = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Земельные угодья'))
    agro_type_land = models.CharField(max_length=255, blank=True, null=True,
                                      verbose_name=_('Сельскохозяйственный вид угодий'))
    desc_brd = models.TextField(blank=True, null=True, verbose_name=_('Описания ограничения'))
    date_of_completion = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Дата заполнения'))
    perrenial_plant = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Многолетние насаждения'))
    forest_areas = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Лесные площади'))
    underwater = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Под водой'))
    otherlands = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Прочие земли'))
    collective_gardens_and_veg = models.CharField(max_length=255, blank=True, null=True,
                                                  verbose_name=_('Коллективные сады и огороды'))
    irrigated = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Орошаемые'))
    rainfed = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Богарные'))
    improved_radical = models.CharField(max_length=3, blank=True, null=True,
                                        verbose_name=_('Улучшенные (коренного улучшения)'))
    inaccessible = models.CharField(max_length=3, blank=True, null=True,
                                    verbose_name=_('Неиспользуемый из-за труднодоступности'))
    intensive_use = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Интенсивное использование'))
    pasture = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Пастбище'))
    plant_not_forestfund = models.CharField(max_length=255, blank=True, null=True,
                                            verbose_name=_('Древесно кустарниковые насаждения, не входящие в государственный лесной фонд'))
    property_form = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Форма собственности'))
    disturbed_lands = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Нарушенные земли'))
    lot_number = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Номер участка'))
    elementary_sectionnumber = models.CharField(max_length=55, blank=True, null=True,
                                                verbose_name=_('Номер элементарного участка'))

    descriptiom_doc = models.TextField(blank=True, null=True, verbose_name=_('Описание (в случае необходимости)'))
    udp = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Угодья длительного пользования'))
    limite = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Ограничения'))

    haushold_land = models.CharField(max_length=55, blank=True, null=True,
                                     verbose_name=_('Приусадебные земли и служебные наделы граждан'))
    number_of_yards = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Число дворов'))
    number_of_families = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Число семей'))
    total_land = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Всего земель'))
    crmid = models.CharField(max_length=55, blank=True, null=True)
    smcreatorid = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Создатель'))
    smownerid = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Владелец'))
    modifiedby = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Кем изменено'))
    setype = models.CharField(max_length=55, blank=True, null=True)
    description = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Описание'))
    land_ctg = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Категории Земли (Зем. Баланс)'))
    status = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Статус'))
    """Kadastr"""
    eni_code = models.CharField(max_length=35, blank=True, null=True, verbose_name=_('ЕНИ Код'))
    asr_address = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Адрес участка (АСР)'))
    special_purpose_asr = models.CharField(max_length=100, blank=True, null=True,
                                           verbose_name=_('Целевое назначение (АСР)'))
    land_factarea_asr = models.CharField(max_length=255, blank=True, null=True,
                                         verbose_name=_('Фактическая площадь (АСР)'))
    form_using_asr = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Форма использования (АСР)'))
    land_legalarea = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Юридическая площадь (АСР)'))
    owner_info = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Данные о собственнике (АСР)'))

    class Meta:
        verbose_name = _('Главная таблица')
        verbose_name_plural = _("Главная таблица")

    def __str__(self):
        return self.ink_code
