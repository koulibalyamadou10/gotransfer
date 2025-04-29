from django.db import models
import uuid

# Create your models here.
class Topup(models.Model):
    transaction_id = models.CharField(max_length=255)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    role = models.ForeignKey('beneficiary.Beneficiary', on_delete=models.CASCADE)
    recipient_number = models.CharField(max_length=255)
    operator = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=255)
    selling_currency = models.CharField(max_length=255)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    agent_profit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=[
        ('requested', 'REQUESTED'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='requested')
    sender_first_name = models.CharField(max_length=255)
    sender_last_name = models.CharField(max_length=255)
    sender_telephone = models.CharField(max_length=255)
    agent_username = models.CharField(max_length=255, default='', null=True, blank=True)
    topup_uuid = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)