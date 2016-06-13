from django.conf.urls import url, include
from .views import user_login

urlpatterns = [
    url(r'login/$', view=user_login, name='login'),
]
