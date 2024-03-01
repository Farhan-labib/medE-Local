from django.contrib import admin

# Register your models here.
from .models import product
from authentication.models import UserProfile 

admin.site.register(UserProfile)
admin.site.register(product)
