from django.db import models

# Create your models here.

class Product(models.Model):
    p_name = models.CharField(max_length=255)
    p_category = models.CharField(max_length=255)
    p_image= models.ImageField(upload_to='media/',default='static\cat-icons\syringe.png')  # 'images/' is the upload directory
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    p_discount = models.DecimalField(max_digits=5, decimal_places=2)
    p_id = models.AutoField(primary_key=True)
    p_type = models.CharField(max_length=255, blank=True)
    p_Dosage = models.TextField(blank=True)
    p_Dosage_Strength = models.CharField(max_length=255, blank=True)
    size=models.CharField(max_length=255, blank=True)
    p_link = models.CharField(max_length=765, blank=True)
    def __str__(self):
      return self.p_name