from django.db import models
from users.models import Operator,OperatorBuses
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
import requests
import json

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
            return self.operatorbus.bus_no
        else:
            return


class ErrorDetail(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE,null=True)
    operatorbus = models.ForeignKey(OperatorBuses,on_delete=models.CASCADE,null=True)
    error = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.operatorbus.id is not None:
            return self.operatorbus.bus_no
        else:
            return


@receiver(post_save, sender=GeoDevDetail)
def isGeoTrakDataSameAsTraccar(sender, instance, created, **kwargs):
    if created:
        bus_no = instance.operatorbus.bus_no
        try:
            response = requests.get(f'https://traccar-api.apnibus.com/api/positions/byBusNumber/{bus_no}',
                                    auth=('admin', 'admin'))
            if response.status_code == 200:
                content = response.content
                data_str = content.decode('utf-8')
                json_data = json.loads(data_str)
                if round(instance.lattitude, 2) == round(json_data['latitude'],2) and round(instance.longitude,2) == round(json_data['longitude'],2) and round(instance.speed,2) == round(json_data['speed'],2):
                    print("success")
                    pass

                else:
                    print("error 1")
                    err_obj = ErrorDetail.objects.create(operator_id=instance.operator.id,operatorbus=instance.operatorbus.id, error="GeoTracker and traccar data not matched")
                    err_obj.save()

            else:
                err_obj = ErrorDetail.objects.create(operator_id=instance.operator.id, operatorbus_id=instance.operatorbus.id,
                                                     error=f'Bus {bus_no} does not found on traccar')
                err_obj.save()

        except:
            pass





