from django.contrib import admin
from django.urls import path
from owner import views as views1

urlpatterns = [
    path('add/',views1.add,name="add"),
    path('login/home/',views1.home1,name='home1'),
    path('signup/verify/login/home/',views1.home1,name='home1'),
    path('signup/home/',views1.home1,name='home1'),
    path('owner/add/home1',views1.home1,name='home1'),
    path('add/home1/',views1.home1,name='home1'),
    path('home1/',views1.home1,name='home1'),
    path('', views1.home, name='home'),
    path('home', views1.home, name='home'),
    path('profile/',views1.profile,name='profile'),
    path('home1/profile/',views1.profile,name='profile'),
    path('logoutpage/',views1.logoutpage,name='logoutpage'),    
    path('prop/<str:id>',views1.prop,name='prop'),
    path('about1/',views1.about1,name='about1'),
]