from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from users.forms import CreateUserForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as translate
from utils.utils_classes import CustomLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin



class UserShowView(View):
    def get(self, request):
        all_users = User.objects.all()
        info = []
        for item in all_users:
            full_name = item.first_name + item.last_name
            info.append(
                (
                    item.id,
                    item.username,
                    full_name,
                    item.date_joined,
                )
            )
        
        tables = [
            translate('ID'),
            translate('Username'),
            translate('Full name'),
            translate('Created at'),
        ]
        
        return render(request, 'table.html', context={
            'info': info,
            'title': translate('Users'),
            'tables': tables,
            'url_name_change': 'update_user',
            'url_name_delete': 'delete_user',
        })


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'forms.html'
    success_url = reverse_lazy('home')
    success_message = translate("User registered successfully")  # "Пользователь успешно зарегистрирован"
    extra_context = {
        'title': translate('Create User'),
        'button': translate('Create'),
    }


class UserUpdateView(UserPassesTestMixin, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'password']
    template_name = 'forms.html'
    success_url = reverse_lazy('home')
    success_message = translate("User successfully changed")  # "Пользователь успешно изменен"
    extra_context = {
        'title': translate('Update user'),
        'button': translate('Update'),
    }
    def test_func(self, **kwargs):
        return self.request.user.id == self.kwargs.get('pk')
    
    def handle_no_permission(self):
        text_error = translate("You are not allowed to edit this user")
        messages.error(self.request, text_error)
        return redirect(reverse_lazy('users'))



class UserDeleteView(UserPassesTestMixin, CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'forms.html'
    success_message = translate("User successfully deleted")  # "Пользователь успешно удален"
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = translate('Delete user')
        context['value_to_delete'] = context['object']
        context['name'] = translate('user')
        context['button'] = translate('Delete')
        return context
    def test_func(self, **kwargs):
        return self.request.user.id == self.kwargs.get('pk')
    
    def handle_no_permission(self):
        text_error = translate("You are not allowed to delete this user")
        messages.error(self.request, text_error)
        return redirect(reverse_lazy('users'))

class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'forms.html'
    success_message = translate("You are logged in")  # "Вы залогинены"
    extra_context = {
        'title': translate('Log In'),
        'button': translate('Log In'),
    }
    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        msg = translate("Successfully logged out")
        messages.add_message(request, messages.INFO, msg)
        return response
