from django.contrib.gis.db import models


class ImageBin(models.Model):
    id_image = models.BigIntegerField(blank=True, null=True)
    image = models.FileField(upload_to='bin', blank=True, null=True)
    container_type = models.CharField(max_length=125, blank=True, null=True, verbose_name='тип емкости',
                                      default='Неизвестно')
    container_color = models.CharField(max_length=125, blank=True, null=True, verbose_name='цвет емкости',
                                       default='Неизвестно')
    missing_wheel = models.CharField(max_length=125, blank=True, null=True, verbose_name='отсутствие колеса',
                                     default='Неизвестно')
    container_upside_down = models.CharField(max_length=125, blank=True, null=True, verbose_name='емкость перевернута',
                                             default='Неизвестно')
    integrity_container_broken = models.CharField(max_length=125, blank=True, null=True,
                                                  verbose_name='целостность емкости нарушена', default='Неизвестно')
    traces_damage_containers_fire = models.CharField(max_length=125, blank=True, null=True,
                                                     verbose_name='наличие следов повреждения емкости огнем',
                                                     default='Неизвестно')
    hull_damage = models.CharField(max_length=125, blank=True, null=True, verbose_name='повреждение корпуса',
                                   default='Неизвестно')
    damage_structural_elements_waste_generation = models.CharField(max_length=125, blank=True, null=True,
                                                                   verbose_name='повреждения конструкционных элементов для погрузки отходов',
                                                                   default='Неизвестно')
    smoke = models.CharField(max_length=125, blank=True, null=True, verbose_name='дым', default='Неизвестно')
    fire = models.CharField(max_length=125, blank=True, null=True, verbose_name='огонь', default='Неизвестно')
    type_of_waste = models.CharField(max_length=125, blank=True, null=True,
                                     verbose_name='вид отходов (КГО/ТКО/РСО/Строительные отходы)', default='Неизвестно')
    object_quantity = models.CharField(max_length=10, verbose_name='Колличество распознанных объектов', blank=True, null=True)
    percent = models.CharField(max_length=255, verbose_name='Процент', blank=True, null=True)
