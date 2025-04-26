from django.db import models
import uuid

# Create your models here.
class Remittance(models.Model):
    transaction_id = models.CharField(max_length=255)
    sender = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="remittances")
    role = models.ForeignKey('beneficiary.Beneficiary', related_name="remittance_beneficiaries", on_delete=models.CASCADE)
    cashout_location = models.CharField(max_length=255)
    payout_option = models.CharField(max_length=255)
    amount_sent = models.DecimalField(max_digits=18, decimal_places=2)
    sender_currency = models.CharField(max_length=255)
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=2)
    recipient_amount = models.DecimalField(max_digits=18, decimal_places=2)
    agent_profit = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    fees = models.DecimalField(max_digits=18, decimal_places=2)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=255)
    transaction_completion_date = models.DateTimeField(null=True, blank=True)
    agent_start_username = models.CharField(max_length=255, default='') 
    agent_completion_username = models.CharField(max_length=255, default='')
    comments = models.TextField(blank=True, null=True, default='')
    partner_code = models.CharField(max_length=255, blank=True, null=True, default='')
    remittance_uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"REM-{self.remittance_uuid}"
        super().save(*args, **kwargs)