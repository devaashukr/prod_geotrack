import json
from rest_framework.views import APIView
from .models import OperatorBuses,Operator
from django.db.models import F
import requests
from .models import GeoDevDetail,ErrorDetail

class GeoBusPosition(APIView):
    def get(self,request):
        busses = OperatorBuses.objects.filter(operator__is_traccar_approved=True).annotate(operator_id_fk=F('operator__id'))
        operator_ids = busses.values_list('operator_id_fk', flat=True)
        operator_ids = set(operator_ids)
        busno_devid_mp = {}
        for bus in busses:
            busno_devid_mp[bus.bus_no] = int(bus.deviceid)


        for user_id in operator_ids:
            try:
                user = Operator.objects.get(id=user_id)
                try:
                    response = requests.get('http://blazer7.geotrackers.co.in/GTWS/gtWs/LocationWs/getUsrLatestLocation',auth=(user.username, user.password))
                    if response.status_code == 200:
                        response_json = json.loads(response.content)
                        key_lst = list(response_json.keys())
                        key_lst = [key for key in key_lst if key in busno_devid_mp.keys()]
                        for bus_key in key_lst:
                            data = response_json[bus_key]
                            operator_busid = OperatorBuses.objects.get(deviceid=busno_devid_mp[bus_key])
                            try:
                                pos_obj = GeoDevDetail.objects.create(operator_id=user.id, operatorbus_id=operator_busid.id, deviceid=busno_devid_mp[bus_key],
                                                                      servertime=0,deviceTime=0,lattitude=data[0]['lattitude'],
                                                                      longitude=data[0]['longitude'], speed=data[0]['speed'],
                                                                      address="add1",exceptionBM=data[0]['exceptionBM'],direction=data[0]['direction'],
                                                                      haltedSince=data[0]['haltedSince'],
                                                                      timestamp=data[0]['timestamp'],distance=data[0]['distance'],
                                                                      locStr=data[0]['locStr'],noDataSince=data[0]['noDataSince'],
                                                                      movingSince=data[0]['movingSince'],bmStr=data[0]['bmStr'])

                                pos_obj.save()

                            except Exception as e:
                                # print("this is the exception new", e)
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









