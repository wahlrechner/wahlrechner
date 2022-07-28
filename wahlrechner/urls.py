from django.urls import path

from . import views

urlpatterns = [
    path("", views.start, name="start"),
    path(
        "these/<int:these_pk>/<str:zustand>",
        views.these,
        name="these",
    ),
    path("confirm/<str:zustand>", views.confirm, name="confirm"),
    path("confirm/<str:zustand>/submit", views.confirm_submit, name="confirm_submit"),
    path("result/<str:zustand>", views.result, name="result"),
    path("reason/<int:these_pk>/<str:zustand>", views.reason, name="reason"),
    path("test404", views.test404, name="test404"),
    path("test500", views.test500, name="test500"),
]
