from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from homeownerapp.models import*
from.models import*
from decimal import Decimal

# Create your views here.
def contractordash(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid
    }
    return render(request,'contractordash.html',context)


def contractorlogout(request):
    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('login')
    
    else:
         return redirect('login')
     
def contractorchangepass(request):
    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')  
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            contractor = Logininfo.objects.get(username=contractorid)
            if contractor.password != oldpwd:
                messages.error(request,"Old Password is incorrect")
                return redirect('contractorchangepass')
            elif newpwd != confirmpwd:
                messages.error(request,"New password and confirm password dose not match")
                return redirect('contractorchangepass')
            elif contractor.password == newpwd:
                messages.error(request,"New password is same as old password")
                return redirect('contractorchangepass')
            else:
                contractor.password = newpwd
                contractor.save()
                messages.success(request,"Password changed Successfuly")
                return redirect('contractordash')
            
        except Logininfo.DoesNotExist:
            messages.error(request,"Something went wrong")    
            return redirect('login')
        
    
    return render(request,'contractorchangepass.html',{'contractorid':contractorid})      



def contractorprofile(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor
    }
    return render(request,'contractorprofile.html',context)  



def contractoredit(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor
    }
    
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        contractor.name=name
        contractor.contactno=contactno
        contractor.address = address
        contractor.bio =bio
        if profile:
            contractor.picture=profile
        contractor.save()
        messages.success(request, "Your profile has been update" )
        return redirect ('contractorprofile')
    return render(request,'contractoredit.html',context)       



def contractorviewprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=None)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects
    }
    return render(request,'contractorviewprojects.html',context)



def applyproject(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project
    }
    application = ContractorApplication.objects.filter(project=project,contractor=contractor)
    if application.exists():
        messages.warning(request,"You have alredy applid for Project")
        return redirect('contractorviewprojects')
    if request.method == 'POST':
        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget_str = request.POST.get('estimated_budget')
        estimated_duration = request.POST.get('estimated_duration')
        try:
            estimated_budget = Decimal(estimated_budget_str)
        except:
            messages.error(request,"Invalid estimated budget")
            return redirect('contractorviewprojects')
        app = ContractorApplication(
            contractor=contractor,
            project=project,
            proposal_text=proposal_text,
            design_file=design_file,
            estimated_budget=estimated_budget,
            estimated_duration=estimated_duration
        )
        app.save()
        messages.success(request,"Project Application Successfully")
        return redirect('contractorviewprojects')
    return render(request,'applyproject.html',context)


def contractorapplications(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    applications = ContractorApplication.objects.filter(contractor=contractor)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'applications':applications
    }
    return render(request,'contractorapplications.html',context)







        