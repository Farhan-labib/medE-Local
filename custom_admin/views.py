from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import UserProfile
from products.models import main_product, Orders, presciption_order
from django.forms import ModelForm
from django import forms
import ast
from functools import wraps
from django.db.models import Q
from django.utils import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'level', 'parent']

# View to show the list and handle form submission for adding new locations
def location_manage(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_manage')  # Redirect to the same page to show updated list
    else:
        form = LocationForm()

    locations = Location.objects.all()
    return render(request, 'admin/location_manage.html', {'locations': locations, 'form': form})

class MainMedicineForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code', 'otc_status', 'add_to_list', 'p_name', 'Brand',
            'feature', 'description',
            'size', 'Manufacturer', 'p_generics', 'p_type', 'p_image',
            'p_Dosage_Strength', 'Variant', 'p_category', 'p_Indications',
            'p_Administration', 'p_Pharmacology', 'p_Side_Effects',
            'p_Interaction', 'p_Contradictions', 'p_Precautions', 'p_Pregnancy',
            'p_Therapeutic', 'p_Storage', 'FAQ', 'Suggestions',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = field_name.replace('_', ' ').title()

    def save(self, commit=True):
        self.instance.m_or_g = "Medicines"  
        return super().save(commit)



class MainGeneralForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code', 'p_name', 'Brand', 'feature',
             'description', 'size', 'Manufacturer',
            'p_type', 'p_image', 'Variant', 'p_category', 'Features_Specifications',]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = field_name.replace('_', ' ').title()

    def save(self, commit=True):
        self.instance.m_or_g = "Generals"  
        return super().save(commit)



def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_admin or request.user.is_super_admin):
            return render(request, 'admin/error.html')  
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@admin_required
def create_product(request):
    form = MainMedicineForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_product')
    return render(request, 'admin/create_product.html', {'form': form})


@admin_required
def create_general(request):
    form = MainGeneralForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_product')
    return render(request, 'admin/create_general.html', {'form': form})


@admin_required
def update_product(request, p_id):
    product = get_object_or_404(main_product, p_id=p_id)
    form = MainMedicineForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_product')
    return render(request, 'admin/update_product.html', {'form': form, 'product': product})


@admin_required
def update_general(request, p_id):
    product = get_object_or_404(main_product, p_id=p_id)
    form = MainGeneralForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_product')
    return render(request, 'admin/update_general.html', {'form': form, 'product': product})


@admin_required
def delete_product(request, p_id):
    product = get_object_or_404(main_product, p_id=p_id)
    product.delete()
    return redirect('admin_product')


@admin_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')


@admin_required
def product(request):
    products = main_product.objects.all()
    return render(request, 'admin/admin_product.html', {'products': products})


@admin_required
def medicine(request):
    products = main_product.objects.filter(m_or_g='Medicines')
    return render(request, 'admin/medicines.html', {'products': products})


@admin_required
def general(request):
    products = main_product.objects.filter(m_or_g='Generals')
    return render(request, 'admin/general.html', {'products': products})


@admin_required
def user_list(request):
    users = UserProfile.objects.exclude(is_staff=True) \
                            .exclude(is_super_admin=True) \
                            .exclude(is_admin=True)

    return render(request, 'admin/user.html', {'users': users})


class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'first_name', 'last_name', 'dob', 'gender',
            'email', 'address', 'is_super_admin', 'is_admin', 'is_staff', 'user_type'
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if self.instance and (self.instance.is_super_admin or self.instance.is_admin or self.instance.is_staff):
            self.fields.pop('user_type', None)




@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        if user.is_super_admin or user.is_admin or user.is_staff:
            return redirect('admin_list')
        return redirect('user_list')
    return render(request, 'admin/edit_user.html', {'form': form})


@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    if user.is_super_admin or user.is_admin or user.is_staff:
            return redirect('admin_list')
    return redirect('user_list')


@admin_required
def admin_list(request):
    role_filter = request.GET.get('role', '')
    
    if role_filter:
        if role_filter == 'admin':
            users = UserProfile.objects.filter(is_admin=True)
        elif role_filter == 'staff':
            users = UserProfile.objects.filter(is_staff=True)
        elif role_filter == 'superadmin':
            users = UserProfile.objects.filter(is_super_admin=True)
        else:
            users = UserProfile.objects.all()
    else:
        users = UserProfile.objects.filter(
                    is_staff=True
                ) | UserProfile.objects.filter(
                    is_super_admin=True
                ) | UserProfile.objects.filter(
                    is_admin=True
                )



    return render(request, 'admin/admin_list.html', {'users': users})




@admin_required
def order_list(request):
    sort_by = request.GET.get('sort_by', '')
    payment_method = request.GET.get('payment_method', '')
    status = request.GET.get('status', '')
    
    orders = Orders.objects.all()

    if payment_method:
        orders = orders.filter(payment_options=payment_method)
    
    if status:
        orders = orders.filter(status=status)
    
    if sort_by:
        orders = orders.order_by('-timestamp')  
  
    orders = orders.order_by('-timestamp')  
    
    context = {
        'orders': orders,
    }

    return render(request, 'admin/orders.html', context)




class OrderUpdateForm(ModelForm):
    class Meta:
        model = Orders
        fields = [
            'status'
        ]
        widgets = {
            'prescriptions': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'ordered_products': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'total': forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            'del_adress': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }

@admin_required
def order_details(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)


    # Parse ordered_products safely to a list of tuples
    try:
        ordered_products = ast.literal_eval(order.ordered_products)
        if not isinstance(ordered_products, list):
            ordered_products = []  # Handle cases where it's not a list
    except:
        ordered_products = []  # If parsing fails, use an empty list

    # Handle form submission to update the order
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_details', order_id=order.id)
    else:
        form = OrderUpdateForm(instance=order)

    context = {
        'form': form,
        'order': order,
        'ordered_products': ordered_products,  # Add the parsed ordered_products to the context
    }
    return render(request, 'admin/order_details.html', context)


@admin_required
def prescription(request):
    sort_by = request.GET.get('sort_by', '')
    payment_method = request.GET.get('payment_method', '')
    status = request.GET.get('status', '')
    
    orders = presciption_order.objects.all()

    if payment_method:
        orders = orders.filter(payment_options=payment_method)
    
    if status:
        orders = orders.filter(Order_status=status)
    
    if sort_by:
        orders = orders.order_by('-timestamp')  
  
    orders = orders.order_by('-timestamp')  
    
    context = {
        'orders': orders,
    }

    return render(request, 'admin/prescription.html', context)

def pres_details(request, order_id):
    order = get_object_or_404(presciption_order, pk=order_id)
    medicines = main_product.objects.filter(inventory=1)

    # Calculate discounted price for each product
    for product in medicines:
        discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))
        product.discounted_price = discounted_price

    return render(request, 'admin/pres_details.html', {'order': order, 'medicines': medicines})

    
@csrf_protect
def create_order(request):
    if request.method == "POST":
        try:
            # Get data from request body
            data = json.loads(request.body)

            # Extract product details
            products = data['products']
            ordered_products = []
            total_amount = 0.0

            # Format ordered products as [('Medicine Name', 'Quantity', 'Total Price')]
            for product in products:
                ordered_products.append((product[0], product[1], product[2]))
                total_amount += float(product[2])


            prescriptions_list = []
            if data.get("prescriptions") and data["prescriptions"] != "null":
                    prescriptions_list.append(data['prescriptions'])
        
            # Create the order in the database
            order = Orders.objects.create(
                phonenumber=data['phone_number'],
                ordered_products=str(ordered_products),  # Save as a string of the tuple
                total=total_amount,
                del_adress=data['delivery_address'],
                payment_options=data['payment_method'],
                status="Pending",
                TxID=data.get('TxID'),
                paymentMobile=data.get('payment_mobile'),
                prescriptions=prescriptions_list,
                Delivery_status="Pending",
                timestamp=timezone.now(),
            )

            # Send success response
            return JsonResponse({"message": "Order Created Successfully", "order_id": order.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            new_status = data.get("order_status")

            # Fetch and update the order status
            order = presciption_order.objects.get(id=order_id)
            order.Order_status = new_status
            order.save()

            return JsonResponse({"message": "Order status updated successfully!"}, status=200)

        except presciption_order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def inventory(request):
    search_query = request.GET.get('search', '')  # Get search query from the URL
    products = main_product.objects.all()  # Get all products by default

    if search_query:
        products = products.filter(
            p_name__icontains=search_query) | products.filter(
            product_code__icontains=search_query) | products.filter(
            p_category__icontains=search_query)

    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'admin/inventory.html', context)


    

def inventory_dashboard(request):
    # Query all products where inventory equals 1
    products = main_product.objects.filter(inventory=1)
    
    # Pass the products to the template
    return render(request, 'admin/inventory_dashboard.html', {'products': products})


class ProductEditForm(forms.Form):
    p_type = forms.CharField(max_length=255)
    p_name = forms.CharField(max_length=255)
    product_code = forms.CharField(max_length=255)
    SKU = forms.CharField(max_length=255, required=False)
    Batch = forms.CharField(max_length=255, required=False)
    MFG_Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    EXP_Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    Stock = forms.IntegerField(required=False)
    Purchase_Price = forms.DecimalField(max_digits=10, decimal_places=2)
    p_price = forms.DecimalField(max_digits=10, decimal_places=2)
    p_discount = forms.DecimalField(max_digits=5, decimal_places=2)
    medPerStrip = forms.DecimalField(max_digits=10, decimal_places=2)
    
    # Hidden field for inventory
    inventory = forms.IntegerField(widget=forms.HiddenInput(), required=False)

def inventory_edit(request, product_id):
    # Fetch the product instance
    product = get_object_or_404(main_product, p_id=product_id)

    if request.method == 'POST':
        # If the form is submitted, bind the form with the posted data
        form = ProductEditForm(request.POST)

        if form.is_valid():
            # Update the product's attributes from the form data
            product.p_type = form.cleaned_data['p_type']
            product.p_name = form.cleaned_data['p_name']
            product.product_code = form.cleaned_data['product_code']
            product.SKU = form.cleaned_data['SKU']
            product.Batch = form.cleaned_data['Batch']
            product.MFG_Date = form.cleaned_data['MFG_Date']
            product.EXP_Date = form.cleaned_data['EXP_Date']
            product.Stock = form.cleaned_data['Stock']
            product.Purchase_Price = form.cleaned_data['Purchase_Price']
            product.p_price = form.cleaned_data['p_price']
            product.p_discount = form.cleaned_data['p_discount']
            product.medPerStrip = form.cleaned_data['medPerStrip']
            product.inventory = 1
            
            # Save the updated product to the database
            product.save()

            # Redirect to the inventory dashboard (or another appropriate page)
            return redirect('inventory_dashboard')
    else:
        # If it's a GET request, pre-fill the form with the product's existing data
        initial_data = {
            'p_type': product.p_type,
            'product_code': product.product_code,
            'p_name': product.p_name,
            'SKU': product.SKU,
            'Batch': product.Batch,
            'MFG_Date': product.MFG_Date,
            'EXP_Date': product.EXP_Date,
            'Stock': product.Stock,
            'Purchase_Price': product.Purchase_Price,
            'p_price': product.p_price,
            'p_discount': product.p_discount,
            'medPerStrip': product.medPerStrip,
        }

        form = ProductEditForm(initial=initial_data)

    return render(request, 'admin/edit_inventory.html', {'form': form, 'product': product})