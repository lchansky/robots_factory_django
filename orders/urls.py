from django.urls import path, include
from .views import *

urlpatterns = [
    path('new', order_new, name='order_new'),
]
