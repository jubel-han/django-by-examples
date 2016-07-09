from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
from .models import Contact


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
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    follow_ids = request.user.following.values_list('id', flat=True)

    if follow_ids:
        actions = actions.filter(user_id__in=follow_ids)\
                         .select_related('user', 'user__profile')\
                         .prefetch_related('target')
    actions = actions[:10]

    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


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
            create_action(request.user, 'created new account')
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
            p = profile_form.cleaned_data['photo']
            profile_form.save()
            messages.success(request, 'Profile updated successfully! %s' % p)
            create_action(request.user, 'updated profile', profile_form)
        else:
            messages.error(request, 'Profile updated failed!')
    else:
        profile_form = ProfileEditForm(instance=request.user)
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/edit.html',
                  {'profile_form': profile_form,
                   'user_form': user_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                create_action(request.user, 'is not followed', user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
