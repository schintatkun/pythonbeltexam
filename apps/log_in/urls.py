from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^logout$',views.logout,),
    url(r'^register$',views.register),
    url(r'^userdashboard$',views.userdashboard),
    url(r'^login$',views.login),
    url(r'^addjob$',views.addjob),
    url(r'^createjob$',views.createjob),
    url(r'^getjob$',views.getjob),
    url(r'^view/(?P<id>\d+)$',views.view),
    url(r'^cancel/(?P<id>\d+)$',views.cancel),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^editjob/(?P<id>\d+)$',views.editjob),
    url(r'^addtomyjob/(?P<id>\d+)$',views.addtomyjob)
]