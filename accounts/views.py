from django.shortcuts import render,redirect
from .forms import LoginForm, RegistrationForm, GestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.http import is_safe_url
from .models import GuestEmail
from django.http import HttpResponse

def guest_register_page(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_url = next_ or next_post or '/'
    form_g = GestForm(request.POST or None)
    if form_g.is_valid():
        email = form_g.cleaned_data.get("email")

        new_guest_email = GuestEmail.objects.create(email=email)
        request.session["guest_email_id"] = new_guest_email.id
        if is_safe_url(request_url, request.get_host()):
            return redirect(request_url)
        else:
            return redirect('/login/')
    return redirect('/login/')

def login_page(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_url = next_ or next_post or '/'
    '''if request.user.is_authenticated:
        return redirect(request_url)'''
    form_l = LoginForm(request.POST or None)
    form_r = RegistrationForm(request.POST or None)
    action_type = request.POST.get("action_type")
    if (action_type == "registration"):
        context = {"form_login": form_l, "form_registration": form_r, "s_active": "registration"}
        if form_r.is_valid():
            username = form_r.cleaned_data.get("username")
            password = form_r.cleaned_data.get("password")
            email = form_r.cleaned_data.get("email")
            new_user = User.objects.create_user(username, email, password)
            if is_safe_url(request_url, request.get_host()):
                return redirect(request_url)
            else:
                return redirect('/')
        return render(request, 'accounts/login.html', context)
    else:
        context = {"form_login": form_l, "form_registration": form_r, "s_active": "login"}
        if form_l.is_valid():
            print("form is validated")

            username = form_l.cleaned_data.get("username")
            password = form_l.cleaned_data.get("password")
            user = authenticate(request, username=username,
                                password=password)
            #print(request.user.is_authenticated)
            if user is not None:
                #print(user)
                login(request, user)
                try:
                    del request.session["guest_email_id"]
                except:
                    pass
                context['form_login'] = LoginForm()
                if is_safe_url(request_url, request.get_host()):
                    return redirect(request_url)
                else:
                    return redirect('/')
            else:
                print("Error")

        return render(request, 'accounts/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')