"""
URL configuration for medE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from Home import views as  firstactivity
from products import views as  secondactivity
from django.conf import settings
from django.conf.urls.static import static

from authentication import views as authenticationViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',firstactivity.home, name='home'),
    path('product/<str:p_name>/', secondactivity.prod, name='prod'),
    path("Category<str:p_category>/",secondactivity.category,name='category'),
    path('live_search/', secondactivity.live_search, name='live_search'),
    path('get_product_info/<int:p_id>/', secondactivity.get_product_info, name='get_product_info'),
    path('send_otp/', authenticationViews.send_otp, name='send_otp'),
    path('verify_otp/', authenticationViews.verify_otp, name='verify_otp'),
    path('verify_forgot_password_otp/', authenticationViews.verify_forgot_password_otp, name='verify_forgot_password_otp'),
    path('login/', authenticationViews.mylogin, name='mylogin'),
    path('forgot_password/', authenticationViews.forgotPassword, name='forgotpassword'),
    path('register/', authenticationViews.myregister, name='myregister'),
    path('logout/', authenticationViews.mylogout, name='mylogout'),
    path('profile/',firstactivity.profile, name='profile'),
    path('profile/update_profile/', authenticationViews.update_profile, name='update_profile'),
    path('product/<str:p_name>/', secondactivity.prod, name='prod'),
    path('order_confirm/',secondactivity.order_confirm, name='order_confirm'),
    path('checkout/', secondactivity.checkout_view, name='checkout'),
    path('confirm/', secondactivity.order_complete, name='confirm'),
    path('save_med_list/', secondactivity.save_med_list, name='save_med_list'),
    path('remove_productList/<int:product_id>/', secondactivity.remove_productList, name='remove_productList'),
    path('quickorder/',firstactivity.quick_order, name='quickorder'),
    path('upload_prescription/',firstactivity.upload_prescription, name='upload_prescription'),
    path('prescription_confirm/', secondactivity.pres_confirm, name='prescription_confirm'),
    path('prescriptions_order/', secondactivity.presciptions_order, name='presciptions_order'),
    path('searchresult/', firstactivity.searchresult, name='search_results'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)