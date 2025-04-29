from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import random
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from products.models import Orders, Profile_MedList, presciption_order
from custom_admin.models import TemporaryOrders, Location
import ast

def mylogin(request):
    if request.method == 'POST':
        phone_number = '+880' + request.POST.get('phone_number')
        password = request.POST.get('password')
        user_profile = UserProfile.objects.filter(phone_number=phone_number).first()

        if user_profile is not None and check_password(password, user_profile.password):
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        elif user_profile is None:
            messages.error(request, 'Invalid phone number.')
            return redirect('mylogin')
        else:
            messages.error(request, 'Incorrect password, please try again.')
            return redirect('mylogin')

    return render(request, 'login.html')

def signup(request):
    phone_number = request.session.get('phone_number')
    if request.method == 'POST':
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password == c_password:
            hashed_password = make_password(password)
            UserProfile.objects.get_or_create(
                phone_number=phone_number,
                defaults={'password': hashed_password},
                first_name=first_name,
                last_name=last_name,
            )
            del request.session['otp']
            del request.session['phone_number']
            return render(request, 'login.html')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'register2.html')

def verify_otp(request):
    if request.method == 'POST':
        otp1, otp2, otp3, otp4 = [request.POST.get(f'otp{i}') for i in range(1, 5)]
        user_otp = otp1 + otp2 + otp3 + otp4
        stored_otp = request.session.get('otp')
      
        if user_otp == stored_otp:
            messages.success(request, 'OTP verified successfully!')
            return render(request, 'register2.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('myregister')

def verify_forgot_password_otp(request):
    if request.method == 'POST':
        otp1, otp2, otp3, otp4 = [request.POST.get(f'otp{i}') for i in range(1, 5)]
        user_otp = otp1 + otp2 + otp3 + otp4
        stored_otp = request.session.get('otp')
   
        if user_otp == stored_otp:
            messages.success(request, 'OTP verified successfully!')
            return render(request, 'forgot_pass2.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('forgotpassword')

    return render(request, 'authentication/forgot_password.html')

def forgot_pass2(request):
    phone_number = request.session.get('phone_number')
    if request.method == 'POST':
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password == c_password:
            hashed_password = make_password(password)
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            user_profile.password = hashed_password
            user_profile.save()

            del request.session['otp']
            del request.session['phone_number']

            messages.success(request, 'Password changed successfully!')
            return redirect('mylogin')
        else:
            messages.error(request, 'Passwords do not match.')  
    return render(request, 'forgot_pass2.html')

def myregister(request):
    return render(request, 'register.html')

def forgotPassword(request):
    return render(request, 'forgot_password.html')

def send_otp(request):
    if request.method == 'POST':
        phone_number = '+880' + request.POST.get('phone_number')
        otp = str(random.randint(1000, 9999))

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f'Your OTP is: {otp}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            return render(request, 'register.html', {'phone_number': phone_number, 'message': "OTP Sent Successfully"})
        except TwilioRestException:
            return render(request, 'register.html', {'phone_number': phone_number, 'message': 'Failed to send OTP. Please try again'})
    return HttpResponse("Invalid request method")

def send_forgot_otp(request):
    if request.method == 'POST':
        phone_number = '+880' + request.POST.get('phone_number')
        otp = str(random.randint(1000, 9999))
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f'Your OTP is: {otp}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            return render(request, 'forgot_password.html', {'phone_number': phone_number, 'message': "OTP Sent Successfully"})
        except TwilioRestException:
            return render(request, 'forgot_password.html', {'phone_number': phone_number, 'message': 'Failed to send OTP. Please try again'})
    return HttpResponse("Invalid request method")

def mylogout(request):
    logout(request)
    return redirect('home')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_profile = request.user
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.dob = request.POST.get('dob')
        user_profile.gender = request.POST.get('gender')
        user_profile.email = request.POST.get('email')
        user_profile.address = request.POST.get('address')
        user_profile.save()

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
        for item in data:
            try:
                if len(item) == 3:
                    name, number, _ = item
                    d.append(f"{name}X{number}")
                else:
                    name, number, unit, price = item
                    d.append(f"{name}X{number} ({unit} - {price})")
            except ValueError:
                continue

        orders_data[i.id] = [d, i.total, i.timestamp, i.status]
    
    # Process TemporaryOrders data
    temp_orders_data = {}
    for i in temp_orders:
        d = []
        data = ast.literal_eval(i.ordered_products)
        for item in data:
            name, number, _ = item
            d.append(f"{name}X{number}")
        
        temp_orders_data[i.id] = [d, i.total, i.timestamp, i.status, True]
    
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