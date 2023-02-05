from django.urls import path, include
from .views import *

urlpatterns = [
    path('weekly_report', download_last_week_report),
]
