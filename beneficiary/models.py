from django.db import models
import uuid

# Create your models here.
class Beneficiary(models.Model):
    customer = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='beneficiaries')
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=13, blank=False, null=False, error_messages={
        'blank': "Ce champ ne peut pas être vide.",
        'null': "Ce champ ne peut pas être nul."
    })
    country_code = models.CharField(max_length=5, blank=False, null=False, error_messages={
        'blank': "Ce champ ne peut pas être vide.",
        'null': "Ce champ ne peut pas être nul."
    })      
    country_currency = models.CharField(max_length=5, blank=False, null=False, error_messages={
        'blank': "Ce champ ne peut pas être vide.",
        'null': "Ce champ ne peut pas être nul."
    }, default='GNF')
    pays = models.CharField(max_length=50, blank=False, null=False)
    beneficiary_uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    active = models.BooleanField(default=True)
    id_card = models.CharField(max_length=191)
    id_exp_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)