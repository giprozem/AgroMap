# Generated by Django 4.1.2 on 2023-04-26 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_notifications'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
    ]
