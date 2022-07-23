from django.urls import path

from . import views

urlpatterns = [
    path("", views.start, name="start"),
    path("these", views.these, name="these"),
    path("confirm", views.confirm, name="confirm"),
    path("results", views.results, name="results"),
    path("reason", views.reason, name="reason"),
    path("test404", views.test404, name="test404"),
    path("test500", views.test500, name="test500"),
]
