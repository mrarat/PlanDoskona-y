from django.urls import path

from . import views

urlpatterns = [
    path("", views.MyMessageView.as_view(), name="mymessage")   ,
]