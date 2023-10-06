from django.db import models
from users.models import Operator,OperatorBuses
import uuid

class GeoDevDetail(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, related_name='geodevdetails')
    operatorbus = models.ForeignKey(OperatorBuses,on_delete=models.CASCADE, null=True, related_name='geodevdetails')
    protocol = models.CharField(default='TCP', null=True)
    deviceid = models.BigIntegerField(blank=True,null=True)
    servertime = models.BigIntegerField(default=0, null=True)
    deviceTime = models.BigIntegerField(default=True, null=True)
    lattitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True,null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    speed = models.FloatField(blank=True,null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    exceptionBM = models.BigIntegerField(blank=True,null=True)
    direction = models.IntegerField(blank=True,null=True)
    haltedSince = models.CharField(max_length=200,blank=True,null=True)
    timestamp = models.BigIntegerField(blank=True,null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    locStr = models.CharField(max_length=200,blank=True,null=True)
    noDataSince = models.CharField(max_length=200,blank=True,null=True)
    movingSince = models.CharField(max_length=200,blank=True,null=True)
    bmStr = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        if self.operator is not None:
            return self.operator.username
        else:
            print("i m in else condition")
            return


class ErrorDetail(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE,null=True)
    busdeviceid = models.ForeignKey(OperatorBuses, on_delete=models.CASCADE, null=True)
    error = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.busdeviceid is not None:
            return self.busdeviceid

