from django.db import models

# Create your models here.
class Fees(models.Model):
    src_country = models.CharField(max_length=50)
    dst_country = models.CharField(max_length=50)
    from_amount = models.DecimalField(max_digits=10, decimal_places=2)
    to_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_fees = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)