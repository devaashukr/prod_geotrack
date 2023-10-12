import requests
from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import json
# import requests

class Operator(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    platform = models.CharField(max_length=200,choices = (
            ('plat1', 'GeoTracker'),
            ('plat2', 'GpsTracker'),
            ('plat3', 'Tacker'),
        ))
    is_active = models.BooleanField(default=True,blank=True)
    is_geotrak_approved = models.BooleanField(default=False, blank=True)
    bus_details = models.JSONField(blank=True, null=True)
    bus_list = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.username

class OperatorBuses(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, related_name='operator')
    deviceid = models.CharField(db_index=True)
    bus_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.deviceid

    class Meta:
        db_table = 'operator_buses'


class BusList(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True)
    bus_no = models.CharField(max_length=100)
    uniqueId = models.BigIntegerField(blank=True,null=True)
    deviceId = models.BigIntegerField(blank=True,null=True)
    is_traccar_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.bus_no


@receiver(post_save, sender=Operator)
def operator_register_signal(sender, instance, created, **kwargs):
    if not created:
        return
    username = instance.username
    password = instance.password

    try:
        response = requests.get('http://blazer7.geotrackers.co.in/GTWS/gtWs/LocationWs/getUsrLatestLocation',auth=(username, password))

        user = Operator.objects.get(username=instance.username)
        if response.status_code == 200:
            content = response.content
            data_str = content.decode('utf-8')
            data_dict = json.loads(data_str)
            bus_nums = [key for key in data_dict]
            for bus in bus_nums:
                obj = BusList.objects.create(operator_id=user.id,bus_no=bus)
                obj.save()
            bus_nums_json = json.dumps({"bus_nums": bus_nums}, indent=4).strip("\n")
            existing_data = json.loads(user.bus_details) if user.bus_details else None

            if existing_data != data_dict:
                user.bus_details = data_str
                user.bus_list = bus_nums_json
                user.save()

        else:
            errorLst = [response.status_code, response.headers, response.content]
            json_error_res = json.dumps(errorLst)

            if user.bus_details != json_error_res:
                user.bus_details = json_error_res
                user.save()

    except:
        pass


@receiver(post_save, sender=BusList)
def traccar_approval_signal(sender, instance, **kwargs):
    if instance.is_traccar_approved and not instance.uniqueId:
        try:
            response = requests.get('https://traccar-api.apnibus.com/api/devices',
                                    auth=('admin', 'admin'))
            if response.status_code == 200:
                content = response.content
                data_str = content.decode('utf-8')
                data_dict = json.loads(data_str)
                bus = BusList.objects.get(bus_no=instance.bus_no)
                for data in data_dict:
                    if data['name'] == bus.bus_no:
                        bus.uniqueId = data['uniqueId']
                        bus.deviceId = data['id']
                        bus.is_traccar_approved = True
                        bus.save()
                        break

        except Exception as e:
            print(f"Error: {str(e)}")

