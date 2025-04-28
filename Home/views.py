from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from products.models import Orders
from authentication.models import UserProfile
from products.models import Profile_MedList
from products.models import presciption_order
import ast
from custom_admin.models import Location, TemporaryOrders
from django.http import JsonResponse
from products.models import main_product 
from django.core.files.storage import FileSystemStorage
import os
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
def home(request):
    products = Product.objects.all()
    for product in products:

        product.discounted_price = product.p_price - (product.p_price*(product.p_discount/100))	#FOR DISCOUNT
    print(products)
    return render(request,'index.html',{'products': products})



def profile(request):
    User = UserProfile()
    phonenumber = request.user.phone_number
    
    # Get data from both tables
    orders = Orders.objects.filter(phonenumber=phonenumber)
    temp_orders = TemporaryOrders.objects.filter(phonenumber=phonenumber)
    p_order = presciption_order.objects.filter(phonenumber=phonenumber)
    
    # Process Orders data
    orders_data = {}
    for i in orders:
        d = []
        data = ast.literal_eval(i.ordered_products)
        print("hello world", data)
        for item in data:
            try:
                # Check if item has 3 elements
                if len(item) == 3:
                    name, number, _ = item
                    d.append(str(name + "X" + number))
                else:
                    # Handle the case where the length is not 3
                    name, number, unit, price = item  # Adjust based on the correct number of elements
                    d.append(f"{name}X{number} ({unit} - {price})")  # Customize as per your needs
            except ValueError:
                print(f"Skipping invalid item: {item}")

        orders_data[i.id] = [d, i.total, i.timestamp, i.status]
    
    # Process TemporaryOrders data
    temp_orders_data = {}
    for i in temp_orders:
        d = []
        data = ast.literal_eval(i.ordered_products)
        for item in data:
            name, number, _ = item
            d.append(str(name + "X" + number))
        
        temp_orders_data[i.id] = [d, i.total, i.timestamp, i.status, True]  # Last True indicates temporary order
    
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
    saved_data = Profile_MedList.objects.filter(phone_number=phonenumber).values()
    data_list = list(saved_data)
    med_list = data_list[0]['med_list']
    counter=0
    t=[]
    total=0
    for key,value in med_list.items():
        morning_day_len = len(med_list[key][0])  # Length of ['Morning', 'Day']
        dayy = med_list[key][1]  # The value 5
        products_data = main_product.objects.filter(p_id=int(key)).values('p_name', 'medPerStrip', 'p_price','p_discount')
        medPerStrip = products_data[counter]['medPerStrip']
        price=(products_data[counter]['p_price'] - (products_data[counter]['p_price']*(products_data[counter]['p_discount']/100)))
        quantity=(products_data[counter]['medPerStrip']*morning_day_len*dayy)/medPerStrip
        t.append((products_data[counter]['p_name'], str(int(quantity)),"Piece", '{:.2f}'.format(float(price * quantity))))         
        total+=round(price*quantity,2)

    
    prescription_required = request.session.get('prescription_required', False)
    for_stock = request.session.get('for_stock', {})
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

    context={'product_data_list': t,
             'total': total, 
             'user_address': user_address,
             
             'prescription_required': prescription_required,
             'division_data': json.dumps(list(division_data.keys())),  # Convert to list for JS
             'zilla_data': json.dumps(zilla_data),
             'upazila_data': json.dumps(upazila_data),
             'union_data': json.dumps(union_data),
             'for_stock': for_stock,
             'union_data': json.dumps(union_data, cls=DjangoJSONEncoder),}
    print(context)
    return render(request, 'order_confirm.html', context)

    

def upload_prescription(request):
    if request.method == 'POST':
        prescription_image = request.FILES.get('prescription_image')
        selected_days = request.POST.getlist('selected_days')
        phone_number = request.user.phone_number  # Replace this with the actual method to get the user's phone number.

        # Create the user's prescription folder if it doesn't exist.
        user_prescription_folder = os.path.join('media', 'prescription', str(phone_number))
        if not os.path.exists(user_prescription_folder):
            os.makedirs(user_prescription_folder)

        # Save the prescription image to the user's folder.
        fs = FileSystemStorage(location=user_prescription_folder)
        saved_image = fs.save(prescription_image.name, prescription_image)
        image= "prescription/"+phone_number+"/"+saved_image

        # Update the prescriptions column in the database
        try:
            user_medlist = Profile_MedList.objects.get(phone_number=phone_number)
            prescriptions = user_medlist.prescriptions

            if prescriptions:
                prescriptions.append((image, selected_days[0]))
            else:
                prescriptions = [(image, selected_days[0])]

            user_medlist.prescriptions = (prescriptions)
            user_medlist.save()

            return JsonResponse({'success': True})
        except Profile_MedList.DoesNotExist:
            # Create a new user with the provided phone number
            new_user_medlist = Profile_MedList(phone_number=phone_number, prescriptions=([(image, selected_days[0])]))
            new_user_medlist.save()
            return JsonResponse({'success': True})
    # Handle other HTTP methods if needed

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def searchresult(request):
    if request.method == 'POST':
        # Get the search results data from the request
        search_results_json = request.POST.get('search_results', None)

        if search_results_json:
            # Parse the JSON data
            search_results = json.loads(search_results_json)

            # Process the search results as needed

            p_id_list = [item['p_id'] for item in search_results]
            p_details = []
            for id in p_id_list:
                products = main_product.objects.filter(p_id=id)
                for product in products:
                    product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))
                    print(product.p_image)
                p_details.append(products)

            context = {
                'product_details': p_details,
            }
            
            
            # Render the HTML template with the context
            html_content = render(request, 'search-results.html', context).content.decode('utf-8')

            # Return the HTML content as the response
            return HttpResponse(html_content)
    
    # Return an error response if the request doesn't contain the expected data
    return HttpResponse('Invalid request', status=400)
