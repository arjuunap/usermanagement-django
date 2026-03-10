from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
# Create your views here


@cache_control(no_cache=True,no_store=True,must_revalidate=True)
@login_required(login_url='user:login') 
def home(request):
    return render(request,'user/home.html')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username = email ,password = password)
        print(user)
        
            
        if user is not None:
            if  user.is_blocked:
                messages.error(request,"You are blocked from admin")
                return redirect("user:login")
            print(user)
            login(request,user)
            return redirect('user:home')
        else:
            messages.error(request,"Invalid email or password")
            return redirect('user:login')
    return render(request,'user/login.html')


from . forms import SignupForm
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = SignupForm()
    return render(request,'user/signup.html',{"form":form})




def logout_view(request):
    logout(request)
    # messages.success(request,"logout successfully")
    return redirect("user:login")