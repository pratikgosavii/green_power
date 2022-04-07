from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import *


def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)

            
            if user:
                print('yes')
                login(request, user)
                return redirect('dashboard')

            else:

                msg = 'Credentials wrong'


                context = {
                    'msg': msg,
                    'form': forms,
                }
                return render(request, 'users/login.html', context)
        
        else:

           
            context = {
                'form': forms,
                }
            return render(request, 'users/login.html', context)
    context = {'form': forms}
    return render(request, 'users/login.html', context)



def register_page(request):

    forms = registerForm()
    if request.method == 'POST':
        forms = registerForm(request.POST)
        if forms.is_valid():
            forms.save()
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                
                messages.error(request, 'user already exsist')
                messages.success(request, 'sdst')
                return redirect('register')
            else:
                return redirect('register')
        else:

            context = {
                'form': forms,
            }

            return render(request, 'users/resgister.html', context)

    else:
        print(forms.as_p)

        context = {'form': forms}

        return render(request, 'users/resgister.html', context)



def register_distributor(request, username, password):
    
    if not User.objects.filter(username=username).exists():

        test = User.objects.create_user(username=username, password=password, is_distributor = True)

        if test:
            return test
        else:
            messages.error(request, 'something went wrong')
            return redirect('add_distributor')
    
    else:

        messages.error(request, 'username exists')
        return redirect('add_distributor')



def register_showroom(request, username, password):
    
    if not User.objects.filter(username=username).exists():

        test = User.objects.create_user(username=username, password=password, is_showroom = True)

        if test:

            return test

        else:
            messages.error(request, 'something went wrong')
            return redirect('add_showroom')
    
    else:

        messages.error(request, 'username exists')
        return redirect('add_showroom')


def logout_page(request):
    logout(request)
    return redirect('login')
