from django.db import models


# Create your models here.
class CarInfo(models.Model):
    lane_name = models.CharField(max_length=15)
    lane_code = models.CharField(max_length=7)
    time = models.CharField(max_length=22)
    car_type = models.CharField(max_length=3)
    speed = models.PositiveSmallIntegerField()
    car_length = models.PositiveSmallIntegerField()
    axles = models.PositiveSmallIntegerField()
    total_weight = models.PositiveSmallIntegerField()
    axle1_weight = models.PositiveSmallIntegerField()
    axle2_weight = models.PositiveSmallIntegerField()
    axle3_weight = models.PositiveSmallIntegerField()
    axle4_weight = models.PositiveSmallIntegerField()
    axle5_weight = models.PositiveSmallIntegerField()
    axle6_weight = models.PositiveSmallIntegerField()
    axle7_weight = models.PositiveSmallIntegerField()
    axle8_weight = models.PositiveSmallIntegerField()
    axle9_weight = models.PositiveSmallIntegerField()
    axle10_weight = models.PositiveSmallIntegerField()
    overload = models.CharField(max_length=5)
    overspeed = models.CharField(max_length=5)
    state = models.CharField(max_length=5)

    class Meta:
        permissions = ()
