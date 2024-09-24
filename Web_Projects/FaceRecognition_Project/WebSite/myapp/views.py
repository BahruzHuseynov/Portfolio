from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserInfoForm, UserLoginForm
from django.contrib import messages
from .models import UserInfo, User, Student
from .face_actions import face_recognizer, take_photo
from django.contrib.auth.decorators import login_required
# Create your views here.
def common(request):
    return render(request, 'common.html')


def home(request):
    context = {
        "students":Student.objects.all()
    }
    return render(request, 'home.html', context)

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are logged in as {request.user.username}')
        return redirect('myapp:home')
    form1 = UserRegisterForm()
    form2 = UserInfoForm()
    if request.method =="POST":
        form1 = UserRegisterForm(request.POST)
        form2 = UserInfoForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            print(user)
            userinfo = UserInfo(user=user, head_image=form2.cleaned_data.get('head_image'))
            userinfo.save()
            messages.success(request, f'Account created for {user}')
            login(request,user)
            return redirect('myapp:home')     

    context = {
        'form1':form1,
        'form2':form2,
    }
    return render(request,'register.html',context)  


def log_out(request):
    messages.warning(request, 'Logged out')
    logout(request)
    return render(request,'home.html')  

def log_in(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are logged in as {request.user.username}')
        return redirect('myapp:home')
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        print("1----------")
        print(form.get_user())
        if form.is_valid():
            user = form.get_user()
            print(user)
            userinfo = UserInfo.objects.get(user=user)
            print("2----------")
            if face_recognizer(userinfo.head_image.url, user.username):
                login(request, user)
                messages.success(request,f'You are logged in as {user.username}')
                return redirect('myapp:home')
            else:
                login(request, user)
                messages.warning(request,f'Login failed')
                return redirect('myapp:home')

    form = UserLoginForm(request)         
    context = {
        'form':form,
    }
    return render(request, "login.html", context)  

@login_required
def snapshot(request):
    userinfo = UserInfo.objects.get(user=request.user)
    userinfo.head_image = take_photo(request.user.username)
    userinfo.save()
    return render(request,"profile.html")

def reference(request): return render(request,"reference.html")

def register_snapshot(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are logged in as {request.user.username}')
        return redirect('myapp:home')
    form = UserRegisterForm()
    if request.method =="POST":
        form = UserRegisterForm(request.POST)
        print("------------1")
        if form.is_valid():
            print("------------2")
            user = form.save()
            userinfo = UserInfo(user=user)
            userinfo.head_image = take_photo(user.username)
            userinfo.save()
            messages.success(request, f'Account created for {user}')
            login(request,user)
            return redirect('myapp:home')     

    context = {
        'form':form,
    }
    return render(request,'register_snapshot.html',context)  

@login_required
def profile(request, user_id):
    form = UserInfoForm()
    user = User.objects.get(id=user_id)
    if request.method =="POST":
        form = UserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            userinfo = UserInfo.objects.get(user=user)
            x = form.cleaned_data.get("head_image")
            print(x)
            userinfo.head_image = x
            userinfo.save()
            return redirect("myapp:home")     

    context = {
        'form':form,
        'user':user,
    }
    return render(request,'profile.html',context) 


