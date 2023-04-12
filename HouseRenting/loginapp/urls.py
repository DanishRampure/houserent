from django.contrib import admin
from django.urls import path
from loginapp import views as views1
from owner import views as views2
from rentee import views as views3


urlpatterns = [

    path('', views1.home, name='home'), 
    path('home', views1.home, name='home'),
    path('home/', views1.home, name='home'),
    path('signup/', views1.signup, name='signup'),
    path('login/signup/', views1.signup, name='signup'),
    path('signup/login',views1.login,name='login'), 
    path('login/',views1.login,name='login'),
    path('signup/verify/login/',views1.login,name='login'),
    path('verify/',views1.verify,name="verify"),
    path('verify1/',views1.verify1,name="verify1"),
    path('signup/verify/',views1.verify,name="verify"),
    path('forgot/',views1.forgot,name='forgot'),
    path('forgotconfirm/',views1.forgotconfirm,name='forgotconfirm'),
    path('forgotconfirm/forgot/',views1.forgot,name='forgot'),
    path('login/home/',views2.home1,name='home1'),
    path('login/home/about1/',views2.about1,name='about1'),
    path('welcome/',views1.home,name='home'),
    path('add/',views2.add,name="add"),
    path('signup/verify/login/home/',views2.home1,name='home1'),
    path('signup/home/',views2.home1,name='home1'),
    path('add/home1/',views2.home1,name='home1'),
    path('home1/',views2.home1,name='home1'),
    path('logoutpage/',views2.logoutpage,name='logoutpage'),
    path('add/home/',views2.add,name="add"),
    path('login/home/profile/',views2.profile,name='profile'),
    path('login/home/prop/<str:id>',views2.prop,name='prop'),
    path('about/',views1.about,name='about'),
    path('login/home1/', views3.home , name='home'),
    path('signup/verify/login/home1/', views3.home , name='home'),
]
