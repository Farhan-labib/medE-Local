# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from twilio.rest import Client
import random
from django.conf import settings  # Import Django settings module
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile  # Import your UserProfile model
from django.contrib.auth.decorators import login_required
from products.models import Orders
import ast
from products.models import Profile_MedList
from products.models import presciption_order
from custom_admin.models import TemporaryOrders, Location

def mylogin(request):
    if request.method == 'POST':
        phone_number = '+880'+request.POST.get('phone_number')
        password = request.POST.get('password')

        # Retrieve user profile based on phone number
        user_profile = UserProfile.objects.filter(phone_number=phone_number).first()

        print(user_profile)  # Debug: Print user_profile to check if it's retrieved correctly

        if user_profile is not None and check_password(password, user_profile.password):
            # Password matches, log the user in
            user = authenticate(request, username=phone_number, password=password)
            print(user)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
        elif user_profile is None:
            # User authentication failed, show error message
            messages.error(request, 'Invalid phone number.')
            return redirect('mylogin')  # Redirect back to the login page if authentication fails
        else:
            # User authentication failed, show error message
            messages.error(request, 'Incorrect password, please try again.')
            return redirect('mylogin')

    return render(request, 'login.html')


from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import UserProfile  # Import your user profile model
def signup(request):
     
     phone_number = request.session.get('phone_number')
     if request.method == 'POST':
         password = request.POST.get('password')
         c_password=request.POST.get('c_password')
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')

            # Hash the password
         if(password==c_password):
            hashed_password = make_password(password)

            # Check if a user profile with the given phone number already exists
            user_profile, created = UserProfile.objects.get_or_create(
                phone_number=phone_number,
                defaults={'password': hashed_password},
                first_name=first_name,
                last_name=last_name,
            )
            del request.session['otp']
            del request.session['phone_number']
            return render(request,'login.html')
         else:
            messages.error(request, 'Passwords do not match.')
        
         return render(request, 'register2.html')


            


def verify_otp(request):
    print("Getting here")
    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        user_otp = otp1 + otp2 + otp3 + otp4
        stored_otp = request.session.get('otp')
      
        # print(user_otp, stored_otp , phone_number)
        if user_otp == stored_otp:

            messages.success(request, 'OTP verified successfully!')
            return render(request,'register2.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('myregister')  # Redirect back to the registration page if OTP is invalid




def verify_forgot_password_otp(request):
    if request.method == 'POST':
        if request.method == 'POST':
            otp1 = request.POST.get('otp1')
            otp2 = request.POST.get('otp2')
            otp3 = request.POST.get('otp3')
            otp4 = request.POST.get('otp4')
            user_otp = otp1 + otp2 + otp3 + otp4
            stored_otp = request.session.get('otp')

       
            if user_otp == stored_otp:

                messages.success(request, 'OTP verified successfully!')
                return render(request,'forgot_pass2.html')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('forgotpassword')  # Redirect back to the registration page if OTP is invalid

    # Handle GET requests (if any) here
    return render(request, 'authentication/forgot_password.html')

def forgot_pass2(request):
    phone_number = request.session.get('phone_number')
    if request.method == 'POST':
        password = request.POST.get('password')
        c_password=request.POST.get('c_password')
        if(password==c_password):
            hashed_password = make_password(password)
            # Retrieve the user profile with the given phone number
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            # Update the user's password
            user_profile.password = hashed_password
            user_profile.save()

            # Clear the OTP data from the session
            del request.session['otp']
            del request.session['phone_number']

            messages.success(request, 'Password changed successfully!')
            return redirect('mylogin')  # Redirect to the login page after changing the password
        else:
            messages.error(request, 'Passwords do not match.')  
    return render(request, 'forgot_pass2.html')

def myregister(request):
    return render(request, 'register.html')


def forgotPassword(request):
    return render(request, 'forgot_password.html')

# def send_otp(request):
#     if request.method == 'POST':
#         phone_number = '+880'+request.POST.get('phone_number')
#         otp = str(random.randint(1000, 9999))  # Generate a random 4-digit OTP

#         # Send the OTP via Twilio
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         message = client.messages.create(
#             body=f'Your OTP is: {otp}',
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=phone_number
#         )

#         # Store the OTP in session for verification
#         request.session['otp'] = otp
#         request.session['phone_number'] = phone_number
#         print(otp)
#         return HttpResponse("OTP sent successfully")


from twilio.base.exceptions import TwilioRestException
from django.http import HttpResponse, JsonResponse
from django.conf import settings

def send_otp(request):
    if request.method == 'POST':
        phone_number = '+880' + request.POST.get('phone_number')
        otp = str(random.randint(1000, 9999))  # Generate a random 4-digit OTP

        try:
            # Send the OTP via Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your OTP is: {otp}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            # Store the OTP in session for verification
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            print(f"OTP sent successfully to {phone_number}, otp: {otp}")
            return render(request, 'register.html', {'phone_number':phone_number,'message': "OTP Sent Successfully"})
            # return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})
        except TwilioRestException as e:
            # Log the error or handle it appropriately
            print(f"Twilio Error: {e}")
            return render(request, 'register.html', {'phone_number':phone_number, 'message': 'Failed to send OTP. Please try again'})
    return HttpResponse("Invalid request method")
def send_forgot_otp(request):
    if request.method == 'POST':
        phone_number = '+880' + request.POST.get('phone_number')
        otp = str(random.randint(1000, 9999))  # Generate a random 4-digit OTP
        try:
            # Send the OTP via Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your OTP is: {otp}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            # Store the OTP in session for verification
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            print(f"OTP sent successfully to {phone_number}, otp: {otp}")
            return render(request, 'forgot_password.html', {'phone_number':phone_number,'message': "OTP Sent Successfully"})
            # return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})
        except TwilioRestException as e:
            # Log the error or handle it appropriately
            print(f"Twilio Error: {e}")
            return render(request, 'forgot_password.html', {'phone_number':phone_number, 'message': 'Failed to send OTP. Please try again'})
    return HttpResponse("Invalid request method")

def mylogout(request):
    logout(request)
    return redirect('home')




@login_required
def update_profile(request):
    if request.method == 'POST':
        # print(request.POST)
        # Extract form values from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Update user profile
        user_profile = request.user
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.dob = dob
        user_profile.gender = gender
        user_profile.email = email
        user_profile.address = address
        # print("Before save:", user_profile.first_name)  # Check user profile data before saving
        user_profile.save()
        # print("After save:", user_profile.first_name)  # Check user profile data after saving

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
        for item in data:
            name, number, _ = item
            d.append(str(name + "X" + number))
        
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