from rest_framework.urls import path
from .views import GeoBusPosition, SendDataTraccar

urlpatterns = [
    path('get-bus-position/', GeoBusPosition.as_view()),
    path('send-pos-traccar/', SendDataTraccar.as_view())
]