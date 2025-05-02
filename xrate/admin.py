from django.contrib import admin
from .models import XRate

# Register your models here.
@admin.register(XRate)
class FeesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in XRate._meta.fields]