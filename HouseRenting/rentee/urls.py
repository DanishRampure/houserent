from django.contrib import admin
from django.urls import path
from rentee import views
from rentee.views import create_review


app_name = 'rentee'

urlpatterns = [
    # path('', views.home , name='home'), # to show demo with team urls, uncomment this line later
    # path('login/', views.user_login , name='user_login'),
    # path('register/', views.user_register , name='user_register'),
    # path('home/', views.home , name='home'),
   path('home/', views.home , name='home'),
    path('properties/', views.location , name='location'),
    path('properties/type/', views.Property_type , name='Property_type'),
    path('wishlist/',views.wishlist,name="wishlist"),
      path('show/',views.show,name="show"),
    # path('properties/<int:property_id>/', views.detail , name='detail'),
     # uncomment the above path when you want to check the detail page dynamically
    path('about/', views.aboutus , name='aboutus'),
    path('reviews/', views.Property_reviews , name='Property_reviews'), 
    path("postreview/",views.create_review,name="review"),
    path('properties/detail/', views.detail , name='detail'), 
    path('properties/detail/images/', views.images , name='images'),
    path("location/",views.location),
    path("session/",views.session),
    path("wishlist/",views.wishlist,name="wishlist"),
    #above path is to check the detail page statically, comment it after testing
]

#------- OLD CODE---------#

# from django.urls import path
# from rentee import views
# from rentee.views import signup,login,review

# urlpatterns = [
#     path('register', signup.as_view()),
#     # path('books_upload',views.books_upload),
#     path('login',login.as_view()),
#     # path('success',views.success),
#     path('home',views.home),
#     path('property',views.Property),
#     path("review",review.as_view()),
#     path("location",views.location)
# ]

