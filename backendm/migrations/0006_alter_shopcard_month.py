# Generated by Django 3.2.4 on 2021-06-30 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendm', '0005_auto_20210629_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcard',
            name='month',
            field=models.IntegerField(default=0),
        ),
    ]
