from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully!')
                else:
                    return HttpResponse('Disabled account :-(')
            else:
                return HttpResponse('Invalid Login ;-(')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet.
            new_user = user_form.save(commit=False)
            # Set the chose password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save user object
            new_user.save()
            return render(request, 'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegisterForm()
    return render(request, 'registration/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user,
                                       data=request.POST)
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST,
                                 files=request.FILES)
        # process and save form cleaned data to database
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Profile updated failed!')
    else:
        profile_form = ProfileEditForm(instance=request.user)
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/edit.html',
                  {'profile_form': profile_form,
                   'user_form': user_form})


