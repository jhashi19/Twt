from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from .forms import CustomUserCreationModelForm, CustomUserChangeModelForm
from .models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    template_name = 'users/signup.html'
    form_class = CustomUserCreationModelForm

    def post(self, *args, **kwargs):
        form = CustomUserCreationModelForm(self.request.POST,
                                           self.request.FILES)
        is_valid = form.is_valid()
        if not is_valid:
            return render(self.request, 'users/signup.html', {'form': form})
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(reverse('login'))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'users/user_update.html'
    form_class = CustomUserChangeModelForm
    success_url = reverse_lazy('login')  # ユーザ情報を更新したらプロフィール画面に戻るよう修正。
    login_url = 'login'
    fields = ['username', 'icon', 'email', 'age']
