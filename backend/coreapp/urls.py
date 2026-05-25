from django.urls import path
from .views import *

urlpatterns = [
    path("transpile/", transpile_code),
    path("run/", run_code),
]