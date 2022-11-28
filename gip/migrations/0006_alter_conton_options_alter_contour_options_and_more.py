# Generated by Django 4.1.2 on 2022-11-28 09:33

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gip', '0005_historicalcropyield_historicalcontour_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conton',
            options={'verbose_name': 'Айыл Аймак', 'verbose_name_plural': 'Айылные Аймаки'},
        ),
        migrations.AlterModelOptions(
            name='contour',
            options={'verbose_name': 'Поле', 'verbose_name_plural': 'Поля'},
        ),
        migrations.AlterModelOptions(
            name='cropyield',
            options={'verbose_name': 'Урожайность', 'verbose_name_plural': 'Урожайность'},
        ),
        migrations.AlterModelOptions(
            name='culture',
            options={'verbose_name': 'Культура', 'verbose_name_plural': 'Культуры'},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': 'Район', 'verbose_name_plural': 'Район'},
        ),
        migrations.AlterModelOptions(
            name='farmer',
            options={'verbose_name': 'Фермер', 'verbose_name_plural': 'Фермеры'},
        ),
        migrations.AlterModelOptions(
            name='fertility',
            options={'verbose_name': 'Удобрение', 'verbose_name_plural': 'Удобрения'},
        ),
        migrations.AlterModelOptions(
            name='historicalconton',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical Айылные Аймаки'},
        ),
        migrations.AlterModelOptions(
            name='historicalcontour',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical Поля'},
        ),
        migrations.AlterModelOptions(
            name='historicalcropyield',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Урожайность', 'verbose_name_plural': 'historical Урожайность'},
        ),
        migrations.AlterModelOptions(
            name='landuse',
            options={'verbose_name': 'Землепользование', 'verbose_name_plural': 'Земепользования'},
        ),
        migrations.AlterModelOptions(
            name='landusephotos',
            options={'verbose_name': 'Фото землепользования', 'verbose_name_plural': 'Фото земепользования'},
        ),
        migrations.AlterModelOptions(
            name='orthophoto',
            options={'verbose_name': 'Спутниковый снимок', 'verbose_name_plural': 'Спутниковые снимки'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Область', 'verbose_name_plural': 'Области'},
        ),
        migrations.AlterModelOptions(
            name='soilclass',
            options={'verbose_name': 'Вид почвы', 'verbose_name_plural': 'Виды почв'},
        ),
        migrations.AlterModelOptions(
            name='soilclassmap',
            options={'verbose_name': 'Контур вида почвы', 'verbose_name_plural': 'Контуры вида почвы'},
        ),
        migrations.AlterModelOptions(
            name='soilfertility',
            options={'verbose_name': 'Плодородие почвы', 'verbose_name_plural': 'Плодородие почв'},
        ),
        migrations.AlterModelOptions(
            name='soilproductivity',
            options={'verbose_name': 'Продуктивность почвы', 'verbose_name_plural': 'Продуктивность почв'},
        ),
        migrations.AlterModelOptions(
            name='village',
            options={'verbose_name': 'Село', 'verbose_name_plural': 'Сёла'},
        ),
        migrations.AlterField(
            model_name='conton',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contons', to='gip.district', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Наименование Айылного аймака'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='conton',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contours', to='gip.conton', verbose_name='Айылный аймак'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='farmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contours', to='gip.farmer', verbose_name='Фермер'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='sum_ha',
            field=models.FloatField(blank=True, null=True, verbose_name='Площадь га'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crop_yields', to='gip.contour', verbose_name='Поле'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='culture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crop_yields', to='gip.culture', verbose_name='Культура'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='season',
            field=models.IntegerField(blank=True, null=True, verbose_name='сезон'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='weight',
            field=models.FloatField(help_text='Указыается в центнерах', verbose_name='урожайность'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='year',
            field=models.IntegerField(verbose_name='год'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='coefficient_crop',
            field=models.FloatField(verbose_name='Коеффициент урожайности'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Культура'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='district',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='district',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='district',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='district',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='gip.region', verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='district',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='district',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='mobile',
            field=models.CharField(max_length=20, verbose_name='номер телефона'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='pin_inn',
            field=models.CharField(max_length=14, verbose_name='ПИН или ИНН'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='farmers', to=settings.AUTH_USER_MODEL, verbose_name='Фермер'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование удобрения'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='district',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.district', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Наименование Айылного аймака'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='conton',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.conton', verbose_name='Айылный аймак'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='farmer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.farmer', verbose_name='Фермер'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='sum_ha',
            field=models.FloatField(blank=True, null=True, verbose_name='Площадь га'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Поле'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='culture',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.culture', verbose_name='Культура'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='season',
            field=models.IntegerField(blank=True, null=True, verbose_name='сезон'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='weight',
            field=models.FloatField(help_text='Указыается в центнерах', verbose_name='урожайность'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='year',
            field=models.IntegerField(verbose_name='год'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='land_uses', to='gip.contour', verbose_name='Поле'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='culture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='land_uses', to='gip.culture', verbose_name='Культура'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='farmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='land_uses', to='gip.farmer', verbose_name='Фермер'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='season',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сезон'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='year',
            field=models.IntegerField(verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='landusephotos',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='landusephotos',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='landusephotos',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='landusephotos',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='file',
            field=models.FileField(upload_to='ortho_photo', verbose_name='Спутниковый снимок'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='layer_name',
            field=models.CharField(max_length=55, verbose_name='Название слоя'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='url',
            field=models.URLField(max_length=1024, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='use_y_n',
            field=models.BooleanField(verbose_name='Использовать'),
        ),
        migrations.AlterField(
            model_name='region',
            name='area',
            field=models.IntegerField(verbose_name='Площадь'),
        ),
        migrations.AlterField(
            model_name='region',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='region',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='region',
            name='density',
            field=models.FloatField(verbose_name='Плотность'),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Наименование области'),
        ),
        migrations.AlterField(
            model_name='region',
            name='population',
            field=models.IntegerField(verbose_name='Население'),
        ),
        migrations.AlterField(
            model_name='region',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='region',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='fertility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soil_classes', to='gip.fertility', verbose_name='Название удобрение'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Вид почвы'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='soil_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soil_class_maps', to='gip.soilclass', verbose_name='Вид почвы'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='soil_productivity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soil_fertility', to='gip.soilproductivity', verbose_name='Продуктивность почвы'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Продуктивность почвы'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
        migrations.AlterField(
            model_name='village',
            name='conton',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='villages', to='gip.conton', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='village',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='village',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='создан пользователем'),
        ),
        migrations.AlterField(
            model_name='village',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Село'),
        ),
        migrations.AlterField(
            model_name='village',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур'),
        ),
        migrations.AlterField(
            model_name='village',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='время обновления'),
        ),
        migrations.AlterField(
            model_name='village',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='обновлён пользователем'),
        ),
    ]