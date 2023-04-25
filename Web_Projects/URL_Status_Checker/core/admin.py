from django.contrib import admin
from core.models import UrlModel


@admin.register(UrlModel)
class DeclarationAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)
