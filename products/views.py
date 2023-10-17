from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import main_product
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import UserProfile

# Create your views here.
def prod(request, p_name):
    product_details = {
        'name': p_name
    }

    try:
        product = main_product.objects.get(p_name=product_details['name'])
        product.discounted_price = product.p_price - (product.p_price*(product.p_discount/100))	#FOR DISCOUNT
         
    except main_product.DoesNotExist:
        product = None
        

    if request.user.is_authenticated:
        # Check if the user is logged in
            try:
                user_profile = UserProfile.objects.get(pk=request.user.id)
                if user_profile.user_type == 'quantity':
                    # Check if the user's type is 'quantity'
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
            'p_price': str(product.p_price),
            'p_discount': str(product.p_discount),
            'discounted_price':product.p_price - (product.p_price * (product.p_discount / 100)),
            'medPerStrip':product.medPerStrip,
            'p_image':str(product.p_image),
            # Add other fields as needed
        }
        return JsonResponse(product_data)
    
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

