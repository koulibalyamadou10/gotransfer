from django.db import models
import uuid

# Create your models here.
class Statement(models.Model):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='statements')
    credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    debit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=191)
    currency = models.CharField(max_length=191)
    statement_uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.details} - {self.currency} - {self.balance}"