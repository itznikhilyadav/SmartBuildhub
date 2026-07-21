from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from .forms import ProjectForm
from homeownerapp.models import*
from contractorapp.models import*


# Create your views here.



def homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid
    }
    return render(request,'homeownerdash.html',context)
 
 
def homeownerlogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out")
        return redirect('login')
    
    else:
         return redirect('login')
     
     
     
def homechange_pass(request):
    if 'homeownerid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')  
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            homeowner = Logininfo.objects.get(username=homeownerid)
            if homeowner.password != oldpwd:
                messages.error(request,"Old Password is incorrect")
                return redirect('homechange_pass')
            elif newpwd != confirmpwd:
                messages.error(request,"New password and confirm password dose not match")
                return redirect('homechange_pass')
            elif homeowner.password == newpwd:
                messages.error(request,"New password is same as old password")
                return redirect('homechange_pass')
            else:
                homeowner.password = newpwd
                homeowner.save()
                messages.success(request,"Password changed Successfuly")
                return redirect('homeownerdash')
            
        except Logininfo.DoesNotExist:
            messages.error(request,"Something went wrong")    
            return redirect('login')
        
    
    return render(request,'homechange_pass.html',{'homeownerid':homeownerid})         



def homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner
    }
    return render(request,'homeownerprofile.html',context)



def homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner
    }
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        homeowner.name=name
        homeowner.contactno=contactno
        homeowner.address = address
        homeowner.bio =bio
        if profile:
            homeowner.picture=profile
        homeowner.save()
        messages.success(request, "Your profile has been update" )
        return redirect ('homeownerprofile')
    return render(request,'homeowneredit.html',context)



def addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'form':form
    }
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner
            project.save()
            messages.success(request,"Project has been added")
            return redirect('addproject')
        else:
            messages.error(request,"Invalid form")
            return redirect('addproject')
    return render(request,'addproject.html',context)



def homeownerviewprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects
    }
    return render(request,'homeownerviewprojects.html',context)



def homeownerviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    applications = ContractorApplication.objects.filter(project=project)
    
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'applications':applications,
    }
    return render(request,'homeownerviewapplications.html',context)
 
 
 
     
     
             
        