from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login as logs, logout, update_session_auth_hash
from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm
from .models import MyRegistration
from .forms import MyRegistrationForm, ProfileForm, AdminProfileForm, LoginForm, ChangePassword
from django.contrib import messages

#Registration Form
# def signup(request):
#     if request.user.is_authenticated:
#         if request.method=='POST':
#             if request.POST.get('password1')==request.POST.get('password2'):
#                 try:
#                     MyRegistration.objects.get(username=request.POST.get('username'))
#                     fm=MyRegistrationForm()
#                     return render (request, 'account/signup.html', {'error':'This username already exists!', 'form':fm})
#                 except MyRegistration.DoesNotExist:
#                     MyRegistration.objects.create_user(first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     username=request.POST.get('username'),
#                     email=request.POST.get('email'),
#                     location=request.POST.get('location'),
#                     designation=request.POST.get('designation'),
#                     password=request.POST.get('password1'))
#                     messages.success(request, 'Registered successfully!!')
#             fm=MyRegistrationForm()
#             cur_user=request.user
#             return render(request, 'account/signup.html', {'form':fm, 'cur_user':cur_user})
#         else:
#             fm=MyRegistrationForm()
#             cur_user=request.user
#             return render(request, 'account/signup.html', {'form':fm, 'cur_user':cur_user})
#     else:
#         return HttpResponseRedirect('/')

def signup(request):
    print('1')
    if request.user.is_authenticated:
        print('2')
        if request.method=='POST':
            print('3')
            if request.POST.get('password1')==request.POST.get('password2'):
                print('4')
                fm=MyRegistrationForm(request.POST)
                for field in fm:
                    print("Field Error:", field.name,  field.errors)
                if fm.is_valid():
                    print('6')
                    fm.save()
                    messages.success(request, 'Registered successfully!!')
                    fm=MyRegistrationForm()
                print('7')
                cur_user=request.user
                return render(request, 'account/signup.html', {'form':fm, 'cur_user':cur_user})
        else:
            fm=MyRegistrationForm()
            cur_user=request.user
            return render(request, 'account/signup.html', {'form':fm, 'cur_user':cur_user})
    else:
        return HttpResponseRedirect('/')


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            print('request.post: ', request.POST)
            print('request: ', request)
            fm=AuthenticationForm(request=request, data=request.POST)
            print('fm: ', fm)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                print(uname, upass)
                user = authenticate(username=uname, password=upass)
                if user is not None and user.is_active:
                    if user.location=="Dhule":
                        print(user)
                        logs(request, user)
                        messages.success(request, 'Logged in successfully !!')
                        return HttpResponseRedirect('/account/dhulehome/')
                    elif user.location=="Solapur":
                        print(user)
                        logs(request, user)
                        messages.success(request, 'Logged in successfully !!')
                        return HttpResponseRedirect('/account/solapurhome/')
                    elif user.location=="Other":
                        print(user)
                        logs(request, user)
                        messages.success(request, 'Logged in successfully !!')
                        return HttpResponseRedirect('/account/adminhome/')
                else:
                    return HttpResponse('Not validated!')
            else:
                fm = LoginForm()
                messages.warning(request, 'Wrong Email Address or Password!')
                context={'form':fm}
                return render(request, 'account/login.html', context)
        else:
            fm = LoginForm()
            context={'form':fm}
            return render(request, 'account/login.html', context)
    else:
        if request.user.location=="Dhule":
            return HttpResponseRedirect('/account/dhulehome/')
        elif request.user.location=="Solapur":
            return HttpResponseRedirect('/account/solapurhome/')
        elif request.user.location=="Other":
            return HttpResponseRedirect('/account/adminhome/')

# Dhule home

def dhule_home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print('aaya!')
            if request.user.is_superuser == True:
                print('reuest.post: ',request.POST)
                fm = AdminProfileForm(request.POST, instance=request.user)
                print('0')
                users = MyRegistration.objects.all()
                print('1')
                for field in fm:
                    print("Field Error:", field.name,  field.errors)
            else:
                print('2')
                fm = ProfileForm(request.POST, instance=request.user)
                users = None
            if fm.is_valid():
                print('3')
                messages.success(request, 'Profile Updated !!!')
                fm.save()
            else:
                print('4')
        else:
            if request.user.is_superuser == True:
                fm = AdminProfileForm(instance=request.user)
                users = MyRegistration.objects.all()
            else:
                fm = ProfileForm(instance=request.user)
                users = None
        return render(request, 'account/dhule_home.html', {'name':request.user, 'form':fm, 'users':users})
    else:
        return HttpResponseRedirect('/')

# Solapur Home

def solapur_home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = AdminProfileForm(request.POST, instance=request.user)
                users = MyRegistration.objects.all()
                for field in fm:
                    print("Field Error:", field.name,  field.errors)
            else:
                fm = ProfileForm(request.POST, instance=request.user)
                users = None
            if fm.is_valid():
                messages.success(request, 'Profile Updated !!!')
                fm.save()
        else:
            if request.user.is_superuser == True:
                fm = AdminProfileForm(instance=request.user)
                users = MyRegistration.objects.all()
            else:
                fm = ProfileForm(instance=request.user)
                users = None
        return render(request, 'account/solapur_home.html', {'name':request.user, 'form':fm, 'users':users})
    else:
        return HttpResponseRedirect('/')

#Admin Home

def admin_home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = AdminProfileForm(request.POST, instance=request.user)
                users = MyRegistration.objects.all()
            else:
                fm = ProfileForm(request.POST, instance=request.user)
                users = None
            if fm.is_valid():
                messages.success(request, 'Profile Updated !!!')
                fm.save()
        else:
            if request.user.is_superuser == True:
                fm = AdminProfileForm(instance=request.user)
                users = MyRegistration.objects.all()
            else:
                fm = ProfileForm(instance=request.user)
                users = None
        return render(request, 'account/admin_home.html', {'name':request.user, 'form':fm, 'users':users})
    else:
        return HttpResponseRedirect('/')

# Logout

def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')

# Change Password without old Password
def passchange(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = ChangePassword(user=request.user, data=request.POST)
            # print('fm ka value: ', fm)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Changed Successfully')
                if request.user.location=="Dhule":
                    return HttpResponseRedirect('/account/dhulehome/')
                elif request.user.location=="Solapur":
                    return HttpResponseRedirect('/account/solapurhome/')
                elif request.user.location=="Other":
                    return HttpResponseRedirect('/account/adminhome/')
            else:
                messages.warning(request, 'Password should be strong!')
                for field in fm:
                    print("Field Error:", field.name,  field.errors)
                fm=ChangePassword(user=request.user)
                cur_user=request.user
                return render(request, 'account/passchange.html', {'form':fm, 'cur_user':cur_user})
        else:
            fm=ChangePassword(user=request.user)
            cur_user=request.user
            return render(request, 'account/passchange.html', {'form':fm, 'cur_user':cur_user})
    else:
        return HttpResponseRedirect('/')

#User Details

def user_detail(request, id):
  if request.user.is_authenticated:
    if request.method=='POST':
        print(request.POST)
        pi = MyRegistration.objects.get(pk=id)
        print(pi)
        fm=AdminProfileForm(request.POST, instance=pi)
        print(fm)
        if fm.is_valid():
            fm.save()
        pi = MyRegistration.objects.get(pk=id)
        fm = AdminProfileForm(instance=pi)
        users = MyRegistration.objects.all()
        cur_user=request.user
        messages.success(request, 'Changes made successfully')
        return render(request, 'account/userdetail.html', {'form':fm, 'users':users, 'cur_user':cur_user})
    else:
        pi = MyRegistration.objects.get(pk=id)
        fm = AdminProfileForm(instance=pi)
        users = MyRegistration.objects.all()
        cur_user=request.user
        return render(request, 'account/userdetail.html', {'form':fm, 'users':users, 'cur_user':cur_user})
  else:
    return HttpResponseRedirect('/')