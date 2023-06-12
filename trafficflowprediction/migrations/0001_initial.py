# Generated by Django 4.1.7 on 2023-03-24 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lane_name', models.CharField(max_length=15)),
                ('lane_code', models.CharField(max_length=7)),
                ('time', models.TimeField()),
                ('car_type', models.CharField(max_length=3)),
                ('speed', models.PositiveSmallIntegerField()),
                ('car_length', models.PositiveSmallIntegerField()),
                ('axles', models.PositiveSmallIntegerField()),
                ('total_weight', models.PositiveSmallIntegerField()),
                ('axle1_weight', models.PositiveSmallIntegerField()),
                ('axle2_weight', models.PositiveSmallIntegerField()),
                ('axle3_weight', models.PositiveSmallIntegerField()),
                ('axle4_weight', models.PositiveSmallIntegerField()),
                ('axle5_weight', models.PositiveSmallIntegerField()),
                ('axle6_weight', models.PositiveSmallIntegerField()),
                ('axle7_weight', models.PositiveSmallIntegerField()),
                ('axle8_weight', models.PositiveSmallIntegerField()),
                ('axle9_weight', models.PositiveSmallIntegerField()),
                ('axle10_weight', models.PositiveSmallIntegerField()),
                ('overload', models.BooleanField()),
                ('overspeed', models.BooleanField()),
                ('state', models.BooleanField()),
            ],
            options={
                'permissions': (),
            },
        ),
    ]