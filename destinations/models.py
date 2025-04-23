from django.db import models
import uuid

# Create your models here.
class Destination(models.Model):
    country_name = models.CharField(max_length=50)
    country_code = models.IntegerField()
    city_name = models.CharField(max_length=50)
    currency = models.CharField(max_length=5)
    direction = models.CharField(max_length=10)
    destination_uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
