from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import* 


# Create your views here.
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    return render(request,'admindash.html')

def adminlogout(request):
    if 'adminid'in request.session:
        del request.session['adminid']
        messages.success(request,'You are logged out')
        return redirect('adminlogin')
    else:
        return redirect('index')
    
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    enqs=enquiry.objects.all()
    return render(request,'viewenq.html', {'enq':enqs,'adminid':adminid})    

def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enq = enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,"Enquary Deleted Successfully")
    return redirect('viewenq')

def change_password(request):
    if 'adminid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')  
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = Logininfo.objects.get(username=adminid)
            if admin.password != oldpwd:
                messages.error(request,"Old Password is incorrect")
                return redirect('change_password')
            elif newpwd != confirmpwd:
                messages.error(request,"New password and confirm password dose not match")
                return redirect('change_password')
            elif admin.password == newpwd:
                messages.error(request,"New password is same as old password")
                return redirect('change_password')
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request,"Password changed Successfuly")
                return redirect('admindash')
            
        except Logininfo.DoesNotExist:
            messages.error(request,"Something went wrong")    
            return redirect('adminlogin')
        
    
    return render(request,'change_password.html',{'adminid':adminid})        


def managecontractors(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    contractors = UserInfo.objects.filter(login__usertype='contractor')
    return render(request,'managecontractors.html',{'adminid':adminid,'contractors':contractors})


def managehomeowners(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    homeowners = UserInfo.objects.filter(login__usertype='homeowner')
    return render(request,'managehomeowners.html',{'adminid':adminid,'homeowners':homeowners})