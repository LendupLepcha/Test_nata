# Generated by Django 3.1.6 on 2021-03-03 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chart', '0011_auto_20210303_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
