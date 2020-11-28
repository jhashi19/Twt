from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import datetime, timedelta
from .models import Tweet, Comment
from .forms import TweetForm, CommentForm
from users.models import CustomUser


# LoginRequiredMixinを先に継承することでログインしていないユーザはツイート画面を開けないようにする。
class IndexView(RedirectView):
    url = reverse_lazy('tweet:twt_list')
    login_url = 'login'


class TwtListView(ListView):
    model = Tweet
    template_name = 'tweet/twt_list.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweets = []
        tweet_list = Tweet.objects.all().order_by('-created')
        now = datetime.now()
        for tweet in tweet_list:
            tweet_time = calc_tweet_time(now, tweet.created)
            tweet_liked = False
            if tweet.like.filter(id=self.request.user.id).exists():
                tweet_liked = True
            tweets.append({
                'tweet': tweet,
                'tweet_time': tweet_time,
                'comments': Comment.objects.select_related('tweet').filter(
                    tweet__id=tweet.id).count(),
                'tweet_liked': tweet_liked
            })
        context.update({'tweets': tweets})
        return context


class TwtDetailView(DetailView):
    model = Tweet
    template_name = 'tweet/twt_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweet = Tweet.objects.get(pk=self.kwargs['pk'])
        tweet_liked = False
        if tweet.like.filter(id=self.request.user.id).exists():
            tweet_liked = True
        now = datetime.now()
        tweet_time = calc_tweet_time(now, tweet.created)
        comment_list = Comment.objects.filter(tweet__id=self.kwargs['pk'])
        comments = []
        for comment in comment_list:
            comment_liked = False
            if comment.like.filter(id=self.request.user.id).exists():
                comment_liked = True
            comments.append({
                'comment': comment,
                'comment_liked': comment_liked,
            })
        context.update({
            'comments': comments,
            'tweet': tweet,
            'tweet_time': tweet_time,
            'tweet_liked': tweet_liked,
        })
        return context


class TwtCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = 'tweet/twt_create.html'
    fields = ['tweet', 'picture']
    login_url = 'login'
    success_url = reverse_lazy('tweet:twt_list')

    def post(self, *args, **kwargs):
        form = TweetForm(self.request.POST, self.request.FILES)
        is_valid = form.is_valid()
        if not is_valid:
            return render(self.request, 'twt_create.html', {'form': form})
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse_lazy('tweet:twt_detail',
                                     args=(form.instance.id,)))


# UserPassesTestMixinを継承することで、投稿の編集は投稿者のみがすることができるようになる。
class TwtEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    template_name = 'tweet/twt_edit.html'
    fields = ['tweet', 'picture']
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TwtDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = 'tweet/twt_delete.html'
    success_url = reverse_lazy('tweet:twt_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweet = Tweet.objects.get(pk=self.kwargs['pk'])
        context.update({'tweet': tweet})
        return context


class TwtCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'tweet/comment_create.html'
    fields = ['comment']
    login_url = 'login'
    # 上にツイートはあるが、表示はコメント部分が一番上に表示されるように最初からスクロールされた状態で表示する。

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweet = Tweet.objects.get(pk=self.kwargs['pk'])
        context.update({
            'tweet': tweet,
        })
        return context

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            return render(self.request, 'tweet/comment_create.html',
                          {'form': form})
        form.instance.tweet = Tweet.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse_lazy('tweet:twt_detail',
                                     args=(form.instance.tweet_id,)))


class TwtCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'tweet/comment_delete.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        context.update({
            'comment': comment,
            'tweet': Tweet.objects.get(
                id=comment.tweet.id),
        })
        return context

    def get_success_url(self, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('tweet:twt_detail',
                            kwargs={'pk': comment.tweet.id})


class TwtCommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'tweet/comment_edit.html'
    fields = ['comment']
    login_url = 'login'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        context.update({
            'comment': comment,
            'tweet': Tweet.objects.get(
                id=comment.tweet.id),
        })
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('tweet:twt_detail',
                            kwargs={'pk': comment.tweet.id})


class ProfileView(ListView):
    model = Tweet
    template_name = 'tweet/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = CustomUser.objects.get(id=self.kwargs['pk'])
        follower_count = profile_user.followers.all().count()
        following_count = profile_user.followees.all().count()
        is_follow = False
        if profile_user.followers.filter(id=self.request.user.id).exists():
            is_follow = True
        tweets = []
        tweet_list = Tweet.objects.filter(
            author_id=self.kwargs['pk']).order_by('-created')
        now = datetime.now()
        for tweet in tweet_list:
            tweet_time = calc_tweet_time(now, tweet.created)
            tweet_liked = False
            if tweet.like.filter(id=self.request.user.id).exists():
                tweet_liked = True
            tweets.append({
                'tweet': tweet,
                'tweet_time': tweet_time,
                'comments': Comment.objects.select_related('tweet').filter(
                    tweet__id=tweet.id).count(),
                'tweet_liked': tweet_liked
            })
        context.update({
            'tweets': tweets,
            'profile_user': profile_user,
            'is_follow': is_follow,
            'follower_count': follower_count,
            'following_count': following_count,
        })
        return context


# ブラウザバックでいいねの挙動がおかしくなる。ハートのオンオフが逆になる。またはいいね数が逆になる。
def tweet_like(request):
    if request.user.is_authenticated:
        tweet = Tweet.objects.get(id=request.POST.get('tweet_id'))
        tweet_like = False
        if tweet.like.filter(id=request.user.id).exists():
            tweet.like.remove(request.user)
            tweet_like = False
        else:
            tweet.like.add(request.user)
            tweet_like = True
        like_count = tweet.like.count()
        json_data = {
            'like_count': like_count,
            'tweet_like': tweet_like,
        }
        return JsonResponse(json_data)
    else:
        return HttpResponse(reverse_lazy('login'))


def comment_like(request):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
        if comment.like.filter(id=request.user.id).exists():
            comment.like.remove(request.user)
        else:
            comment.like.add(request.user)
        comment_like_count = comment.like.count()
        json_data = {
            'comment_like_count': comment_like_count
        }
        return JsonResponse(json_data)
    else:
        return HttpResponse(reverse_lazy('login'))


def tweet_detail_like(request):
    if request.user.is_authenticated:
        tweet = Tweet.objects.get(id=request.POST.get('tweet_id'))
        if tweet.like.filter(id=request.user.id).exists():
            tweet.like.remove(request.user)
        else:
            tweet.like.add(request.user)
        like_count = tweet.like.count()
        json_data = {
            'detail_like_count': like_count
        }
        return JsonResponse(json_data)
    else:
        return HttpResponse(reverse_lazy('login'))


def calc_tweet_time(now, created_time):
    """いつ投稿したか現時点からの経過時間を計算する。
       投稿から1週間を過ぎたら投稿した日付・時刻を返す。"""
    created_time = datetime(
        year=created_time.year,
        month=created_time.month,
        day=created_time.day,
        hour=created_time.hour,
        minute=created_time.minute,
        second=created_time.second
    )
    delta = now - created_time
    if delta < timedelta(seconds=60):
        tweet_time = f'{delta.seconds}秒前'
    elif delta < timedelta(minutes=60):
        tweet_time = f'{delta.seconds // 60}分前'
    elif delta < timedelta(hours=24):
        tweet_time = f'{delta.seconds // 3600}時間前'
    elif delta < timedelta(days=7):
        tweet_time = f'{delta.days}日前'
    else:
        tweet_time = f"{created_time.strftime('%Y/%m/%d %H:%m:%S')}"

    return tweet_time
