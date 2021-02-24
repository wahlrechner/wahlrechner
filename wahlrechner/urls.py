from django.urls import path

from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('these', views.these, name='these'),
    path('confirm', views.confirm, name='confirm'),
    path('results', views.results, name='results'),
    path('reason', views.reason, name='reason')
]
