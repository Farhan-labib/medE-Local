from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import os
import ast

from .models import main_product, Profile_MedList, presciption_order, Orders
from authentication.models import UserProfile
from custom_admin.models import Location, TemporaryOrders


def prod(request, p_link):
    product_details = {'p_link': p_link}

    try:
        product = main_product.objects.get(p_link=product_details['p_link'])
        product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))
    except main_product.DoesNotExist:
        product = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(pk=request.user.id)
            if user_profile.user_type == 'quantity':
                return render(request, 'product.html', {'product_details': product})
        except UserProfile.DoesNotExist:
            pass
    
    return render(request, 'product_day.html', {'product_details': product})


from django.db.models import Q

def category(request, p_category):
    all_products = main_product.objects.filter(
        p_category=p_category,
        Stock__gt=0,
        inventory__gt=0
    )

    grouped_products = {}
    
    for product in all_products:
        parent = product.parent_code.strip()

        if parent not in grouped_products:
            grouped_products[parent] = []

        grouped_products[parent].append(product)

    final_products = []

    for parent_code, product_group in grouped_products.items():
        lowest_stock_product = min(product_group, key=lambda x: x.Stock)
        lowest_stock_product.discounted_price = lowest_stock_product.p_price - (
            lowest_stock_product.p_price * (lowest_stock_product.p_discount / 100)
        )
        final_products.append(lowest_stock_product)

    final_products.sort(key=lambda x: x.count, reverse=True)

    context = {
        'product_details': final_products,
        'category': p_category,
    }

    return render(request, 'category-wise.html', context)

def all_product(request):
    all_products = main_product.objects.filter(
        Stock__gt=0,
        inventory__gt=0,
        m_or_g='Generals'
    )

    grouped_products = {}

    for product in all_products:
        parent = product.parent_code.strip()

        if parent not in grouped_products:
            grouped_products[parent] = []

        grouped_products[parent].append(product)

    final_products = []

    for parent_code, product_group in grouped_products.items():
        lowest_stock_product = min(product_group, key=lambda x: x.Stock)
        lowest_stock_product.discounted_price = lowest_stock_product.p_price - (
            lowest_stock_product.p_price * (lowest_stock_product.p_discount / 100)
        )
        final_products.append(lowest_stock_product)

    final_products.sort(key=lambda x: x.count, reverse=True)

    context = {
        'product_details': final_products,
    }

    return render(request, 'all_product.html', context)


def all_medicine(request):
    all_products = main_product.objects.filter(
        Stock__gt=0,
        inventory__gt=0,
        m_or_g='Medicines'
    )

    grouped_products = {}

    for product in all_products:
        parent = product.parent_code.strip()

        if parent not in grouped_products:
            grouped_products[parent] = []

        grouped_products[parent].append(product)

    final_products = []

    for parent_code, product_group in grouped_products.items():
        lowest_stock_product = min(product_group, key=lambda x: x.Stock)
        lowest_stock_product.discounted_price = lowest_stock_product.p_price - (
            lowest_stock_product.p_price * (lowest_stock_product.p_discount / 100)
        )
        final_products.append(lowest_stock_product)

    final_products.sort(key=lambda x: x.count, reverse=True)

    context = {
        'product_details': final_products,
    }

    return render(request, 'all_medicine.html', context)



def live_search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        results = main_product.objects.filter(p_name__icontains=query).values(
            'p_name', 'p_type', 'size', 'p_id', 'p_link'
        )
        return JsonResponse(list(results), safe=False)


def get_product_info(request, p_id):
    try:
        product = main_product.objects.get(p_id=p_id)
        discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))
        
        product_data = {
            'p_id': p_id,
            'p_name': product.p_name,
            'p_category': product.p_category,
            'otc_status': product.otc_status,
            'p_price': str(product.p_price),
            'p_discount': str(product.p_discount),
            'discounted_price': discounted_price,
            'medPerStrip': product.medPerStrip,
            'stripPerBox': product.stripPerBox,
            'p_image': str(product.p_image),
            'add_to_list': product.add_to_list,
        }
        return JsonResponse(product_data)
    
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def checkout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        output = {}
        total = 0
        prescription_required = False
        product_index = 1
        
        # Fetch all products in one query
        product_ids = list(data.keys())
        products = {str(p.p_id): p for p in main_product.objects.filter(p_id__in=product_ids)}
        
        for key, value in data.items():
            if key not in products:
                return JsonResponse({'error': f'Product with ID {key} not found'}, status=404)
                
            product = products[key]
            unique_key = f"{product_index}. {product.p_name}"
            product_index += 1
            
            if product.otc_status == "no":
                prescription_required = True
                
            product_price_after_discount = round(product.p_price - (product.p_price * (product.p_discount / 100)), 2)
            
            if value['packaging'] == 'Pack':
                product_total = round(value['quantity'] * product_price_after_discount * product.medPerStrip, 2)
            elif value['packaging'] == 'Box':
                product_total = round(value['quantity'] * product_price_after_discount * product.medPerStrip * product.stripPerBox, 2)
            else:
                product_total = round(value['quantity'] * product_price_after_discount, 2)
                
            total += product_total
            output[unique_key] = f"{str(value)};{format(product_total, '.2f')}"
            
        request.session['prescription_required'] = prescription_required
        request.session['checkout_output'] = output
        request.session['checkout_total'] = format(total, '.2f')
        request.session['for_stock'] = data
        
        return JsonResponse({'message': 'Checkout successful'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


def order_confirm(request):
    output = request.session.get('checkout_output', {})
    total = request.session.get('checkout_total', 0)
    prescription_required = request.session.get('prescription_required', False)
    for_stock = request.session.get('for_stock', {})
    
    # Process product data
    product_data_list = []
    for product_name, product_data in output.items():
        parts = product_data.split(';')
        if len(parts) >= 2:
            try:
                info_dict = ast.literal_eval(parts[0])
                quantity = info_dict.get('quantity', 0)
                packaging = info_dict.get('packaging', '')
                price = parts[1]
                product_data_list.append((product_name, quantity, packaging, price))
            except Exception:
                continue
                
    # Fetch all location data in a single query
    locations = Location.objects.all()
    
    # Initialize data structures
    division_data = {}
    zilla_data = {}
    upazila_data = {}
    union_data = {}
    
    # Process locations more efficiently with a single loop
    for location in locations:
        if location.level == 'division':
            division_data[location.name] = location.name
        elif location.level == 'zilla' and location.parent:
            parent = location.parent.name
            if parent not in zilla_data:
                zilla_data[parent] = []
            zilla_data[parent].append(location.name)
        elif location.level == 'upazila' and location.parent:
            parent = location.parent.name
            if parent not in upazila_data:
                upazila_data[parent] = []
            upazila_data[parent].append(location.name)
        elif location.level == 'union' and location.parent:
            parent = location.parent.name
            if parent not in union_data:
                union_data[parent] = []
            union_data[parent].append({
                'name': location.name,
                'id': location.id,
                'delivery_fee': float(location.delivery_fee) if location.delivery_fee else 60.0
            })
    
    context = {
        'product_data_list': product_data_list,
        'prescription_required': prescription_required,
        'total': total,
        'division_data': json.dumps(list(division_data.keys())),
        'zilla_data': json.dumps(zilla_data),
        'upazila_data': json.dumps(upazila_data),
        'union_data': json.dumps(union_data, cls=DjangoJSONEncoder),
        'for_stock': for_stock,
    }
    
    return render(request, 'order_confirm.html', context)


def order_complete(request):
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber')
        ordered_products = request.POST.get('ordered_products')
        prescription_file = request.FILES.get('prescription')
        base_total = float(request.POST.get('total', 0))

        # Compile delivery address
        division = request.POST.get('division')
        zilla = request.POST.get('zilla')
        upazila = request.POST.get('upazila')
        union = request.POST.get('union')
        address = request.POST.get('address')
        del_address = f"{division}, {zilla}, {upazila}, {union}, {address}"

        payment_mobile = request.POST.get('paymentMobile')
        tx_id = request.POST.get('TxID')
        payment_options = request.POST.get('payment-options')
        for_stock = request.POST.get('for_stock')

        # Get delivery fee based on union
        delivery_fee = 60 
        try:
            union_obj = Location.objects.get(name=union, level='union')
            if union_obj.delivery_fee:
                delivery_fee = float(union_obj.delivery_fee)
        except Location.DoesNotExist:
            pass

        grand_total = base_total + delivery_fee

        # Handle prescription file upload
        image = []
        if prescription_file:
            user_prescription_folder = os.path.join('media', 'otc_prescription', str(phonenumber))
            os.makedirs(user_prescription_folder, exist_ok=True)
            fs = FileSystemStorage(location=user_prescription_folder)
            saved_image = fs.save(prescription_file.name, prescription_file)
            image = [f"otc_prescription/{phonenumber}/{saved_image}"]

        # Create and save order
        Orders.objects.create(
            phonenumber=phonenumber,
            ordered_products=ordered_products,
            prescriptions=image,
            total=grand_total,
            del_adress=del_address,
            status='Pending',
            paymentMobile=payment_mobile,
            TxID=tx_id,
            payment_options=payment_options,
            for_stock=for_stock
        )
        return render(request, 'confirm.html')


def save_med_list(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_phone_number = data.get('user')
        p_id = data.get('p_id')
        intakes = data.get('intakes')
        num_Days = data.get('numDays')

        # Retrieve or create user and update med_list in one operation
        user, _ = Profile_MedList.objects.get_or_create(phone_number=user_phone_number)
        
        med_list = user.med_list or {}
        med_list[p_id] = [intakes, num_Days]
        user.med_list = med_list
        user.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def remove_productList(request, product_id):
    try:
        user_phone_number = request.user.phone_number
        user = Profile_MedList.objects.get(phone_number=user_phone_number)
        med_list = user.med_list
        
        if str(product_id) in med_list:
            del med_list[str(product_id)]
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Product ID not found in med_list'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def pres_confirm(request):
    phonenumber = request.user.phone_number
    saved_data = Profile_MedList.objects.filter(phone_number=phonenumber).values()
    
    # Fetch and process location data
    locations = Location.objects.all()
    division_data = {}
    zilla_data = {}
    upazila_data = {}
    union_data = {}
    
    # Process locations in a single pass
    for location in locations:
        if location.level == 'division':
            division_data[location.name] = location.name
        elif location.level == 'zilla' and location.parent:
            parent = location.parent.name
            if parent not in zilla_data:
                zilla_data[parent] = []
            zilla_data[parent].append(location.name)
        elif location.level == 'upazila' and location.parent:
            parent = location.parent.name
            if parent not in upazila_data:
                upazila_data[parent] = []
            upazila_data[parent].append(location.name)
        elif location.level == 'union' and location.parent:
            parent = location.parent.name
            if parent not in union_data:
                union_data[parent] = []
            union_data[parent].append(location.name)

    context = {
        'division_data': json.dumps(list(division_data.keys())),
        'zilla_data': json.dumps(zilla_data),
        'upazila_data': json.dumps(upazila_data), 
        'union_data': json.dumps(union_data),
        'data_list': list(saved_data)
    }

    return render(request, 'pres_confirm.html', context)


def presciptions_order(request):
    if request.method == 'POST':
        phone_number = request.user.phone_number
        prescription_img = request.POST.get('prescription_img')
        days = request.POST.get('days2')
        
        # Compile delivery address
        division = request.POST.get('division')
        zilla = request.POST.get('zilla')
        upazila = request.POST.get('upazila')
        union = request.POST.get('union')
        address = request.POST.get('address')
        delivery_address = f"{division}, {zilla}, {upazila}, {union}, {address}"
        
        payment_mobile = request.POST.get('paymentMobile')
        tx_id = request.POST.get('TxID')
        payment_options = request.POST.get('payment-options')
        
        # Create prescription order
        presciption_order.objects.create(
            phonenumber=phone_number,
            prescription_img=prescription_img,
            days=days,
            del_adress=delivery_address,
            timestamp=timezone.now(),
            paymentMobile=payment_mobile,
            TxID=tx_id,
            payment_options=payment_options
        )
        
    return render(request, 'confirm.html')


def update_medlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            med_list_data = data.get('medListData', {})
            user_phone_number = request.user.phone_number
            
            # Update the Profile_MedList in a single operation
            Profile_MedList.objects.filter(phone_number=user_phone_number).update(med_list=med_list_data)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required(login_url='/login/')
def view_temp_order(request, order_id):
    temp_order = get_object_or_404(TemporaryOrders, id=order_id)
    
    # Check authorization
    if request.user.phone_number != temp_order.phonenumber:
        return HttpResponseForbidden("You are not authorized to view this order.")
    
    # Process ordered products
    ordered_products = []
    if temp_order.ordered_products:
        products_list = ast.literal_eval(temp_order.ordered_products)
        for product in products_list:
            name, quantity, price = product
            subtotal = float(price)
            ordered_products.append({
                'name': name,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
    
    # Calculate subtotals
    products_subtotal = sum(item['subtotal'] for item in ordered_products)
    delivery_fee = float(temp_order.total) - products_subtotal

    context = {
        'order': temp_order,
        'ordered_products': ordered_products,
        'products_subtotal': products_subtotal,
        'delivery_fee': delivery_fee,
    }
    
    return render(request, 'temp_order_invoice.html', context)


def user_confirm(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        temporary_order = get_object_or_404(TemporaryOrders, id=order_id)

        # Transfer temporary order to confirmed order
        Orders.objects.create(
            ordered_products=temporary_order.ordered_products,
            prescriptions=temporary_order.prescriptions,
            timestamp=temporary_order.timestamp,
            phonenumber=temporary_order.phonenumber,
            del_adress=temporary_order.del_adress,
            payment_options=temporary_order.payment_options,
            paymentMobile=temporary_order.paymentMobile,
            TxID=temporary_order.TxID,
            total=temporary_order.total,
            status='Pending',
            for_stock=temporary_order.for_stock
        )

        # Delete the temporary order
        temporary_order.delete()

    return redirect('profile')
