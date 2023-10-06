from django.db import models
from users.models import Operator,OperatorBuses
import uuid

class GeoDevDetail(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True)
    operatorbus = models.ForeignKey(OperatorBuses,on_delete=models.SET_NULL, null=True)
    protocol = models.CharField(default='TCP')
    deviceid = models.BigIntegerField()
    servertime = models.BigIntegerField(default=0, null=True)
    deviceTime = models.BigIntegerField(blank=True, null=True)
    fixtime = models.BigIntegerField(default=0, null=True)
    valid = models.BooleanField(default=True)
    altitude = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    speed = models.FloatField()
    course = models.FloatField(blank=True,null=True, default=0)
    address = models.CharField(max_length=200, blank=True, null=True)
    attributes = models.CharField(max_length=200, default=0, null=True)
    accuracy = models.FloatField(default=0,null=True)

    def __str__(self):
        if self.operator is not None:
            return self.operator.username
        else:
            return "Unknown Operator"


class ErrorDetail(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL,null=True)
    busdeviceid = models.ForeignKey(OperatorBuses, on_delete=models.SET_NULL, null=True)
    error = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.busdeviceid is not None:
            return self.busdeviceid

