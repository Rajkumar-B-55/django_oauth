import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth

from app.forms import RegistrationForm, LoginForm
from app.service import UserSvc
from app.google_svc import GoogleSvc

from app.linkedin_svc import LinkedinSvc


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
            request.session.pop('linkedin_token', None)
            auth.logout(request)
        return redirect(home)
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def google_signin(request):
    try:
        auth_url = GoogleSvc.login()
        if auth_url is not None:
            return redirect(auth_url)
        return Exception
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def google_signup(request):
    try:
        auth_url = GoogleSvc.login()
        if auth_url is not None:
            return redirect(auth_url)
        return Exception
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def google_callback(request):
    try:
        code = request.GET.get("code")
        response = GoogleSvc.callback(code)

        request.session["google_id"] = response.get("sub")
        request.session['first_name'] = response.get('given_name')
        request.session['family_name'] = response.get('family_name')
        request.session['email'] = response.get('email')

        email = response['email']
        user_exists = UserSvc.check_user_exists(email)
        if not user_exists:
            user_dict_google = {
                'first_name': response['given_name'],
                'last_name': response['family_name'],
                'email': response['email']
            }

            new_user = UserSvc.add_user(user_dict_google['first_name'], user_dict_google['last_name'],
                                        user_dict_google['email'], password='google_admin')
            return redirect(protected_area)
        else:
            return redirect(protected_area)
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


@GoogleSvc.login_is_required
def protected_area(request):
    try:
        if request.session:
            user_data = {
                'first_name': request.session['first_name'],
                'last_name': request.session['family_name'],
                'email': request.session['email']
            }
            return render(request, 'user_profile.html', {'user_data': user_data})
        else:
            raise Exception
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def linkedin_signin(request):
    try:
        if request.session.get('linkedin_token') is not None:
            request.session.pop('linkedin_token', None)
            return redirect(home)
        else:
            return redirect(linkedin_login)
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def linkedin_signup(request):
    try:
        if request.session.get('linkedin_token') is not None:
            request.session.pop('linkedin_token', None)
            return redirect(home)
        else:
            return redirect(home)
    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def linkedin_login(request):
    try:
        resp = LinkedinSvc.auth_code()
        return redirect(resp)

    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})


def linkedin_authorize(request):
    try:
        auth_code = request.GET.get('code')
        if auth_code is None:
            return JsonResponse({'error': 'Access denied'})
        # method for profile
        resp = LinkedinSvc.profile_api(auth_code)
        resp = resp.json()
        access_token = resp['access_token']

        headers = {
            'Authorization': f'Bearer {access_token}',
            'cache-control': 'no-cache',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        me_url = LinkedinSvc.base_url + 'userinfo'

        my_profile = requests.request('GET', url=me_url, headers=headers, data={})
        if my_profile.status_code == 200:
            my_profile = my_profile.json()
            email = my_profile['email']
            first_name = my_profile['given_name']
            last_name = my_profile['family_name']
            user_exists = UserSvc.check_user_exists(email)
            if not user_exists:
                new_user = UserSvc.add_user(
                    firstname=first_name,
                    lastname=last_name,
                    email=email,
                    password="linkedin_admin"
                )
                return render(request, 'register_success.html', {'email': email})
            else:
                user_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
                return render(request, 'user_profile.html', {'user_data': user_data})

    except Exception as e:
        return JsonResponse({'error': str(e.args[0])})
