from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import messages, auth
#from django.core.urlresolvers import reverse
from .forms import UserLoginForm, UserRegistrationForm, UserForm, ProfileForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm


def index(request):
    """Displays the index page"""
    return render(request, "index.html")


def logout(request):
    """Logs the user out and redirects them back to the index page"""
    auth.logout(request)
    return redirect(reverse('index'))


def login(request):
    """Handles the login form"""
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request.POST['username_or_email'],
                                     password=request.POST['password'])

            if user and user.is_active:  # Passes the rejection message if user has had 'is_active' flag set to false
                auth.login(request, user)

                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('profile'))
            else:
                user_form.add_error(None, "Your username or password are incorrect")
    else:
        user_form = UserLoginForm()

    args = {'user_form': user_form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', args)


@login_required
def profile(request):
    """Displays the profile page of a user who is logged-in"""
    return render(request, 'profile_content.html')


def register(request):
    """Handles the registration form"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            user = auth.authenticate(request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered!")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "Unable to log you in at this time. Please refresh and try again.")
    else:
        user_form = UserRegistrationForm()

    args = {'user_form': user_form}
    return render(request, 'register.html', args)

"""
@login_required
def edit_profile(request):
    Handles the edit profile form
    if request.method == 'POST':
        user_form = UserEditProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('profile'))
    else:
        user_form = UserEditProfileForm(instance=request.user)

    args = {'user_form': user_form}
    return render(request, 'edit_profile.html', args)
"""

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ("Your profile was successfully updated!"))
            return redirect(reverse('profile'))
        else:
            messages.error(request, ('Update unsuccessful. Please rectify the problem below'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    args = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'edit_profile.html', args)

