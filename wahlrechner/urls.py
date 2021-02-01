from django.urls import path

from . import views

urlpatterns = [
    path('these', views.these, name='these'),
]
