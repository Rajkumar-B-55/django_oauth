from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from app.forms import RegistrationForm, LoginForm
from app.service import UserSvc


def home(request):
    return render(request, 'home.html')


def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['firstname']
                last_name = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Check if the user with the provided email already exists
                user = UserSvc.check_user_exists(email)
                if not user:
                    new_user = UserSvc.add_user(first_name, last_name, email, password)
                    return render(request, 'register_success.html', {'email': email})
                else:
                    return render(request, 'user_exists.html', {'email': email})
        else:
            form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})

    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Check if the user with the provided email already exists
                user = UserSvc.check_user_exists(email)
                if user is not None:
                    is_matched = UserSvc.check_password(password, user.password)

                    if is_matched:
                        return render(request, 'user_profile.html', {'user_data': user})
                    else:
                        return render(request, 'user_exists.html', {"fromlogin": " "})
                else:
                    return redirect(home)
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def register_template(request):
    try:
        return render(request, 'signup.html')
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def logout(request):
    try:
        if request:
            request.session.clear()
            auth.logout(request)
        return redirect(home)
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})
