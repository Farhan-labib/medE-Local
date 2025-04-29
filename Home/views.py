from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
import ast
import json
import os

from .models import Product
from products.models import Orders, Profile_MedList, presciption_order, main_product
from authentication.models import UserProfile
from custom_admin.models import Location, TemporaryOrders


def home(request):
    products = Product.objects.filter(Stock__gt=0, inventory__gt=0)
    for product in products:
        product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))
    return render(request, 'index.html', {'products': products})


def profile(request):
    phonenumber = request.user.phone_number
    
    # Get data from tables using a single database hit each
    orders = Orders.objects.filter(phonenumber=phonenumber)
    temp_orders = TemporaryOrders.objects.filter(phonenumber=phonenumber)
    p_order = presciption_order.objects.filter(phonenumber=phonenumber)
    
    # Process Orders data
    orders_data = {}
    for i in orders:
        d = []
        data = ast.literal_eval(i.ordered_products)
        for item in data:
            try:
                if len(item) == 3:
                    name, number, _ = item
                    d.append(f"{name}X{number}")
                else:
                    name, number, unit, price = item
                    d.append(f"{name}X{number} ({unit} - {price})")
            except ValueError:
                continue

        orders_data[i.id] = [d, i.total, i.timestamp, i.status]
    
    # Process TemporaryOrders data
    temp_orders_data = {}
    for i in temp_orders:
        d = []
        data = ast.literal_eval(i.ordered_products)
        for item in data:
            name, number, _ = item
            d.append(f"{name}X{number}")
        
        temp_orders_data[i.id] = [d, i.total, i.timestamp, i.status, True]
    
    # Fetch MedList data
    saved_data = Profile_MedList.objects.filter(phone_number=phonenumber).values()
    data_list = list(saved_data)
    
    return render(request, 'user-profile.html', {
        'orders': orders_data,
        'temp_orders': temp_orders_data,
        'medList': data_list, 
        'p_order': p_order,
        'user_phone_number': phonenumber
    })


def quick_order(request):
    phonenumber = request.user.phone_number
    user_address = request.user.address
    
    # Get saved medication list
    saved_data = Profile_MedList.objects.filter(phone_number=phonenumber).values()
    data_list = list(saved_data)
    med_list = data_list[0]['med_list']
    
    # Get all p_ids at once for batch query
    p_ids = list(med_list.keys())
    products_data_dict = {str(item['p_id']): item for item in main_product.objects.filter(p_id__in=[int(pid) for pid in p_ids]).values('p_id', 'p_name', 'medPerStrip', 'p_price', 'p_discount')}
    
    # Calculate order details
    t = []
    total = 0
    for key, value in med_list.items():
        morning_day_len = len(med_list[key][0])
        dayy = med_list[key][1]
        
        product = products_data_dict[key]
        medPerStrip = product['medPerStrip']
        price = (product['p_price'] - (product['p_price'] * (product['p_discount'] / 100)))
        quantity = (product['medPerStrip'] * morning_day_len * dayy) / medPerStrip
        t.append((product['p_name'], str(int(quantity)), "Piece", '{:.2f}'.format(float(price * quantity))))
        total += round(price * quantity, 2)

    prescription_required = request.session.get('prescription_required', False)
    for_stock = request.session.get('for_stock', {})
    
    # Process locations - fetch data once and iterate over it
    locations = Location.objects.all()
    
    # Initialize data structures
    division_data = {}
    zilla_data = {}
    upazila_data = {}
    union_data = {}

    # Process locations in a single loop
    for location in locations:
        if location.level == 'division':
            division_data[location.name] = location.name
        elif location.level == 'zilla' and location.parent:
            parent_division = location.parent.name
            if parent_division not in zilla_data:
                zilla_data[parent_division] = []
            zilla_data[parent_division].append(location.name)
        elif location.level == 'upazila' and location.parent:
            parent_zilla = location.parent.name
            if parent_zilla not in upazila_data:
                upazila_data[parent_zilla] = []
            upazila_data[parent_zilla].append(location.name)
        elif location.level == 'union' and location.parent:
            parent_upazila = location.parent.name
            if parent_upazila not in union_data:
                union_data[parent_upazila] = []
            union_data[parent_upazila].append({
                'name': location.name,
                'id': location.id,
                'delivery_fee': float(location.delivery_fee) if location.delivery_fee else 60.0
            })

    context = {
        'product_data_list': t,
        'total': total, 
        'user_address': user_address,
        'prescription_required': prescription_required,
        'division_data': json.dumps(list(division_data.keys())),
        'zilla_data': json.dumps(zilla_data),
        'upazila_data': json.dumps(upazila_data),
        'union_data': json.dumps(union_data, cls=DjangoJSONEncoder),
        'for_stock': for_stock
    }
    
    return render(request, 'order_confirm.html', context)


def upload_prescription(request):
    if request.method == 'POST':
        prescription_image = request.FILES.get('prescription_image')
        selected_days = request.POST.getlist('selected_days')
        phone_number = request.user.phone_number
        
        # Create directory only if needed
        user_prescription_folder = os.path.join('media', 'prescription', str(phone_number))
        os.makedirs(user_prescription_folder, exist_ok=True)

        # Save the prescription image
        fs = FileSystemStorage(location=user_prescription_folder)
        saved_image = fs.save(prescription_image.name, prescription_image)
        image = f"prescription/{phone_number}/{saved_image}"

        # Update or create the prescription record
        user_medlist, created = Profile_MedList.objects.get_or_create(
            phone_number=phone_number,
            defaults={'prescriptions': [(image, selected_days[0])]}
        )
        
        if not created:
            prescriptions = user_medlist.prescriptions or []
            prescriptions.append((image, selected_days[0]))
            user_medlist.prescriptions = prescriptions
            user_medlist.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def searchresult(request):
    if request.method == 'POST':
        search_results_json = request.POST.get('search_results')
        
        if not search_results_json:
            return HttpResponse('Invalid request', status=400)
            
        search_results = json.loads(search_results_json)
        p_id_list = [item['p_id'] for item in search_results]
        
        # Retrieve all products in a single query
        products_queryset = main_product.objects.filter(p_id__in=p_id_list)
        p_details = []
        
        for id in p_id_list:
            product_list = []
            for product in products_queryset:
                if product.p_id == id:
                    product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))
                    product_list.append(product)
            
            if product_list:
                p_details.append(product_list)
        
        context = {'product_details': p_details}
        html_content = render(request, 'search-results.html', context).content.decode('utf-8')
        return HttpResponse(html_content)
    
    return HttpResponse('Invalid request', status=400)