# Generated by Django 4.2.4 on 2023-09-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0004_alter_dataconfig_simulater'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulator',
            name='producer_type',
            field=models.CharField(choices=[('csv', 'csv'), ('xml', 'xsml'), ('sql', 'sql')], max_length=25),
        ),
    ]
