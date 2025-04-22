from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

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
