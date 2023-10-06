import requests
from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
# import requests

class Operator(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    platform = models.CharField(max_length=200,choices = (
            ('plat1', 'GeoTracker'),
            ('plat2', 'GpsTracker'),
            ('plat3', 'Tacker'),
        ))
    # other = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True,blank=True)
    bus_details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.username

class OperatorBuses(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, related_name='operator')
    deviceid = models.CharField(db_index=True)
    tracker_approved = models.BooleanField(default=False)
    bus_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.deviceid

    class Meta:
        db_table = 'operator_buses'

import json
@receiver(post_save, sender=Operator)
def operator_register_signal(sender, instance, created, **kwargs):
    username = instance.username
    password = instance.password

    try:
        response = requests.get('http://blazer7.geotrackers.co.in/GTWS/gtWs/LocationWs/getUsrLatestLocation',
                                auth=(username, password))

        user = Operator.objects.get(username=instance.username)
        if response.status_code == 200:
            content = response.content
            data_str = content.decode('utf-8')
            data_dict = json.loads(data_str)

            existing_data = json.loads(user.bus_details) if user.bus_details else None

            if existing_data != data_dict:
                user.bus_details = data_str
                user.save()

        else:
            errorLst = [response.status_code, response.headers, response.content]
            json_error_res = json.dumps(errorLst)

            if user.bus_details != json_error_res:
                user.bus_details = json_error_res
                user.save()

    except:
        pass
