from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class Location(models.Model):
    LEVEL_CHOICES = [
        ('division', 'Division'),
        ('zilla', 'Zilla'),
        ('upazila', 'Upazila'),
        ('union', 'Union'),
    ]

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return f"{self.name} ({self.level})"

    class Meta:
        unique_together = ('name', 'level', 'parent')


class TemporaryOrders(models.Model):
    phonenumber = models.CharField(max_length=20)
    ordered_products = models.TextField()
    total = models.FloatField()
    del_adress = models.TextField(null=True, blank=True)
    payment_options = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")
    TxID = models.CharField(max_length=100, null=True, blank=True)
    paymentMobile = models.CharField(max_length=20, null=True, blank=True)
    prescriptions = models.JSONField(null=True, blank=True)
    Delivery_status = models.CharField(max_length=20, default="Pending")
    timestamp = models.DateTimeField(default=timezone.now)
    for_stock= models.TextField(default="null")

    def __str__(self):
        return f"Temporary Order by {self.phonenumber}"