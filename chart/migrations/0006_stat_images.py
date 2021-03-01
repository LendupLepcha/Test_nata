# Generated by Django 3.1.6 on 2021-03-01 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0005_auto_20210219_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stat_Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sun', models.IntegerField(blank=True, default='default.png')),
                ('moon', models.IntegerField(blank=True, default='default.png')),
                ('mercury', models.IntegerField(blank=True, default='default.png')),
                ('venus', models.IntegerField(blank=True, default='default.png')),
                ('mars', models.IntegerField(blank=True, default='default.png')),
                ('jupiter', models.IntegerField(blank=True, default='default.png')),
                ('saturn', models.IntegerField(blank=True, default='default.png')),
                ('uranus', models.IntegerField(blank=True, default='default.png')),
                ('neptune', models.IntegerField(blank=True, default='default.png')),
                ('pluto', models.IntegerField(blank=True, default='default.png')),
                ('ceres', models.IntegerField(blank=True, default='default.png')),
                ('chart_frame', models.IntegerField(blank=True, default='default.png')),
                ('aspact_frame', models.IntegerField(blank=True, default='default.png')),
                ('conjunction', models.IntegerField(blank=True, default='default.png')),
                ('opposition', models.IntegerField(blank=True, default='default.png')),
                ('square', models.IntegerField(blank=True, default='default.png')),
                ('sextile', models.IntegerField(blank=True, default='default.png')),
                ('trine', models.IntegerField(blank=True, default='default.png')),
            ],
        ),
    ]
