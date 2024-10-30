from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView

from orders.models import Order, Transaction

from .forms import CustomUserLoginForm, CustomUserRegisterForm, UserProfileForm
from .models import User


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему.')
                return redirect('main:index')
            else:
                messages.warning(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему. Теперь укажите свои навыки в '
                                      'настройках профиля')
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
        user.skills.set(form.cleaned_data['skills'])

        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        # исходящие заказы работодателя
        context['employer_orders'] = Order.objects.filter(client=self.request.user)

        # входящие заказы рабочему
        context['worker_orders'] = Order.objects.filter(worker=self.request.user)
        return context


class PublicUserProfileView(DetailView):
    model = User
    template_name = 'users/public_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])


class TransactionHistoryView(ListView):
    model = Transaction
    template_name = 'users/transaction_history.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        # Возвращаем только транзакции для текущего пользователя (работодателя)
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')


def logout_view(request):
    logout(request)
    return redirect('main:index')
