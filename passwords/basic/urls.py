from django.conf.urls import url
from basic import views

app_name='basic'

urlpatterns=[
    url('register',views.register,name='register'),
    url('login',views.user_login,name='login'),
]
