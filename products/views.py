from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .models import main_product, Profile_MedList, presciption_order
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import UserProfile
import json
import os
from django.conf import settings
from .models import Orders
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from custom_admin.models import Location, TemporaryOrders
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
import ast




def prod(request, p_link):
    
    product_details = {
        'p_link': p_link,
    }

    try:
        product = main_product.objects.get(p_link=product_details['p_link'])
        product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))  # FOR DISCOUNT
    except main_product.DoesNotExist:
        product = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(pk=request.user.id)
            if user_profile.user_type == 'quantity':
                return render(request, 'product.html', {'product_details': product})
        except UserProfile.DoesNotExist:
            pass  # Handle the case where the user profile does not exist
    
    # Default case if the user is not logged in or their type is not 'quantity'
    return render(request, 'product_day.html', {'product_details': product})








def category(request, p_category):
    products = main_product.objects.filter(p_category=p_category)

    # Calculate the discounted price for each product
    for product in products:
        product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))

    context = {
        'product_details': products,
        'category': p_category,
    }

    return render(request, 'category-wise.html', context)


def live_search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        results = main_product.objects.filter(p_name__icontains=query)

        # Convert the queryset to a list of dictionaries
        results_list = [
            {
                'p_name': product.p_name,
                'p_type': product.p_type,
                'size': product.size,
                'p_id':product.p_id,
                'p_link':product.p_link,
            }
            for product in results
        ]

        return JsonResponse(results_list, safe=False)
    


def get_product_info(request, p_id):
    try:
        # Use get() to retrieve a single product by p_id
        product = main_product.objects.get(p_id=p_id)

        # Create a dictionary with the product information
        product_data = {
            'p_id': p_id,
            'p_name': product.p_name,
            'p_category': product.p_category,
            'otc_status': product.otc_status,
            'p_price': str(product.p_price),
            'p_discount': str(product.p_discount),
            'discounted_price':product.p_price - (product.p_price * (product.p_discount / 100)),
            'medPerStrip':product.medPerStrip,
            'p_image':str(product.p_image),
            'add_to_list':product.add_to_list,
            # Add other fields as needed
        }
        return JsonResponse(product_data)
    
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)




def checkout_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            # Process the cart_data as needed (e.g., complete the checkout)
            output = {}
            total = 0
            prescription_required = False
            product_index = 1  # Initialize the product index
            for key, value in data.items():
                product = main_product.objects.get(p_id=key)

                # Create a numbered key in the format "1. ProductName"
                unique_key = f"{product_index}. {product.p_name}"
                product_index += 1  # Increment the index for each product

                # Check if a prescription is required
                if product.otc_status == "no":
                    prescription_required = True

                # Calculate the product price after discount and round to 2 decimal places
                product_price_after_discount = round(product.p_price - (product.p_price * (product.p_discount / 100)), 2)
                
                # Calculate the total for the product (quantity * price) and round to 2 decimal places
                product_total = round(value * product_price_after_discount, 2)

                # Update the overall total and round it
                total += product_total

                # Store product info in output with the numbered key
                output[unique_key] = f"{str(value)};{format(product_total, '.2f')}"

            

            # Add shipping cost (fixed at 60) if total is greater than 0
            

            # Save information to the session
            request.session['prescription_required'] = prescription_required
            request.session['checkout_output'] = output
            request.session['checkout_total'] = format(total, '.2f')
            request.session['for_stock']  = data

            # Return a successful response
            return JsonResponse({'message': 'Checkout successful'})

        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except main_product.DoesNotExist:
            # Handle product not found error
            return JsonResponse({'error': 'Product not found'}, status=404)

    # For other HTTP methods (e.g., GET), return a method not allowed response
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)


def order_confirm(request):
    output = request.session.get('checkout_output', {})
    total = request.session.get('checkout_total', 0)
    prescription_required = request.session.get('prescription_required', False)
    for_stock = request.session.get('for_stock', {})
    print(for_stock)
    
    # Split product data into tuples
    product_data_list = [
        (product_name, *product_data.split(';')) 
        for product_name, product_data in output.items()
    ]

    # Get locations from the database
    locations = Location.objects.all()

    # Initialize data structures
    division_data = {}  # Stores all divisions
    zilla_data = {}     # Key: division, Value: list of zillas
    upazila_data = {}   # Key: zilla, Value: list of upazilas
    union_data = {}     # Key: upazila, Value: list of unions

    # First pass: Populate divisions
    print(locations)
    for location in locations:
        if location.level == 'division':
            division_data[location.name] = location.name  # Store division name

    # Second pass: Populate zillas under divisions
    for location in locations:
        if location.level == 'zilla' and location.parent:
            parent_division = location.parent.name
            if parent_division not in zilla_data:
                zilla_data[parent_division] = []
            zilla_data[parent_division].append(location.name)

    # Third pass: Populate upazilas under zillas
    for location in locations:
        if location.level == 'upazila' and location.parent:
            parent_zilla = location.parent.name
            if parent_zilla not in upazila_data:
                upazila_data[parent_zilla] = []
            upazila_data[parent_zilla].append(location.name)

    # Fourth pass: Populate unions under upazilas
    for location in locations:
        if location.level == 'union' and location.parent:
            parent_upazila = location.parent.name
            if parent_upazila not in union_data:
                union_data[parent_upazila] = []
            union_data[parent_upazila].append(location.name)

    union_qs = Location.objects.filter(level='union')
    union_data = {}

    for union in union_qs:
        parent_upazila = union.parent.name if union.parent else ""
        if parent_upazila not in union_data:
            union_data[parent_upazila] = []
        union_data[parent_upazila].append({
            'name': union.name,
            'id': union.id,
            'delivery_fee': float(union.delivery_fee) if union.delivery_fee else 60.0
        })

    context = {
        'product_data_list': product_data_list,
        'prescription_required': prescription_required,
        'total': total,
        'division_data': json.dumps(list(division_data.keys())),  # Convert to list for JS
        'zilla_data': json.dumps(zilla_data),
        'upazila_data': json.dumps(upazila_data),
        'union_data': json.dumps(union_data),
        'for_stock': for_stock,
        'union_data': json.dumps(union_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'order_confirm.html', context)





def order_complete(request):
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber')
        ordered_products = request.POST.get('ordered_products')
        prescription_file = request.FILES.get('prescription')
        base_total = float(request.POST.get('total', 0))  # Total from product price only

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

      
        delivery_fee = 60 
        try:
            union_obj = Location.objects.get(name=union, level='union')
            if union_obj.delivery_fee:
                delivery_fee = float(union_obj.delivery_fee)
        except Location.DoesNotExist:
            pass  

        grand_total = base_total + delivery_fee

     
        image = []
        if prescription_file:
            user_prescription_folder = os.path.join('media', 'otc_prescription', str(phonenumber))
            if not os.path.exists(user_prescription_folder):
                os.makedirs(user_prescription_folder)
            fs = FileSystemStorage(location=user_prescription_folder)
            saved_image = fs.save(prescription_file.name, prescription_file)
            image = [f"otc_prescription/{phonenumber}/{saved_image}"]

     
        order = Orders(
            phonenumber=phonenumber,
            ordered_products=ordered_products,
            prescriptions=image,
            total=grand_total,
            del_adress=del_address,
            status='pending',
            paymentMobile=payment_mobile,
            TxID=tx_id,
            payment_options=payment_options,
            for_stock=for_stock
        )
        order.save()

        return render(request, 'confirm.html')


from django.http import JsonResponse

def save_med_list(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_phone_number = data.get('user')
        p_id = data.get('p_id')
        intakes = data.get('intakes')
        num_Days = data.get('numDays')

        # Retrieve or create the user object based on phone number
        user, created = Profile_MedList.objects.get_or_create(phone_number=user_phone_number)

        # Ensure the med_list field is initialized as a dictionary if it's null
        med_list = [intakes,num_Days]

        if user.med_list is None:
            user.med_list = {}
        # Update the med_list field
        user.med_list[p_id] = med_list
        user.save()

        # Return a success response
        return JsonResponse({'success': True})

    except Exception as e:
        # Return an error response if there is any exception
        return JsonResponse({'success': False, 'error': str(e)})

def remove_productList(request, product_id):
    try:
        user_phone_number = request.user.phone_number  # Implement a function to get the user's phone number
        user = Profile_MedList.objects.get(phone_number=user_phone_number)
        med_list = user.med_list
        # print('Current med_list:', med_list)  # Add this line to debug

        # Check if the productId exists in med_list before attempting to delete
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
    locations = Location.objects.all()

    # Initialize data structures
    division_data = {}  # Stores all divisions
    zilla_data = {}     # Key: division, Value: list of zillas
    upazila_data = {}   # Key: zilla, Value: list of upazilas
    union_data = {}     # Key: upazila, Value: list of unions

    # First pass: Populate divisions
    print(locations)
    for location in locations:
        if location.level == 'division':
            division_data[location.name] = location.name  # Store division name

    # Second pass: Populate zillas under divisions
    for location in locations:
        if location.level == 'zilla' and location.parent:
            parent_division = location.parent.name
            if parent_division not in zilla_data:
                zilla_data[parent_division] = []
            zilla_data[parent_division].append(location.name)

    # Third pass: Populate upazilas under zillas
    for location in locations:
        if location.level == 'upazila' and location.parent:
            parent_zilla = location.parent.name
            if parent_zilla not in upazila_data:
                upazila_data[parent_zilla] = []
            upazila_data[parent_zilla].append(location.name)

    # Fourth pass: Populate unions under upazilas
    for location in locations:
        if location.level == 'union' and location.parent:
            parent_upazila = location.parent.name
            if parent_upazila not in union_data:
                union_data[parent_upazila] = []
            union_data[parent_upazila].append(location.name)

    context={
        'division_data': json.dumps(list(division_data.keys())),  # Convert to list for JS
        'zilla_data': json.dumps(zilla_data),
        'upazila_data': json.dumps(upazila_data), 
        'union_data': json.dumps(union_data),
        'data_list' : list(saved_data)
    }

    # Convert the QuerySet to a list of dictionaries
    data_list = list(saved_data)
    return render(request,'pres_confirm.html',context )


def presciptions_order(request):
    if request.method == 'POST':
        # Get the necessary data from the form and logged in user
        phone_number = request.user.phone_number  # Replace with your actual user profile field
        prescription_img = request.POST.get('prescription_img')  # Make sure this is the correct form field name
        days = request.POST.get('days2')
        division = request.POST.get('division')
        zilla = request.POST.get('zilla')
        upazila = request.POST.get('upazila')
        union = request.POST.get('union')
        address=request.POST.get('address')
        delivery_address = division + ', ' + zilla + ', ' + upazila + ', ' + union + ', ' + address
        payment_mobile = request.POST.get('paymentMobile')
        tx_id = request.POST.get('TxID')
        payment_options=request.POST.get('payment-options')
        # Create a new prescription order
        prescription_order_obj = presciption_order.objects.create(
            phonenumber=phone_number,
            prescription_img=prescription_img,
            days=days,
            del_adress=delivery_address,
            timestamp=timezone.now(), # You can set the default status here
            paymentMobile=payment_mobile,
            TxID=tx_id,
            payment_options = payment_options
        )
        prescription_order_obj.save()
    return render(request,'confirm.html')


def update_medlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        med_list_data = data.get('medListData', {})

        # Get the logged-in user's phone number (assuming you're using Django's authentication)
        user_phone_number = request.user.phone_number   # Adjust this according to your user model

        # Update the Profile_MedList
        Profile_MedList.objects.filter(phone_number=user_phone_number).update(
                med_list=med_list_data  # Update this according to your actual data structure
            )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def view_temp_order(request, order_id):
    # Get the temporary order
    temp_order = get_object_or_404(TemporaryOrders, id=order_id)
    
    # Check if the user is authorized to view this order
    if request.user.phone_number != temp_order.phonenumber:
        return HttpResponseForbidden("You are not authorized to view this order.")
    
    # Process ordered products
    ordered_products = []
    if temp_order.ordered_products:
        products_list = ast.literal_eval(temp_order.ordered_products)
        for product in products_list:
            name, quantity, price = product
            ordered_products.append({
                'name': name,
                'quantity': quantity,
                'price': price,
                'subtotal': float(quantity) * float(price)
            })
    
    # Calculate product subtotal
    products_subtotal = sum(item['subtotal'] for item in ordered_products)
    
    # Calculate delivery fee
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
        temporary_order = TemporaryOrders.objects.get(id=order_id)

        # Create a confirmed order from the temporary one
        confirmed_order = Orders.objects.create(
            ordered_products=temporary_order.ordered_products,
            prescriptions=temporary_order.prescriptions,
            timestamp=temporary_order.timestamp,
            phonenumber=temporary_order.phonenumber,
            del_adress=temporary_order.del_adress,
            payment_options=temporary_order.payment_options,
            paymentMobile=temporary_order.paymentMobile,
            TxID=temporary_order.TxID,
            total=temporary_order.total,
            # Copy all necessary fields from temporary_order
        )

        # Optionally delete the temporary order after confirmation
        temporary_order.delete()

        return redirect('profile')  # Redirect to the confirmed order details page
    return redirect('profile')  # Redirect if method is not POST
