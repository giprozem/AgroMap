# Generated by Django 4.1.2 on 2023-04-19 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0010_alter_ai_found_options_alter_contour_ai_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
