from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
import ast
import json
import os
from products.models import Orders, Profile_MedList, presciption_order, main_product
from authentication.models import UserProfile
from custom_admin.models import Location, TemporaryOrders


def home(request):
    return render(request, 'index.html')


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

    # Fetch user's saved med list
    saved_data = Profile_MedList.objects.filter(phone_number=phonenumber).values()
    data_list = list(saved_data)
    med_list = data_list[0]['med_list']

    # Query all product details needed
    p_ids = list(med_list.keys())
    products_data_dict = {
        str(item['p_id']): {
            'p_id': item['p_id'],
            'p_name': item['p_name'],
            'medPerStrip': int(item['medPerStrip']),
            'stripPerBox': int(item['stripPerBox']),
            'p_price': float(item['p_price']),
            'p_discount': float(item['p_discount']),
            'p_image': str(item['p_image']),
        }
        for item in main_product.objects.filter(p_id__in=[int(pid) for pid in p_ids])
        .values('p_id', 'p_name', 'medPerStrip', 'stripPerBox', 'p_price', 'p_discount', 'p_image')
    }

    t = []
    total = 0
    for_stock = {}

    for key, value in med_list.items():
        morning_day_len = len(value[0])
        dayy = value[1]

        product = products_data_dict[key]
        quantity = morning_day_len * dayy  # total pieces

        unit_price = product['p_price'] * (1 - product['p_discount'] / 100)
        subtotal = unit_price * quantity

        t.append((
            product['p_name'],
            str(quantity),
            "Piece",
            '{:.2f}'.format(subtotal)
        ))
        total += round(subtotal, 2)

        for_stock[str(product['p_id'])] = {
            'packaging': 'Piece',
            'quantity': quantity,
            'price': '{:.4f}'.format(unit_price),
            'medPerStrip': product['medPerStrip'],
            'stripPerBox': product['stripPerBox'],
            'name': product['p_name'],
            'image': product['p_image']
        }

    # Location processing
    locations = Location.objects.all()
    division_data, zilla_data, upazila_data, union_data = {}, {}, {}, {}

    for location in locations:
        if location.level == 'division':
            division_data[location.name] = location.name
        elif location.level == 'zilla' and location.parent:
            zilla_data.setdefault(location.parent.name, []).append(location.name)
        elif location.level == 'upazila' and location.parent:
            upazila_data.setdefault(location.parent.name, []).append(location.name)
        elif location.level == 'union' and location.parent:
            union_data.setdefault(location.parent.name, []).append({
                'name': location.name,
                'id': location.id,
                'delivery_fee': float(location.delivery_fee) if location.delivery_fee else 60.0
            })

    context = {
        'product_data_list': t,
        'total': total,
        'user_address': user_address,
        'prescription_required': False,
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