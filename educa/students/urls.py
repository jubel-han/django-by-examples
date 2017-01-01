from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    url(r'^register/$', views.StudentResgistrationView.as_view(), name='student_registration'),
    url(r'^enroll-course/$', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    url(r'^course/$', views.StudentCourseListView.as_view(), name='student_course_list'),
    url(r'^course/(?P<pk>\d+)/$', cache_page(120)(views.StudentCourseDetailView.as_view()), name='student_course_detail'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$', cache_page(120)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'),
]
