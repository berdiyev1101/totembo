from django.urls import path
from totembo.views import *
urlpatterns = [
    path("", index, name="index")
]