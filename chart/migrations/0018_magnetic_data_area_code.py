# Generated by Django 3.1.6 on 2021-03-23 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0017_auto_20210323_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='magnetic_data',
            name='area_code',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]