# Generated by Django 4.1.7 on 2023-03-24 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trafficflowprediction', '0002_alter_carinfo_overload_alter_carinfo_overspeed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinfo',
            name='time',
            field=models.CharField(max_length=22),
        ),
    ]