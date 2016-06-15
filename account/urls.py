from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    # login urls with our custom views
    # url(r'login/$', view=user_login, name='login'),

    # login urls with django contrib auth views
    url('^$', view=views.dashboard, name='dashboard'),
    url(r'^login/$', view='django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', view='django.contrib.auth.views.logout', name='logout'),
    url(r'^logout/$', logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', view='django.contrib.auth.views.logout_then_login', name='logout_then_login'),
]
