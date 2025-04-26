from django.db import models

# Create your models here.
class XRate(models.Model):
    """
    Modèle représentant les taux de change entre deux devises.
    """
    src_currency = models.CharField(max_length=3, verbose_name="Devise source")
    dst_currency = models.CharField(max_length=3, verbose_name="Devise de destination")
    ratio = models.DecimalField(max_digits=18, decimal_places=8, verbose_name="Taux de change")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")