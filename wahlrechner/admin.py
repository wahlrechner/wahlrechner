from django.contrib import admin
from .models import These

# Register your models here.


class TheseAdmin(admin.ModelAdmin):
    list_display = ['these_nr', 'these_keyword', 'these_text']
    list_display_links = ['these_keyword']
    ordering = ['these_nr']
    search_fields = ['these_keyword', 'these_text']


admin.site.register(These, TheseAdmin)
