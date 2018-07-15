from django.shortcuts import render
from basic.forms import UserProfileForm,UserForm

from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,'basic/index.html')

@login_required
def special_page(request):
    return HttpResponse('Login Successful')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Wrong User Login Attempt:')
            print('Username: {} Password: {}'.format(username,password))
            return HttpResponse('Invalid Credentials')

    else:
        return render(request,'basic/login.html')

def register(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
                profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    return render(request,'basic/register.html',context={'user_form':user_form,'profile_form':profile_form,'registered':registered})
