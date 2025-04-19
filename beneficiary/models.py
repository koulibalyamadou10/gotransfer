from django.db import models
import uuid

# Create your models here.
class Beneficiary(models.Model):
    customer = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='beneficiaries')
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=13, blank=False, null=False, unique=True, error_messages={
        'unique': "Ce numéro de téléphone est déjà utilisé.",
        'blank': "Ce champ ne peut pas être vide.",
        'null': "Ce champ ne peut pas être nul."
    })
    pays = models.CharField(max_length=50, blank=False, null=False)
    beneficiary_uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)