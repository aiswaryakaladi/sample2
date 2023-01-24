from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .forms import *
from .models import *
from django.core.mail import send_mail
from emal.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.contrib import messages
import uuid

# Create your views here.

def reg(request):
    a=register()
    return render(request,'register.html',{'form':a})

def emailsend(request):
    b=contactusForm()
    if request.method=='POST':
        sub=contactusForm(request.POST)
        if sub.is_valid():
            nm=sub.cleaned_data['Name']
            em=sub.cleaned_data['Email']
            ms=sub.cleaned_data['Message']
            send_mail(str(nm)+"||"+"Wipro-elite",ms,EMAIL_HOST_USER,[em])
            return render(request,"success.html")
    #         send_mail(subject,message,EMAIL_HOST_USER,[EMAIL]
    return render(request,'contactus.html',{'form':b})


def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).first():
             messages.success(request,'username already taken')
             return redirect(login)
        if User.objects.filter(email=email).first():
            messages.success(request,'email already exist')
            return redirect(login)

        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()

        auth_token=str(uuid.uuid4())

        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()

        send_mail_login(email,auth_token)
        return render(request,'success.html')
    return render(request,'login.html')



def send_mail_login(email,auth_token):
    subject="Your account has been verified"
    message=f'paste the link to verify your account  http://127.0.0.1:8000/emalapp/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)


def verify(request,auth_token):
    profile_obj= profile.objects.filter(auth_token=auth_token).first()
    if profile_obj: #if true

        if profile_obj.is_verified: #if profile object is false
            messages.success(request,'Your account is already verified')
            return redirect(loginpage)

        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(loginpage)
    else:

        messages.success(request,'user not found')
        return redirect(loginpage)



def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password= request.POST.get('password')

        user_obj=User.objects.filter(username=username).first()

        if user_obj is None: #if user doesnot exist
            messages.success(request,'user not found')
            return redirect(login)

        profile_obj =profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified: #if not profile is false
            messages.success(request,'profile not verified check your mail')
            return redirect(loginpage)

        user=authenticate(username=username,password=password)
        #user is valid

        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(loginpage)

        return HttpResponse("success")

    return render(request,'loginpage.html')






















