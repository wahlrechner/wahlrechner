from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("wahlrechner.urls")),
    path("admin/", admin.site.urls),
]

admin.site.site_header = "Wahlrechner Admin"
admin.site.site_title = "Wahlrechner Admin"
admin.site.index_title = "Konfiguration"

handler404 = "wahlrechner.views.handler404"
handler500 = "wahlrechner.views.handler500"
