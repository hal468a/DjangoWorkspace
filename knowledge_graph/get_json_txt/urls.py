from django.urls import path
from . import views

urlpatterns = [
    path('get_json_txt/', views.receive_json, name='receive_json'),
]