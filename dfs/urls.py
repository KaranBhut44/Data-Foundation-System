from django.urls import path, include # new
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('registration',views.registration,name='registration'),
    path('home',views.home,name='home'),
    path('download/<int:id>',views.download,name='download'),
    path('cancelReq/<int:id>',views.cancelReq,name='cancelReq'),
    path('requestDataset/<int:id>',views.requestDataset,name='requestDataset'),
    path('adminPanel',views.adminPanel,name='adminPanel'),
    path('acceptReq/<int:id>',views.acceptReq,name='acceptReq'),
    path('rejectReq/<int:id>',views.rejectReq,name='rejectReq'),
    path('registration', views.registration, name='registration'),
    path('validate', views.validate, name='validate'),
    path('validateRegistration', views.validateRegistration, name='validateRegistration'),
    path('login', views.login, name='login'),
    path('logout',views.logout,name='logout')
]