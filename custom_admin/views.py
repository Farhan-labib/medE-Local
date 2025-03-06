from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import UserProfile
from products.models import main_product, Orders
from django.forms import ModelForm
from django.contrib import messages
from django import forms
import ast
from django.contrib import messages


# Form for main_product
class MainMedicineForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code', 'otc_status', 'add_to_list', 'p_name', 'Brand',
            'feature', 'medPerStrip', 'p_price', 'p_discount', 'description',
            'size', 'm_or_g', 'Manufacturer', 'p_generics', 'p_type', 'p_image',
            'p_Dosage_Strength', 'Variant', 'p_category', 'p_Indications',
            'p_Administration', 'p_Pharmacology', 'p_Side_Effects',
            'p_Interaction', 'p_Contradictions', 'p_Precautions', 'p_Pregnancy',
            'p_Therapeutic', 'p_Storage', 'FAQ', 'Suggestions',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = field_name.replace('_', ' ').title()


class MainGeneralForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code', 'p_name', 'Brand', 'feature', 'p_price',
            'p_discount', 'description', 'size', 'm_or_g', 'Manufacturer',
            'p_type', 'p_image', 'Variant', 'p_category', 'Features_Specifications',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = field_name.replace('_', ' ').title()


def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, 'admin/error.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@staff_required
def create_product(request):
    form = MainMedicineForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product created successfully!")
        return redirect('admin_product')
    return render(request, 'admin/create_product.html', {'form': form})


@staff_required
def create_general(request):
    form = MainGeneralForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product created successfully!")
        return redirect('admin_product')
    return render(request, 'admin/create_general.html', {'form': form})


@staff_required
def update_product(request, p_id):
    product = get_object_or_404(main_product, p_id=p_id)
    form = MainMedicineForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully!")
        return redirect('admin_product')
    return render(request, 'admin/update_product.html', {'form': form, 'product': product})


@staff_required
def update_general(request, p_id):
    product = get_object_or_404(main_product, p_id=p_id)
    form = MainGeneralForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully!")
        return redirect('admin_product')
    return render(request, 'admin/update_general.html', {'form': form, 'product': product})


@staff_required
def delete_product(request, p_id):
    product = get_object_or_404(main_product, p_id=p_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('admin_product')


@staff_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')


@staff_required
def product(request):
    products = main_product.objects.all()
    return render(request, 'admin/admin_product.html', {'products': products})


@staff_required
def medicine(request):
    products = main_product.objects.filter(m_or_g='Medicines')
    return render(request, 'admin/medicines.html', {'products': products})


@staff_required
def general(request):
    products = main_product.objects.filter(m_or_g='Generals')
    return render(request, 'admin/general.html', {'products': products})


@staff_required
def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'admin/user.html', {'users': users})


class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'first_name', 'last_name', 'dob', 'gender',
            'email', 'address', 'is_staff', 'is_active', 'user_type'
        ]


@staff_required
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "User updated successfully!")
        return redirect('user_list')
    return render(request, 'admin/edit_user.html', {'form': form})


@staff_required
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('user_list')


@staff_required
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

@staff_required
def order_details(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)

    if not request.user.is_staff:
        return render(request, 'admin/error.html')

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
            messages.success(request, "Order updated successfully!")
            return redirect('order_details', order_id=order.id)
    else:
        form = OrderUpdateForm(instance=order)

    context = {
        'form': form,
        'order': order,
        'ordered_products': ordered_products,  # Add the parsed ordered_products to the context
    }
    return render(request, 'admin/order_details.html', context)
