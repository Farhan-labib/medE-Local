from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from products.models import Orders
from authentication.models import UserProfile
from products.models import Profile_MedList
from products.models import presciption_order
import ast
from django.http import JsonResponse
from products.models import main_product 
from django.core.files.storage import FileSystemStorage
import os
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
    orders = Orders.objects.filter(phonenumber=phonenumber) 
    p_order=presciption_order.objects.filter(phonenumber=phonenumber) 
    temp={}
    for i in orders:
        d=[]
        data=ast.literal_eval(i.ordered_products)
        for item in data:
            name, number, _ = item
            d.append(str(name+"X"+number))


        temp[i.id]=[d,i.total,i.timestamp,i.Delivery_status]

    # Medlist  From here

    
    # print('User Phone Number:', phonenumber)  # Check the user phone number in Django console

    # Assuming 'phone_number' is the field name in your Profile_MedList model
    saved_data = Profile_MedList.objects.filter(phone_number=phonenumber).values()

    # Convert the QuerySet to a list of dictionaries
    data_list = list(saved_data)
    # print(data_list)
    print(p_order)
    return render(request, 'user-profile.html', {'temp': temp,'medList': data_list, 'p_order':p_order})


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
        price=(products_data[counter]['p_price'] - (products_data[counter]['p_price']*(products_data[counter]['p_discount']/100)))/medPerStrip
        quantity=(products_data[counter]['medPerStrip']*morning_day_len*dayy)/medPerStrip
        t.append((products_data[counter]['p_name'], str(int(quantity)), '{:.2f}'.format(float(price * quantity))))         
        total+=round(price*quantity,2)

    if(total>0):
        total+=60
    context={'product_data_list': t, 'total': total, 'user_address': user_address}
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
