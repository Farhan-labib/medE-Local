from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from Home.models import Product

class main_product(models.Model):
    CATEGORY_CHOICES = (
        ('BABY CARE', 'BABY CARE'),
        ('MENS','MENS')
    )
    feature_CHOICES = (('yes', 'yes'), ('no', 'no'))

    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=255)
    p_type = models.CharField(max_length=255)
    p_generics = models.CharField(max_length=255)
    p_company = models.CharField(max_length=255)
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    p_discount = models.DecimalField(max_digits=5, decimal_places=2)
    p_Indications = models.TextField()
    p_Pharmacology = models.TextField()
    p_Dosage = models.TextField()
    p_Interaction = models.TextField()
    p_Contradictions = models.TextField()
    p_Side_Effects = models.TextField()
    p_Pregnancy = models.TextField()
    p_Precautions = models.TextField()
    p_Therapeutic = models.TextField()
    p_Storage = models.CharField(max_length=255)
    p_category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    feature = models.CharField(max_length=255, choices=feature_CHOICES)

    def __str__(self):
        return self.p_name

    def save(self, *args, **kwargs):
        super(main_product, self).save(*args, **kwargs)

        # Check if the feature is 'yes' and create a corresponding Product entry
        if self.feature == 'yes':
            Product.objects.create(
                p_name=self.p_name,
                p_category=self.p_category,
                p_price=self.p_price,
                p_discount=self.p_discount,
                p_id=self.p_id
            )

@receiver(pre_save, sender=main_product)
def delete_product_if_feature_changed(sender, instance, **kwargs):
    # Check if the 'feature' field is transitioning from 'yes' to 'no'
    if instance.pk and instance.feature == 'no':
        try:
            product_to_delete = Product.objects.get(p_id=instance.p_id)
            product_to_delete.delete()
        except Product.DoesNotExist:
            pass  # Handle the case where the Product does not exist

# Register the signal
pre_save.connect(delete_product_if_feature_changed, sender=main_product)
