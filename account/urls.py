from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login urls with our custom views
    # url(r'login/$', view=user_login, name='login'),

    # login urls with django contrib auth views
    url('^$', view=views.dashboard, name='dashboard'),
    url(r'^login/$', view='django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', view='django.contrib.auth.views.logout', name='logout'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', view='django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^password-change/$', auth_views.password_change,
        {'template_name': 'registration/password_change.html'}, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done,
        {'template_name': 'registration/password_change_success.html'}, name='password_change_done'),
]
