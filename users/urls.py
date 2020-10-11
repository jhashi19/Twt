from django.urls import path
from .views import SignUpView

app_name = 'users'
urlpatterns = [
    path('singup/', SignUpView.as_view(), name='signup'),
]
