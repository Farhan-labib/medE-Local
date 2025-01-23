from django.shortcuts import render
from authentication.models import UserProfile

from django.shortcuts import render, get_object_or_404, redirect
from products.models import main_product
from django.forms import ModelForm
from django.contrib import messages

# Form for main_product
class MainProductForm(ModelForm):
    class Meta:
        model = main_product
        fields = '__all__'  # Include all fields from the model

        labels = {
            'product_code': 'Product Code:',
            'p_name': 'Product Name:',
            'p_type': 'Product Type:',
            'otc_status': 'OTC Status:',
            'p_image': 'Product Image:',
            'p_generics': 'Generics:',
            'p_company': 'Company:',
            'medPerStrip': 'Medicine Per Strip:',
            'p_price': 'Price:',
            'p_discount': 'Discount Percentage:',
            'p_Indications': 'Indications:',
            'p_Pharmacology': 'Pharmacology:',
            'p_Dosage': 'Dosage:',
            'p_Interaction': 'Interactions:',
            'p_Contradictions': 'Contradictions:',
            'p_Side_Effects': 'Side Effects:',
            'p_Pregnancy': 'Pregnancy Warnings:',
            'p_Precautions': 'Precautions:',
            'p_Therapeutic': 'Therapeutic Uses:',
            'p_Storage': 'Storage Conditions:',
            'p_category': 'Category:',
            'feature': 'Feature:',
            'add_to_list': 'Add to List:',
            'inventory_quantity': 'Inventory Quantity:',
            'description': 'Product Description:',
            'size': 'Size:',
            'p_Dosage_Strength': 'Dosage Strength:',
            'p_link': 'Product Link:',
        }

def create_product(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = MainProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product created successfully!")
                return redirect('admin_product')
        else:
            form = MainProductForm()
        return render(request, 'admin/create_product.html', {'form': form})
    return render(request, 'admin/error.html')

def update_product(request, p_id):
    if request.user.is_staff:
        product = get_object_or_404(main_product, p_id=p_id)
        if request.method == 'POST':
            form = MainProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully!")
                return redirect('admin_product')
        else:
            form = MainProductForm(instance=product)
        return render(request, 'admin/update_product.html', {'form': form, 'product': product})
    return render(request, 'admin/error.html')

def delete_product(request, p_id):
    if request.user.is_staff:
        product = get_object_or_404(main_product, p_id=p_id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('admin_product')
    return render(request, 'admin/error.html')


def dashboard(request):
    if request.user.is_staff:
        return render(request, 'admin/dashboard.html')
    else:
        return render(request, 'admin/error.html')
def product(request):
    if request.user.is_staff:
        products = main_product.objects.all()
        return render(request, 'admin/admin_product.html', {'products': products})
    else:
        return render(request, 'admin/error.html')
