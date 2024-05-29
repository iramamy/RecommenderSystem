from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import UserRegisterForm
from .models import UserAccount




def explore(request):
    context = {
        'range_list': range(6),
        'range_list_1': range(12)
    }

    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']

            messages.success(request, "Your account has been created!")
            new_user = auth.authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
                )
            auth.login(request, new_user)

            return redirect('explore')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user_accounts/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('explore')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(
            request, 
            email=email, 
            password=password
            )

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in!')

            return redirect('explore')
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'user_accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out!')

    return redirect('login')
