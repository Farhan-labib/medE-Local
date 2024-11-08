from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import localtime
from .models import Orders, main_product, presciption_order
from django.conf import settings
from django.urls import reverse

# Registering the main_product model
class MainProductAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'p_name') 

admin.site.register(main_product, MainProductAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'phonenumber_link', 'status', 'formatted_datetime', 'Delivery_status', 'payment_options')
    list_filter = ('status', 'Delivery_status', 'payment_options')
    search_fields = ('phonenumber',)

    def formatted_datetime(self, obj):
        # Convert timestamp to local time (Bangladesh time)
        local_time = localtime(obj.timestamp)
        # Format the date and time manually to use a period instead of a colon
        formatted_datetime = local_time.strftime('%Y-%m-%d %I.%M %p')
        return formatted_datetime
    formatted_datetime.short_description = 'Date and Time'

    def phonenumber_link(self, obj):
        # Create a clickable link for the phone number
        url = reverse('admin:products_orders_change', args=[obj.id])  # Adjust the URL pattern name as necessary
        return format_html('<a href="{}">{}</a>', url, obj.phonenumber)
    phonenumber_link.short_description = 'Phone Number'
    phonenumber_link.admin_order_field = 'phonenumber'

    def photos_display(self, obj):
        if obj.prescriptions:
            return format_html('<img src="{}{}" height="500" />', settings.MEDIA_URL, obj.prescriptions[0])
        else:
            return "-"
    photos_display.allow_tags = True
    photos_display.short_description = 'Prescription Photo'
    readonly_fields = ('photos_display',)

    def get_list_filter(self, request):
        if request.GET.get('status') == 'confirm':
            return ('status',)
        return super().get_list_filter(request)

admin.site.register(Orders, OrdersAdmin)

class PrescriptionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'phonenumber', 'status', 'formatted_datetime', 'Delivery_status')
    list_filter = ('status', 'Delivery_status')
    search_fields = ('phonenumber',)

    def formatted_datetime(self, obj):
        # Convert timestamp to local time (Bangladesh time)
        local_time = localtime(obj.timestamp)
        # Format the date and time manually to use a period instead of a colon
        formatted_datetime = local_time.strftime('%Y-%m-%d %I.%M %p')
        return formatted_datetime
    formatted_datetime.short_description = 'Date and Time'

    def photo_display(self, obj):
        if obj.prescription_img:
            return format_html('<img src="{}{}" height="500" />', settings.MEDIA_URL, obj.prescription_img)
        else:
            return "-"
    photo_display.allow_tags = True
    photo_display.short_description = 'Prescription Photo'
    readonly_fields = ('photo_display',)

admin.site.register(presciption_order, PrescriptionOrderAdmin)
