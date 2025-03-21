from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import UserProfile
from products.models import main_product, Orders
from django.forms import ModelForm
from django import forms
import ast
from functools import wraps
from django.db.models import Q

# Form for main_product
class MainMedicineForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code', 'otc_status', 'add_to_list', 'p_name', 'Brand',
            'feature', 'medPerStrip', 'p_price', 'p_discount', 'description',
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
            'product_code', 'p_name', 'Brand', 'feature', 'p_price',
            'p_discount', 'description', 'size', 'Manufacturer',
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
            'email', 'address', 'is_super_admin', 'is_admin' ,'is_staff', 'user_type'
        ]



@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'admin/edit_user.html', {'form': form})


@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
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
        users = UserProfile.objects.all()

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
