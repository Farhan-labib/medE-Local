from django.shortcuts import render
from authentication.models import UserProfile

from django.shortcuts import render, get_object_or_404, redirect
from products.models import main_product
from django.forms import ModelForm
from django.contrib import messages

# Form for main_product
class MainMedicineForm(ModelForm):
    class Meta:
        model = main_product
        fields = [
            'product_code',
            'otc_status',
            'add_to_list',
            'p_name',
            'Brand',
            'feature',
            'medPerStrip',
            'p_price',
            'p_discount',
            'description',
            'size',
            'm_or_g',
            'Manufacturer',
            'p_generics',
            'p_type',
            'p_image',
            'p_Dosage_Strength',
            'Variant',
            'p_category',
            'p_Indications',
            'p_Administration',
            'p_Pharmacology',
            'p_Side_Effects',
            'p_Interaction',
            'p_Contradictions',
            'p_Precautions',
            'p_Pregnancy',
            'p_Therapeutic',
            'p_Storage',
            'FAQ',
            'Suggestions',
        ]

        labels = {
            'product_code': 'Product Code:',
            'otc_status': 'OTC Status:',
            'add_to_list': 'Add to List:',
            'p_name': 'Product Name:',
            'Brand': 'Brand/Company:',
            'feature': 'Features:',
            'medPerStrip': 'Medicines Per Strip:',
            'p_price': 'Price:',
            'p_discount': 'Discount (%):',
            'description': 'Product Description:',
            'size': 'Size:',
            'Manufacturer': 'Manufacturer:',
            'p_generics': 'Generic Name:',
            'p_type': 'Product Type:',
            'p_image': 'Product Image:',
            'p_Dosage_Strength': 'Dosage Strength:',
            'Variant': 'Variants:',
            'p_category': 'Category:',
            'p_Administration': 'Administration Method:',
            'p_Indications': 'Indications (Uses):',
            'p_Pharmacology': 'Pharmacology:',
            'p_Side_Effects': 'Possible Side Effects:',
            'p_Interaction': 'Drug Interactions:',
            'p_Contradictions': 'Contraindications:',
            'p_Precautions': 'Precautions:',
            'p_Pregnancy': 'Pregnancy Warnings:',
            'p_Therapeutic': 'Therapeutic Class:',
            'p_Storage': 'Storage Instructions:',
            'FAQ': 'Frequently Asked Questions:',
            'Suggestions': 'Suggestions:',
        }

    def __init__(self, *args, **kwargs):
        super(MainMedicineForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.Meta.labels:
                field.label = self.Meta.labels[field_name]


class MainGeneralForm(ModelForm):
    class Meta:
        model = main_product    
        fields = [
            'product_code',
            'p_name',
            'Brand',
            'feature',
            'p_price',
            'p_discount',
            'description',
            'size',
            'm_or_g',
            'Manufacturer',
            'p_type',
            'p_image',
            'Variant',
            'p_category',
            'Features_Specifications',
        ]

        labels = {
            'product_code': 'Product Code:',
            'p_name': 'Product Name:',
            'Brand': 'Brand/Company:',
            'feature': 'Features:',
            'p_price': 'Price:',
            'p_discount': 'Discount (%):',
            'description': 'Product Description:',
            'size': 'Size:',
            'Manufacturer': 'Manufacturer:',
            'p_type': 'Product Type:',
            'p_image': 'Product Image:',
            'Variant': 'Variants:',
            'p_category': 'Category:',
            'Features_Specifications': 'Features & Specifications:',
        }

    def __init__(self, *args, **kwargs):
        super(MainGeneralForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.Meta.labels:
                field.label = self.Meta.labels[field_name]


def create_product(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = MainMedicineForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product created successfully!")
                return redirect('admin_product')
        else:
            form = MainMedicineForm()
        return render(request, 'admin/create_product.html', {'form': form})
    return render(request, 'admin/error.html')

def create_general(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = MainGeneralForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product created successfully!")
                return redirect('admin_product')
        else:
            form = MainGeneralForm()
        return render(request, 'admin/create_general.html', {'form': form})
    return render(request, 'admin/error.html')

def update_product(request, p_id):
    if request.user.is_staff:
        product = get_object_or_404(main_product, p_id=p_id)
        if request.method == 'POST':
            form = MainMedicineForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully!")
                return redirect('admin_product')
        else:
            form = MainMedicineForm(instance=product)
        return render(request, 'admin/update_product.html', {'form': form, 'product': product})
    return render(request, 'admin/error.html')

def update_general(request, p_id):
    if request.user.is_staff:
        product = get_object_or_404(main_product, p_id=p_id)
        if request.method == 'POST':
            form = MainGeneralForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully!")
                return redirect('admin_product')
        else:
            form = MainGeneralForm(instance=product)
        return render(request, 'admin/update_general.html', {'form': form, 'product': product})
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
def medicine(request):
    if request.user.is_staff:
        products = main_product.objects.filter(m_or_g='Medicines')
        return render(request, 'admin/medicines.html', {'products': products})
    else:
        return render(request, 'admin/error.html')
    
def general(request):
    if request.user.is_staff:
        products = main_product.objects.filter(m_or_g='Generals')
        return render(request, 'admin/general.html', {'products': products})
    else:
        return render(request, 'admin/error.html')
