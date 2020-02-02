from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .tokens import account_activation_token


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None
    # checking if the user exists, if the token is valid.
    if new_user is not None and account_activation_token.check_token(new_user, token):
        # if valid set active true
        new_user.is_active = True
        # set signup_confirmation true
        new_user.save()
        login(request, new_user)
        return redirect('deals:home')
    else:
        return render(request, 'registration/activation_invalid.html')


# TODO Создать crontab который будет удалять не активированных пользователей, который зарегистрировались больше 7 дней назад
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            Profile.objects.create(user=new_user)
            # Activation token
            current_site = get_current_site(request)
            subject = 'Пожалуйста, активируйте свою учетную запись'
            message = render_to_string('registration/activation_request.html', {
                'user': new_user,
                'protocol': request.scheme,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(new_user),
            })
            new_user.email_user(subject, message)
            # Создается профиль пользователя

            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
        else:
            messages.error(request, 'Произошла ошибка обновления вашего профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'profile': profile})
