from django.contrib import admin
from .models import Remittance  # Import the Remittance model

# Register your models here.
@admin.register(Remittance)
class RemittanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Remittance._meta.fields if field.name != 'id']
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20