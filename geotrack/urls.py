from rest_framework.urls import path
from .views import GeoBusPosition

urlpatterns = [
    path('get-bus-position/', GeoBusPosition.as_view()),
]