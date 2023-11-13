from django.contrib import admin

# Register your models here.
from .models import main_product
from .models import Orders
from .models import presciption_order
from django.conf import settings
from django.utils.html import format_html
admin.site.register(main_product)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('phonenumber', 'status', 'timestamp')  # Add any other fields you want to display
    list_filter = ('status',)  # Filter by the 'status' field

    def get_list_filter(self, request):
        if request.GET.get('status') == 'confirm':
            return ('status',)
        return super().get_list_filter(request)

admin.site.register(Orders, OrdersAdmin)

class PrescriptionOrderAdmin(admin.ModelAdmin):
    list_display = ('phonenumber', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('phonenumber',)

    def photo_display(self, obj):
        if obj.prescription_img:
            return format_html('<img src="{}{}" height="500" />', settings.MEDIA_URL, obj.prescription_img)
        else:
            return "-"

    photo_display.allow_tags = True
    photo_display.short_description = 'Prescription Photo'

    readonly_fields = ('photo_display',)

admin.site.register(presciption_order, PrescriptionOrderAdmin)
