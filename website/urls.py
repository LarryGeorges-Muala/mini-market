from django.conf.urls import url 
from . import views

app_name = 'website'

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^manager$', views.manager, name='manager'),
	url(r'^contact_frame$', views.frame_form, name='frame_form'),
	url(r'^contact_frame/email-sent/$',views.frame_form, name='frame_form'),
	url(r'^contact_frame/error-sent/$',views.frame_form, name='frame_form'),
	url(r'^ajax/totalizer/$', views.totalizer, name='totalizer'),
]