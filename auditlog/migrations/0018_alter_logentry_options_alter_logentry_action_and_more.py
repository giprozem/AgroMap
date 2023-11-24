# Generated by Django 4.1.2 on 2023-09-27 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auditlog', '0017_alter_logentry_options_alter_logentry_content_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logentry',
            options={'get_latest_by': 'timestamp', 'ordering': ['-timestamp'], 'verbose_name': 'Change Log', 'verbose_name_plural': 'Change Logs'},
        ),
        migrations.AlterField(
            model_name='logentry',
            name='action',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Created'), (1, 'Updated'), (2, 'Deleted'), (3, 'Accessed')], db_index=True, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='additional_data',
            field=models.JSONField(blank=True, null=True, verbose_name='Additional Data'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='changes',
            field=models.JSONField(null=True, verbose_name='Message Text'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='changes_text',
            field=models.TextField(blank=True, verbose_name='Change Text'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='cid',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Correlation ID'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.contenttype', verbose_name='Content Type'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='object_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='object_pk',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='object_repr',
            field=models.TextField(verbose_name='Representation'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='remote_addr',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='Remote Address'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Time'),
        ),
    ]