from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from Home.models import Product
from django.utils import timezone
class main_product(models.Model):
    CATEGORY_CHOICES = (
    ('General Health', 'General Health'),
    ('Cold & Allergies Remedies', 'Cold & Allergies Remedies'),
    ('Heart Health', 'Heart Health'),
    ('Diabetes Care', 'Diabetes Care'),
    ('Lungs & Respiratory Health', 'Lungs & Respiratory Health'),
    ('Brain & Neurological Health', 'Brain & Neurological Health'),
    ('Muscles & Bone Health', 'Muscles & Bone Health'),
    ('Digestive Health', 'Digestive Health'),
    ('Medical Devices', 'Medical Devices'),
    ('Sexual Health', 'Sexual Health'),
    ('Women Health', 'Women Health'),
    ('Infant care', 'Infant care'),
    ('Supplements & Nutrition', 'Supplements & Nutrition'),
    ('Personal Health', 'Personal Health'),
    ('Blood and Circulatory Health', 'Blood and Circulatory Health'),
    ('Mental Health', 'Mental Health'),
    ('Kidney and Renal Health', 'Kidney and Renal Health'),
    ('Infection Management', 'Infection Management'),
    ('Immune System Health', 'Immune System Health'),
    ('Liver Health', 'Liver Health'),
    ('Thyroids and Hormones', 'Thyroids and Hormones'),
    ('Physical Injury', 'Physical Injury'),
    ('Pain Relief', 'Pain Relief'),
    )

    BUNDLING_CHOICES = (
        ('Box', 'Box'),
        ('Pack', 'Pack'),
        ('Piece', 'Piece'),
    )

    feature_CHOICES = (('yes', 'yes'), ('no', 'no'))
    OTC_CHOICES = (('yes', 'Yes'),('no', 'No'))
    add_list= (('yes', 'Yes'),('no', 'No'))
    m_or_g= (('Medicines', 'Medicines'),('Generals', 'Generals'))
    p_id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=255, blank=True)
    otc_status = models.CharField(max_length=3, choices=OTC_CHOICES, default='yes')
    p_name = models.CharField(max_length=255)
    Brand = models.CharField(max_length=255, blank=True)
    Manufacturer = models.CharField(max_length=255, blank=True)
    p_generics = models.CharField(max_length=255,blank=True)
    p_type = models.CharField(max_length=255, blank=True)
    p_image=models.ImageField(upload_to='media/',default='static\cat-icons\syringe.png')  # 'images/' is the upload directory
    p_Dosage_Strength=models.CharField(max_length=255, blank=True)
    Variant=models.CharField(max_length=255, blank=True)
    p_category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    p_Administration = models.TextField(blank=True)
    Features_Specifications = models.TextField(blank=True)
    bundling = models.CharField(max_length=1024, blank=True, null=True) 
    medPerStrip = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    stripPerBox = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    p_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    p_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    p_Indications = models.TextField(blank=True)
    p_Pharmacology = models.TextField(blank=True)
    p_Dosage = models.TextField(blank=True)
    p_Interaction = models.TextField(blank=True)
    p_Contradictions = models.TextField(blank=True)
    p_Side_Effects = models.TextField(blank=True)
    p_Pregnancy = models.TextField(blank=True)
    p_Precautions = models.TextField(blank=True)
    p_Therapeutic = models.TextField(blank=True)
    p_Storage = models.CharField(max_length=255,blank=True)
    feature = models.CharField(max_length=255, choices=feature_CHOICES)
    add_to_list = models.CharField(max_length=255, choices=add_list, default='yes')
    description=models.TextField(blank=True)
    size=models.CharField(max_length=255, blank=True)
    p_link = models.CharField(max_length=765, blank=True)
    m_or_g = models.CharField(max_length=255, choices=m_or_g, default='Medicines')
    FAQ=models.TextField(blank=True)
    Suggestions=models.TextField(blank=True)
    inventory=models.IntegerField(default=0)
    SKU=models.CharField(max_length=255, blank=True)
    Batch=models.CharField(max_length=255, blank=True)
    MFG_Date=models.DateField(blank=True, null=True)
    EXP_Date=models.DateField(blank=True, null=True)
    Stock=models.IntegerField(default=0)
    Purchase_Price=models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.p_name

    def save(self, *args, **kwargs):
        # Check if the main_product instance is being updated
        self.p_link = f"{self.p_name.replace(' ', '-')}-{self.p_type.replace(' ', '-')}-{self.size.replace(' ', '-')}"
        if self.pk:
            # Check if the associated Product instance exists
            try:
                product_instance = Product.objects.get(p_id=self.p_id)
                # Update the existing Product instance
                product_instance.p_name = self.p_name
                product_instance.p_category = self.p_category
                product_instance.p_price = self.p_price
                product_instance.p_discount = self.p_discount
                product_instance.p_image = self.p_image
                product_instance.p_type = self.p_type
                product_instance.p_Dosage = self.p_Dosage
                product_instance.p_Dosage_Strength = self.p_Dosage_Strength
                product_instance.size = self.size
                product_instance.p_link = self.p_link
                product_instance.inventory = self.inventory
                product_instance.Stock = self.Stock
                
                product_instance.save()
            except Product.DoesNotExist:
                pass  # Handle the case where the Product does not exist

        super(main_product, self).save(*args, **kwargs)

        # Check if the feature is 'yes' and create a corresponding Product entry
        if self.feature == 'yes':
            Product.objects.get_or_create(
                p_name=self.p_name,
                p_category=self.p_category,
                p_price=self.p_price,
                p_discount=self.p_discount,
                p_id=self.p_id,
                p_image=self.p_image,
                p_Dosage=self.p_Dosage,
                p_type=self.p_type,
                p_Dosage_Strength=self.p_Dosage_Strength,
                size=self.size,
                p_link=self.p_link,
                inventory=self.inventory,
                Stock=self.Stock)

    def delete(self, *args, **kwargs):
        # Delete the associated Product when deleting main_product
        if self.feature == 'yes':
            try:
                product_to_delete = Product.objects.get(p_id=self.p_id)
                product_to_delete.delete()
            except Product.DoesNotExist:
                pass  # Handle the case where the Product does not exist

        super(main_product, self).delete(*args, **kwargs)

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


class Orders(models.Model):
    Pending = 'Pending'
    Confirmed = 'Confirmed'
    Shipping = 'Shipping'
    Completed = 'Completed'
    Failed = 'Failed'
    delivery_stat = [
        (Pending, 'Pending'),
        (Confirmed, 'Confirmed'),
        (Shipping , 'Shipping'),
        (Completed , 'Completed'),
        (Failed , 'Failed'),
    ]
    Approved = 'Approved'
    Rejected = 'Rejected'
    pending = 'pending'
    status = [
        (Pending, 'Pending'),
        (Confirmed, 'Confirmed'),
        (Shipping , 'Shipping'),
        (Completed , 'Completed'),
        (Failed , 'Failed'),
    ]
    phonenumber = models.CharField(max_length=15)
    ordered_products = models.TextField(default="null")
    prescriptions = models.JSONField(default="null",blank=True)
    total = models.TextField(default="null")
    del_adress = models.TextField(default="null")
    timestamp = models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=20, choices=status, default='Pending', blank=True)
    Delivery_status=models.CharField(max_length=20, choices=delivery_stat, default='Pending', blank=True)
    paymentMobile = models.CharField(max_length=15, blank=True, null=True)
    TxID = models.CharField(max_length=50, blank=True, null=True)
    payment_options=models.CharField(max_length=20, default='cod', blank=True)
    for_stock= models.TextField(default="null")


class Profile_MedList(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=15, unique=True)
    med_list = models.JSONField(default=dict)  # Set default value as an empty dictionary
    prescriptions = models.JSONField(default=list)

    def __str__(self):
        return self.phone_number
    

class presciption_order(models.Model):
   
    Pending = 'Pending'
    Created = 'Created'
    Rejected = 'Rejected'
    order_stat = [
        (Pending, 'Pending'),
        (Created, 'Created'),
        (Rejected , 'Rejected'),
    ]

    phonenumber = models.CharField(max_length=15)
    prescription_img = models.TextField(default="null")
    days = models.TextField(default="null")
    del_adress = models.TextField(default="null")
    timestamp = models.DateTimeField(default=timezone.now)
    Order_status=models.CharField(max_length=20, choices=order_stat, default='Pending', blank=True)
    paymentMobile = models.CharField(max_length=15, blank=True, null=True)
    TxID = models.CharField(max_length=50, blank=True, null=True)
    payment_options=models.CharField(max_length=20, default='cod', blank=True)
