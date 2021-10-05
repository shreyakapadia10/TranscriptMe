# Generated by Django 3.2.6 on 2021-10-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0004_auto_20210913_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='media_type',
            field=models.CharField(choices=[('text', 'text'), ('audio', 'audio'), ('video', 'video'), ('audio url', 'audio url'), ('video url', 'video url'), ('zoom call', 'zoom call'), ('google meet', 'google meet')], max_length=15),
        ),
    ]
