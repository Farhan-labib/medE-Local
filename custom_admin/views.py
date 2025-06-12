from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import UserProfile
from products.models import main_product, Orders, presciption_order
from django.forms import ModelForm
from django import forms
import ast
from functools import wraps
from django.db.models import Q, Case, When, Value, IntegerField
from django.utils import timezone
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Location, TemporaryOrders
from twilio.rest import Client
from django.conf import settings


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'level', 'parent', 'delivery_fee']
    
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Location.objects.none()
        if 'level' in self.data:
            level = self.data.get('level').lower()
            if level == 'zilla':
                self.fields['parent'].queryset = Location.objects.filter(level='division')
            elif level == 'upazila':
                self.fields['parent'].queryset = Location.objects.filter(level='zilla')
            elif level == 'union':
                self.fields['parent'].queryset = Location.objects.filter(level='upazila')
        elif self.instance.pk and self.instance.parent:
            self.fields['parent'].queryset = Location.objects.filter(level=self.instance.parent.level)
    
    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        delivery_fee = cleaned_data.get('delivery_fee')
        
        if level == 'union' and not delivery_fee:
            self.add_error('delivery_fee', 'Delivery fee is required for Union level')
        
        return cleaned_data


def location_edit(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_manage')
    else:
        form = LocationForm(instance=location)
    
    return render(request, 'admin/location_edit.html', {
        'form': form,
        'location': location
    })


def location_manage(request):
    if request.method == 'POST':
        if 'edit_form' in request.POST:
            location_id = request.POST.get('location_id')
            location = get_object_or_404(Location, id=location_id)
            form = LocationForm(request.POST, instance=location)
        else:
            form = LocationForm(request.POST)
            
        if form.is_valid():
            form.save()
            return redirect('location_manage')
    else:
        form = LocationForm()
    
    level_order = {
        'division': 1,
        'zilla': 2,
        'upazila': 3,
        'union': 4
    }
    
    locations = Location.objects.all().annotate(
        level_sort=Case(
            When(level='division', then=Value(level_order['division'])),
            When(level='zilla', then=Value(level_order['zilla'])),
            When(level='upazila', then=Value(level_order['upazila'])),
            When(level='union', then=Value(level_order['union'])),
            default=Value(99),
            output_field=IntegerField()
        )
    ).order_by('level_sort', 'parent__level', 'name')
    
    return render(request, 'admin/location_manage.html', {
        'form': form,
        'locations': locations,
    })


@csrf_exempt
def update_fee(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        location_id = data.get('location_id')
        delivery_fee = data.get('delivery_fee')
        
        try:
            location = Location.objects.get(id=location_id)
            if location.level != 'union':
                return JsonResponse({'success': False, 'message': 'Only union level locations can have delivery fees'})
            
            location.delivery_fee = delivery_fee
            location.save()
            return JsonResponse({'success': True})
        except Location.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Location not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def location_delete(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    if request.method == 'POST':
        location.delete()
    return redirect('location_manage')


def get_parents_by_level(request):
    level = request.GET.get('level', '').lower()
    data = []

    if level == 'zilla':
        data = Location.objects.filter(level='division').values('id', 'name')
    elif level == 'upazila':
        data = Location.objects.filter(level='zilla').values('id', 'name')
    elif level == 'union':
        data = Location.objects.filter(level='upazila').values('id', 'name')

    return JsonResponse(list(data), safe=False)


class MainMedicineForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
             'product_code', 'otc_status', 'add_to_list', 'p_name', 'Brand',
            'Dosage_Feature', 'size', 'Manufacturer', 'p_generics', 
            'p_type', 'p_image', 'p_Dosage_Strength', 'Variant', 'p_category', 
            'p_Indications', 'p_Administration', 'p_Pharmacology', 'p_Side_Effects',
            'p_Interaction', 'p_Contradictions', 'p_Precautions', 'p_Pregnancy',
            'p_Therapeutic', 'p_Storage', 'FAQ', 'Suggestions', 'Overdose_Effect',
        ]
        labels = {
            'product_code': 'Code Name',
            'otc_status': 'OTC Status',
            'add_to_list': 'ADD to List',
            'p_name': 'Product Name',
            'Brand': 'Brand',
            'Manufacturer': 'Manufacturer',
            'p_generics': 'Generic',
            'p_type': 'Dosage Type',
            'p_Dosage_Strength': 'Dosage Strength',
            'Dosage_Feature': 'Dosage Feature',
            'p_category': 'Drug Category',
            'Variant': 'Variant',
            'size': 'Size',
            'p_Administration': 'Administration of Dosage',
            'p_Indications': 'Indications',
            'p_Pharmacology': 'Pharmacology',
            'p_Side_Effects': 'Side Effect',
            'Overdose_Effect': 'Overdose Effect',
            'p_Interaction': 'Interaction',
            'p_Contradictions': 'Contradiction',
            'p_Precautions': 'Precaution',
            'p_Pregnancy': 'Pregnancy',
            'p_Therapeutic': 'Therapeutic',
            'p_Storage': 'Storage Condition',
            'FAQ': 'FAQ',
            'Suggestions': 'Suggestions',
            'p_image': 'Product Image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_code'] = forms.CharField(
            label='Code Name',
            required=False,
            widget=forms.TextInput(attrs={'readonly': 'readonly'})
        )

    def save(self, commit=True):
        # Auto-generate product_code using p_name, p_type, and size
        name = self.cleaned_data.get('p_name', '').replace(' ', '_')
        dosage_type = self.cleaned_data.get('p_type', '').replace(' ', '_')
        size = self.cleaned_data.get('size', '').replace(' ', '_')

        self.instance.product_code = f"{name}_{dosage_type}_{size}"

        # Set fixed field
        self.instance.m_or_g = "Medicines"  

        return super().save(commit=commit)


class MainGeneralForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code', 'p_name', 'Brand',
            'size', 'Manufacturer',
            'p_type', 'p_image', 'Variant', 'p_category', 'Features_Specifications','Model', 'Description',
        ]
        labels = {
            'product_code': 'Code Name',
            'p_name': 'Product Name',
            'Brand': 'Brand',
            'size': 'Size',
            'Model': 'Model',
            'Manufacturer': 'Manufacturer',
            'p_type': 'Sub-Category',
            'p_image': 'Product Image',
            'Variant': 'Variant',
            'p_category': 'Drug Category',
            'Features_Specifications': 'Features / Specifications',
            'Description': 'Description',
        }

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
    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})


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
                    Q(is_staff=True) | Q(is_super_admin=True) | Q(is_admin=True)
                )

    return render(request, 'admin/admin_list.html', {'users': users})


@admin_required
def order_list(request):
    sort_by = request.GET.get('sort_by', '')
    payment_method = request.GET.get('payment_method', '')
    status = request.GET.get('status', '')
    
    orders = Orders.objects.all().order_by('-timestamp')

    if payment_method:
        orders = orders.filter(payment_options=payment_method)
    
    if status:
        orders = orders.filter(status=status)
    
    return render(request, 'admin/orders.html', {'orders': orders})


class OrderUpdateForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['status']
        widgets = {
            'prescriptions': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'ordered_products': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'total': forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            'del_adress': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }


@admin_required
def order_details(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)

    try:
        ordered_products = ast.literal_eval(order.ordered_products)
        if not isinstance(ordered_products, list):
            ordered_products = []
    except:
        ordered_products = []

    if request.method == 'POST' and 'return_order' in request.POST:
        if order.status == 'Confirmed':
            try:
                for_stock_data = ast.literal_eval(order.for_stock)

                if isinstance(for_stock_data, dict):
                    for product_id, product_info in for_stock_data.items():
                        try:
                            quantity = int(product_info['quantity'])
                            packaging = product_info['packaging']
                            med_per_strip = float(product_info['medPerStrip'])
                            strip_per_box = float(product_info['stripPerBox'])

                            if packaging == 'Piece':
                                final_quantity = quantity
                            elif packaging == 'Pack':
                                final_quantity = quantity * med_per_strip
                            elif packaging == 'Box':
                                final_quantity = quantity * med_per_strip * strip_per_box
                            else:
                                final_quantity = quantity

                            product = main_product.objects.get(p_id=product_id)
                            product.Stock += int(final_quantity)
                            product.save()

                        except Exception:
                            pass  # Consider logging errors in real app

            except Exception:
                pass

            order.status = 'Failed'
            order.save()

        return redirect('order_details', order_id=order.id)




    if request.method == 'POST' and 'status' in request.POST:
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            updated_order = form.save(commit=False)

            if updated_order.status == 'Confirmed':
                try:
                    for_stock_data = ast.literal_eval(order.for_stock)
                    if isinstance(for_stock_data, dict):
                        for product_id, product_info in for_stock_data.items():
                            try:
                                quantity = int(product_info['quantity'])
                                packaging = product_info['packaging']
                                med_per_strip = product_info['medPerStrip']
                                strip_per_box = product_info['stripPerBox']

                                if packaging == 'Piece':
                                    final_quantity = quantity
                                elif packaging == 'Pack':
                                    final_quantity = quantity * med_per_strip
                                elif packaging == 'Box':
                                    final_quantity = quantity * med_per_strip * strip_per_box
                                else:
                                    final_quantity = quantity

                                product = main_product.objects.get(p_id=product_id)
                                product.Stock -= final_quantity
                                product.save()

                            except (main_product.DoesNotExist, KeyError, Exception):
                                pass
                except Exception:
                    pass

            updated_order.save()
            return redirect('order_details', order_id=order.id)
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'admin/order_details.html', {
        'form': form,
        'order': order,
        'ordered_products': ordered_products,
    })


@admin_required
def prescription(request):
    sort_by = request.GET.get('sort_by', '')
    payment_method = request.GET.get('payment_method', '')
    status = request.GET.get('status', '')
    
    orders = presciption_order.objects.all().order_by('-timestamp')

    if payment_method:
        orders = orders.filter(payment_options=payment_method)
    
    if status:
        orders = orders.filter(Order_status=status)
    
    return render(request, 'admin/prescription.html', {'orders': orders})


def pres_details(request, order_id):
    order = get_object_or_404(presciption_order, pk=order_id)
    medicines = main_product.objects.filter(inventory=1)

    for product in medicines:
        product.discounted_price = product.p_price - (product.p_price * (product.p_discount / 100))

    return render(request, 'admin/pres_details.html', {'order': order, 'medicines': medicines})


@csrf_protect
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            products = data['products']
            ordered_products = []
            total_amount = 0.0
            print("Received products:", products)

            # Build ordered_products list and calculate total_amount
            for product in products:
                # product = [name, quantity, total_price, product_code]
                ordered_products.append((product[0], product[1], product[2]))
                total_amount += float(product[2])

            # Prepare delivery fee
            delivery_fee = 60
            delivery_address = data.get("delivery_address")
            if delivery_address and delivery_address != "null":
                parts = delivery_address.split(", ")
                if len(parts) > 3:
                    union_name = parts[3]
                    try:
                        union_obj = Location.objects.get(name=union_name, level='union')
                        if union_obj.delivery_fee:
                            delivery_fee = float(union_obj.delivery_fee)
                    except Location.DoesNotExist:
                        pass
            total_amount += delivery_fee

            # Prescriptions list
            prescriptions_list = []
            if data.get("prescriptions") and data["prescriptions"] != "null":
                prescriptions_list.append(data['prescriptions'])

            # Build for_stock dictionary keyed by main_product.p_id
            for_stock = {}
            for product in products:
                product_code = product[3]
                try:
                    main_prod_obj = main_product.objects.get(product_code=product_code)
                    # Use p_id as key (converted to string for JSON serializability)
                    for_stock[str(main_prod_obj.p_id)] = {
                        'packaging': 'Piece',
                        'quantity': int(product[1]),
                        'price': str(product[2]),
                        'medPerStrip': float(main_prod_obj.medPerStrip),
                        'stripPerBox': float(main_prod_obj.stripPerBox),
                        'name': main_prod_obj.p_name,
                        'image': main_prod_obj.p_image.url if main_prod_obj.p_image else ''
                    }
                except main_product.DoesNotExist:
                    # Handle missing product gracefully
                    for_stock[product_code] = {'error': f'Product with code {product_code} not found'}

            # Create TemporaryOrders record
            temp_order = TemporaryOrders.objects.create(
                phonenumber=data['phone_number'],
                ordered_products=str(ordered_products),
                total=total_amount,
                del_adress=delivery_address,
                payment_options=data['payment_method'],
                status="Pending",
                TxID=data.get('TxID'),
                paymentMobile=data.get('payment_mobile'),
                prescriptions=prescriptions_list,
                Delivery_status="Pending",
                timestamp=timezone.now(),
                for_stock=for_stock  # Make sure your model has JSONField for this
            )

            # Send SMS via Twilio (optional)
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message_body = (
                f"Dear Customer,\n"
                f"Your order has been generated.\n"
                f"Please click the link to go to your order page and confirm the order:\n"
                f"http://127.0.0.1:8000/temp-order/{temp_order.id}/\n\n"
                f"Thank you"
            )
            try:
                client.messages.create(
                    body=message_body,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=data['phone_number']
                )
            except Exception:
                pass

            return JsonResponse({"message": "Temporary Order Created", "temp_order_id": temp_order.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            new_status = data.get("order_status")

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
    search_query = request.GET.get('search', '')
    products = main_product.objects.all()

    if search_query:
        products = products.filter(
            Q(p_name__icontains=search_query) | 
            Q(product_code__icontains=search_query) | 
            Q(p_category__icontains=search_query)
        )

    return render(request, 'admin/inventory.html', {
        'products': products,
        'search_query': search_query,
    })


def inventory_dashboard(request):
    products = main_product.objects.filter(inventory=1)
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
    BUNDLING_CHOICES = [
        ('Box', 'Box'),
        ('Pack', 'Pack'),
        ('Piece', 'Piece')
    ]
    bundling = forms.MultipleChoiceField(
        choices=BUNDLING_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    medPerStrip = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    stripPerBox = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    inventory = forms.IntegerField(widget=forms.HiddenInput(), required=False)


def inventory_edit(request, product_id):
    product = get_object_or_404(main_product, p_id=product_id)

    if request.method == 'POST':
        form = ProductEditForm(request.POST)
        if form.is_valid():
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
            product.stripPerBox = form.cleaned_data['stripPerBox']
            product.bundling = ', '.join(form.cleaned_data['bundling'])
            product.inventory = 1
            product.save()
            return redirect('inventory_dashboard')
    else:
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
            'stripPerBox': product.stripPerBox,
            'bundling': product.bundling.split(', ') if product.bundling else [],
        }
        form = ProductEditForm(initial=initial_data)

    return render(request, 'admin/edit_inventory.html', {'form': form, 'product': product})