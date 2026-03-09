from django.shortcuts import render,redirect,get_object_or_404
from user.models import Custom_user
from django.contrib.auth import logout,login,authenticate
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
@login_required(login_url='adminpanel:login')
def admin_panel(request):
    
    users = Custom_user.objects.all()
    return render(request,'adminpanel/admin_panel.html',{'users':users})


@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,username = email ,password = password)
        print("USER:", user)

        if user is not None and user.is_superuser:
           
            # print(user)
            login(request,user)
            return redirect('adminpanel:admin-panel')
    return render(request,'adminpanel/admin_login.html')





@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def admin_logout(request):
    logout(request)
    return redirect('adminpanel:login')

from django.contrib import messages

def edit_user(request,id):
    user = get_object_or_404(Custom_user,id=id)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        if not username or not email:
            messages.error(request,"All fields are required")
            return redirect("adminpanel:edit-user",id=id)
        if Custom_user.objects.exclude(id=id).filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect("adminpanel:edit-user",id=id)
        if Custom_user.objects.exclude(id=id).filter(username=username).exists():
            messages.error(request,"Username aleady taken")
            return redirect("adminpanel:edit-user",id=id)
        
        user.username = username
        user.email = email
        user.save()

        return redirect("adminpanel:admin-panel")

    return render(request,"adminpanel/edit_user.html",{"user":user})