#url patterns
from django.urls import path
from django.conf import settings
from . import views
urlpatterns = [
    path(r'main', views.home, name="main"),
    path(r'order', views.menu, name="order"),
    path(r'confirmation', views.receipt, name="confirmation"),
]