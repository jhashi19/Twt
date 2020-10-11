from django import forms
from .models import Tweet, Comment


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ('tweet', 'picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tweet'].required = False
        self.fields['tweet'].label = 'tweet'
        self.fields['picture'].required = False
        self.fields['picture'].label = 'upload image'

    def clean(self):
        tweet = self.cleaned_data['tweet']
        picture = self.cleaned_data['picture']

        if not (tweet or picture):
            raise forms.ValidationError(
                'Both "tweet" and "image" are blank!'
            )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].required = True
        self.fields['comment'].label = 'comment'
