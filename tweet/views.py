from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import datetime, timedelta
from .models import Tweet, Comment
from .forms import TweetForm, CommentForm


class IndexView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('tweet:twt_list')
    login_url = 'login'


class TwtListView(LoginRequiredMixin, ListView):
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
            tweets.append({
                'tweet': tweet,
                'tweet_time': tweet_time,
                'comments': Comment.objects.select_related('tweet').filter(
                    tweet__id=tweet.id).count(),
            })
        context.update({'tweets': tweets})
        return context


class TwtDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = 'tweet/twt_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweet = Tweet.objects.get(pk=self.kwargs['pk'])
        now = datetime.now()
        tweet_time = calc_tweet_time(now, tweet.created)
        context.update({
            'comments': Comment.objects.select_related('tweet').filter(
                tweet__id=self.kwargs['pk']),
            'tweet': tweet,
            'tweet_time': tweet_time
        })
        return context


class TwtCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = 'tweet/twt_create.html'
    fields = ['tweet', 'picture']
    login_url = 'login'
    success_url = reverse_lazy('tweet:twt_list')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     tweet = Tweet.objects.get(pk=self.kwargs['pk'])
    #     context.update({
    #         'tweet': tweet,
    #     })
    #     return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        form = TweetForm(self.request.POST, self.request.FILES)
        is_valid = form.is_valid()
        if not is_valid:
            return render(self.request, 'twt_create.html', {'form': form})
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse_lazy('tweet:twt_detail'),
                        args=(form.instance.id,))


class TwtEditView(LoginRequiredMixin, UpdateView):
    model = Tweet
    template_name = 'twt_edit.html'
    fields = ['tweet', 'picture']
    login_url = 'login'


class TwtDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy('tweet:twt_list')


class TwtCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'tweet/comment_create.html'
    fields = ['comment']
    # success_url = reverse_lazy('tweet:twt_detail')
    login_url = 'login'
    # ツイートのpkを引数としてとってきて、それに紐づくコメントとして登録する。
    # コメントを入力するテキストエリアの上に元のツイートを表示する。
    # →modelにTweetも指定してリンクの引数に対応するツイートを取得して画面の上部に表示する。
    # 上にツイートはあるが、表示はコメント部分が一番上に表示されるように最初からスクロールされた状態で表示する。

    def form_valid(self, form):
        form.instance.tweet = Tweet.objects.get(pk=self.kwargs.get('pk')) #tweet_idがうまく渡せていない。
        form.instance.author = self.request.user
        return super().form_valid(form)

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
        form.save()
        return redirect(reverse_lazy('tweet:twt_detail'),
                        args=(form.instance.tweet.id,))


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
