from django.contrib import admin
from .models import Fees

# Register your models here.
@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Fees._meta.fields]