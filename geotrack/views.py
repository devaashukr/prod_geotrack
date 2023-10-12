import json
from rest_framework.views import APIView

from users.models import BusList
from .models import OperatorBuses,Operator
import requests
from .models import GeoDevDetail,ErrorDetail
import datetime
from django.db.models import Q
import logging

# Configure logging to write to /var/log/apnibus/cron.log
logging.basicConfig(filename='/var/log/apnibus/cron.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GeoBusPosition(APIView):
    def get(self,request):
        condition = Q(is_traccar_approved=True) & Q(uniqueId__isnull=False)
        busses = BusList.objects.filter(condition)
        operator_ids = []
        for bus in busses:
            if bus.operator.id not in operator_ids:
                operator_ids.append(bus.operator.id)

        for user_id in operator_ids:
            try:
                user = Operator.objects.get(id=user_id)
                condition = Q(uniqueId__isnull=False)
                busses = BusList.objects.filter(condition, operator=user_id)
                bus_nos = busses.values_list('bus_no', flat=True)
                try:
                    response = requests.get('http://blazer7.geotrackers.co.in/GTWS/gtWs/LocationWs/getUsrLatestLocation',auth=(user.username, user.password))
                    if response.status_code == 200:
                        response_json = json.loads(response.content)
                        for bus_key in bus_nos:
                            data = response_json[bus_key]
                            epoch_time = data[0]['timestamp']
                            datetime_object = datetime.datetime.fromtimestamp(epoch_time / 1000)
                            datetime_string = datetime_object.isoformat()
                            bus_list_obj = BusList.objects.get(bus_no=bus_key)
                            try:
                                pos_obj = GeoDevDetail.objects.create(operator_id=user.id, buslist_id=bus_list_obj.id, deviceid=bus_list_obj.deviceId,uniqueid=bus_list_obj.uniqueId,
                                                                      deviceTime=datetime.datetime.fromisoformat(datetime_string),fixtime=datetime.datetime.fromisoformat(datetime_string), lattitude=data[0]['lattitude'],
                                                                      longitude=data[0]['longitude'], speed=data[0]['speed'],
                                                                      address="add1",exceptionBM=data[0]['exceptionBM'],direction=data[0]['direction'],
                                                                      haltedSince=data[0]['haltedSince'],distance=data[0]['distance'],
                                                                      locStr=data[0]['locStr'],noDataSince=data[0]['noDataSince'],
                                                                      movingSince=data[0]['movingSince'],bmStr=data[0]['bmStr'])

                                pos_obj.save()

                            except Exception as e:
                                pass

                    else:
                        errorLst = [response.status_code, response.headers, response.content]
                        json_error_res = json.dumps(errorLst)
                        error_obj = ErrorDetail.objects.create(operator_id=user.id, error=json_error_res)
                        error_obj.save()

                except:
                    error_obj = ErrorDetail.objects.create(operator_id=user.id, error="GeoTracker API does not work")
                    error_obj.save()

            except:
                pass


def postDataOnTraccarApi(id,lat,lon,timestamp,speed):
    logging.info(f'Successfully posted data for id={id}')
    try:
        url = f'https://traccar-api.apnibus.com/?id={id}&lat={lat}&lon={lon}&timestamp={timestamp}&hdop=0&altitude=0&speed={speed}'
        response = requests.post(url, auth=('admin', 'admin'))
        if response.status_code == 200:
            return response.status_code
        else:
            return response.status_code
    except Exception as e:
        pass


class SendDataTraccar(APIView):
    logging.info(f'Successfully HIT CRON data for id={id}')

    def post(self,request):
        try:
            geotrack_obj = GeoDevDetail.objects.filter(is_sent_traccar=False)
            for geo_obj in geotrack_obj:
                status_code = postDataOnTraccarApi(geo_obj.uniqueid, geo_obj.lattitude, geo_obj.longitude, geo_obj.deviceTime, geo_obj.speed)
                if status_code == 200:
                    geo_obj.is_sent_traccar = True
                    geo_obj.save()

                else:
                    pass
        except Exception as e:
            pass
