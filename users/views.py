from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
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


class TweetUserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)


class CommentUserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)


class FollowerUserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = CustomUser.objects.get(id=self.kwargs['pk'])
        user_list = profile_user.followers.all()
        context.update({
            'user_list': user_list,
            'title': 'Follower',
        })
        return context


class FollowingUserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = CustomUser.objects.get(id=self.kwargs['pk'])
        user_list = profile_user.followees.all()
        context.update({
            'user_list': user_list,
            'title': 'Following',
        })
        return context


def follow(request):
    if request.user.is_authenticated:
        login_user = request.user
        profile_user_id = request.POST.get('user_id')
        profile_user = CustomUser.objects.get(id=profile_user_id)
        if profile_user.followers.filter(id=request.user.id).exists():
            profile_user.followers.remove(login_user)
        else:
            profile_user.followers.add(login_user)
        json_data = {
            'follower_count': profile_user.followers.all().count()
        }
        return JsonResponse(json_data)
    else:
        return HttpResponse(reverse_lazy('login'))
