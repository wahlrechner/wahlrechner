from django.contrib import admin
from .models import These, Antwort, Partei

# Register your models here.


class TheseAdmin(admin.ModelAdmin):
    list_display = ['these_nr', 'these_keyword', 'these_text']
    list_display_links = ['these_keyword']
    ordering = ['these_nr']
    search_fields = ['these_keyword', 'these_text']


class AntwortAdmin(admin.ModelAdmin):
    list_display = ['antwort_partei',
                    'antwort_these', 'antwort_position']
    list_display_links = ['antwort_partei', 'antwort_these']
    search_fields = ['antwort_these', 'antwort_partei']
    list_filter = ['antwort_partei']
    autocomplete_fields = ['antwort_these', 'antwort_partei']


class ParteiAdmin(admin.ModelAdmin):
    search_fields = ['partei_name']


admin.site.register(These, TheseAdmin)
admin.site.register(Antwort, AntwortAdmin)
admin.site.register(Partei, ParteiAdmin)
