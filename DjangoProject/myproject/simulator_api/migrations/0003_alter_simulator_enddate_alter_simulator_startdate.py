# Generated by Django 4.2.4 on 2023-09-05 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0002_alter_simulator_enddate_alter_simulator_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulator',
            name='endDate',
            field=models.DateTimeField(default=''),
        ),
        migrations.AlterField(
            model_name='simulator',
            name='startDate',
            field=models.DateTimeField(),
        ),
    ]
