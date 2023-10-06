from django.shortcuts import render
from rest_framework.views import APIView

class GeoTrackerPost(APIView):
    def post(self,request):
        pass


class GetTrackerInfoAfterRegister(APIView):
    def get(self,username, password):
        pass
