from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Antwort, Partei, These

# Register your models here.


class AntwortResource(resources.ModelResource):
    class Meta:
        model = Antwort


class AntwortAdmin(ImportExportModelAdmin):
    list_display = ["antwort_partei", "antwort_these", "antwort_position"]
    list_display_links = ["antwort_partei", "antwort_these"]
    search_fields = [
        "antwort_these__these_text",
        "antwort_these__these_keyword",
        "antwort_partei__partei_name",
    ]
    list_filter = ["antwort_partei"]
    autocomplete_fields = ["antwort_these", "antwort_partei"]
    resource_class = AntwortResource


class AntwortInLine(admin.TabularInline):
    model = Antwort
    extra = 1


class TheseResource(resources.ModelResource):
    class Meta:
        model = These


class TheseAdmin(ImportExportModelAdmin):
    list_display = ["these_nr", "these_keyword", "these_text"]
    list_display_links = ["these_keyword"]
    ordering = ["these_nr"]
    search_fields = ["these_keyword", "these_text"]
    inlines = [AntwortInLine]
    resource_class = TheseResource


class ParteiResource(resources.ModelResource):
    class Meta:
        model = Partei


class ParteiAdmin(ImportExportModelAdmin):
    search_fields = ["partei_name"]
    resource_class = ParteiResource


admin.site.register(These, TheseAdmin)
admin.site.register(Antwort, AntwortAdmin)
admin.site.register(Partei, ParteiAdmin)
