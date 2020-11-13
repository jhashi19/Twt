from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Tweet(models.Model):
    tweet = models.TextField()
    picture = models.ImageField(
        upload_to='image/picture/',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='tweet_author'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(get_user_model(),
                                  blank=True)

    def __str__(self):
        if len(self.tweet) < 10:
            return self.tweet
        else:
            return self.tweet[:10] + '...'

    def get_absolute_url(self):
        return reverse('tweet:twt_detail', args=[str(self.id)])


class Comment(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE
    )
    comment = models.TextField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comment_author'
    )
    like = models.ManyToManyField(get_user_model(),
                                  blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.comment) < 10:
            return self.comment
        else:
            return self.comment[:10] + '...'
