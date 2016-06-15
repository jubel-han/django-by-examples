from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login urls with our custom views
    # url(r'login/$', view=user_login, name='login'),
    # TODO: the urls patterns followed up books doesn't work, changed it a little bit.

    # login urls with django contrib auth views
    url('^$', view=views.dashboard, name='dashboard'),
    url(r'^login/$', view='django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', view='django.contrib.auth.views.logout', name='logout'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', view='django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    # change password url patterns
    url(r'^password-change/$', auth_views.password_change,
        {'template_name': 'registration/pwd_change_form.html'}, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done,
        {'template_name': 'registration/pwd_change_done.html'}, name='password_change_done'),
    # restore password urls
    url(r'^password-reset/$', auth_views.password_reset,
        {'template_name': 'registration/pwd_reset_form.html'}, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done,
        {'template_name': 'registration/pwd_reset_done.html'}, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,
        {'template_name': 'registration/pwd_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete,
        {'template_name': 'registration/pwd_reset_complete.html'}, name='password_reset_complete'),
    # user register url
    url(r'register/$', views.register, name='register'),
]
