from django.urls import path
from . import views
urlpatterns = [
    path('' , views.register_vendor , name="register_vendor")
]