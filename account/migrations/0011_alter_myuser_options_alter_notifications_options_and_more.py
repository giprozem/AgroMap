# Generated by Django 4.1.2 on 2023-06-29 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_myuser_options_alter_notifications_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='notifications',
            options={'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_employee',
            field=models.BooleanField(default=False, verbose_name='Работник'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_farmer',
            field=models.BooleanField(default=False, verbose_name='Фермер'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Администратор'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_supervisor',
            field=models.BooleanField(default=False, verbose_name='Наблюдатель'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Прочитано'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='text',
            field=models.CharField(max_length=100, verbose_name='Текст уведомления'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='text_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Текст уведомления'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='text_ky',
            field=models.CharField(max_length=100, null=True, verbose_name='Текст уведомления'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='text_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Текст уведомления'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(max_length=55, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='my_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profiles', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=14, verbose_name='Номер телефона'),
        ),
    ]