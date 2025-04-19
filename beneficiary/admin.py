from django.contrib import admin
from .models import Beneficiary

# Register your models here.
@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Beneficiary._meta.fields]