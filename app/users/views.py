from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import CustomUserRegisterForm, UserProfileForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему.')
                return redirect('main:index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему.')
            return redirect('main:index')
    else:
        form = CustomUserRegisterForm()

    return render(request, 'users/registration.html', {'form': form})


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_free = form.cleaned_data.get('available')
        user.save()
        user.skills.set(form.cleaned_data['skills'])  # Сохраняем выбранные навыки

        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


def logout_view(request):
    logout(request)
    return redirect('main:index')
