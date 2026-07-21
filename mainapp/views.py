from django.shortcuts import render ,redirect
from . models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

def project(request):
    return render(request,'project.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request, 'services.html') 

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            log=Logininfo.objects.get(username=username,password=password)
            if log is not None:
                if log.usertype.lower() == "homeowner":
                    request.session['homeownerid']=username
                    messages.success(request,"Welcome Homeowner")
                    return redirect('homeownerdash')
                elif log.usertype.lower() == "contractor":
                    request.session['contractorid']=username
                    messages.success(request,"Welcome Contractor")
                    return redirect('contractordash')
                else:
                    messages.error(request,"something went wrong")
                    return redirect('login')
            
        except Logininfo.DoesNotExist:    
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'login.html')

def register(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        usertype=request.POST.get('usertype')
        password=request.POST.get('password')
        u=Logininfo.objects.filter(username=email)
        if u:
            messages.error(request,"Email already exists")
            return redirect('register')
        log=Logininfo(usertype=usertype,username=email,password=password)
        user = UserInfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"You are Registerd")
        return redirect('register')
    return render(request,'register.html')

def adminlogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ad=Logininfo.objects.get(username=username,password=password)
            if ad is not None:
                request.session['adminid']=username
                messages.success(request,"Welcome Admin")
                return redirect('admindash')
        except Logininfo.DoesNotExist:
            messages.success(request,"Invalid Username or Password")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')

def contact(request):
    if request.method == 'POST':
       name=request.POST.get('name')
       email = request.POST.get('email')
       contactno = request.POST.get('contactno')
       subjact = request.POST.get('subjact')
       message = request.POST.get('message')
       enq = enquiry(name=name,email=email,contactno=contactno,subject=subjact,message=message)
       enq.save()
       messages.success(request,"Your enquary has been submitted successfully")
       
       return redirect('contact')
    return render(request,'contact.html')


