from django.contrib import admin
from django.urls import path
from adminpanel import views

urlpatterns = [

    #login and dashboard section 
    path('admin/', admin.site.urls),
    path('',views.index,name='Home'),
    path('connect',views.connect,name="connect"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.handellogout,name="logout"),
    path('logoutpage',views.logoutpage,name="logoutpage"),
    

    #userinfo section
    path('userinfo',views.userinfo,name="userinfo"),
    path('userinfo/search_id',views.user_info_search_id,name="user_info_search_id"),
    path('userinfo/search_first_name',views.user_info_search_first_name,name="user_info_search_first_name"),
    path('userinfo/search_last_name',views.user_info_search_last_name,name="user_info_search_last_name"),
    path('userinfo/search_email',views.user_info_search_email,name="user_info_search_email"),
    path('userinfo/search_phone_number',views.user_info_search_phone_numeber,name="user_info_search_phone_numeber"),
    path('userinfo/search_role',views.user_info_search_role,name="user_info_search_role"),
    path('userinfo/delete/<str:user_id>',views.user_info_delete,name="user_info_delete"),
    path('userinfo/update/<str:user_id>',views.user_info_update,name="user_info_update"),
    path('userinfo/update/update_data/<str:user_id>',views.user_info_submit_updated_data,name="user_info_submit_updated_data"),
    path('userinfo/adduser',views.user_info_adduser,name="user_info_adduser"),
    path('userinfo/submit_data',views.add_data,name="add_data"),



    #managereviews section
    path('managereviews',views.managereviews,name="managereviews"),
    path('managereviews/search_rating_id',views.managereview_search_rating_id,name="managereview_search_rating_id"),
    path('managereviews/search_user_name',views.managereview_search_user_name,name="managereview_search_user_name"),
    path('managereviews/search_user_id',views.managereview_search_user_id,name="managereview_search_user_id"),
    path('managereviews/search_property_id',views.managereview_search_property_id,name="managereview_search_property_id"),
    path('managereviews/search_flat_name',views.managereview_search_flat_name,name="managereview_search_flat_name"),
    # path('managereviews/search_review',views.managereview_search_review,name="anagereview_search_review"),
    path('managereviews/search_rating',views.managereview_search_rating,name="managereview_search_rating"),
    path('managereviews/update/<str:id>',views.managereviews_update,name="managereviews_update"),
    path('managereviews/delete/<str:id>',views.managereviews_delete,name="managereviews_delete"),
    path('managereviews/adddata',views.managereviews_adddata,name="managereviews_adddata"),
    path('managereviews/update/update_data/<str:id>',views.managereviews_submit_updated_data,name="managereviews_submit_updated_data"),
    path('managereviews/submit_data',views.managereviews_add_data,name="managereviews_add_data"),


    # manage Reviews section
    path('manageproperties',views.manageproperties,name="manageproperties"),
    path('manageproperties/adddata',views.manageproperties_adddata,name="manageproperties_adddata"),
    path('manageproperties/submit_data',views.manageproperties_submit_data,name="manageproperties_adddata"),
    path('manageproperties/delete/<str:id>',views.manageproperties_delete,name="manageproperties_update"),
    path('manageproperties/update/<str:id>',views.manageproperties_update,name="manageproperties_update"),
    path('manageproperties/update/update_data/<str:id>',views.manageproperties_submit_updated_data,name="manageproperties_submit_updated_data"),
    path('manageproperties/search_id',views.manageproperties_search_id,name="manageproperties_search_id"),
    path('manageproperties/search_city',views.manageproperties_search_city,name="manageproperties_search_city"),
    path('manageproperties/search_flat_name',views.manageproperties_search_flat_name,name="manageproperties_search_flat_name"),
    path('manageproperties/search_ramount',views.manageproperties_search_ramount,name="manageproperties_search_ramount"),
    path('manageproperties/search_area',views.manageproperties_search_area,name="manageproperties_search_area"),
    path('manageproperties/search_status',views.manageproperties_search_status,name="manageproperties_search_status"),
    path('manageproperties/search_owner_id',views.manageproperties_search_owner_id,name="manageproperties_search_owner_id"),
    path('manageproperties/search_bond',views.manageproperties_search_bond,name="manageproperties_search_bond"),
    

    # manage rental section 
    path('managerental',views.managerental,name="managerental"),
    path('managerental/update/<str:id>',views.managerental_update,name="managerental_update"),
    path('managerental/update/update_data/<str:id>',views.managerental_submit_updated_data,name="managerental_submit_updated_data"),
    path('managerental/search_id',views.managerental_search_id,name="managerental_search_id"),
    path('managerental/search_city',views.managerental_search_city,name="managerental_search_city"),
    path('managerental/search_flat_name',views.managerental_search_flat_name,name="managerental_search_flat_name"),
    path('managerental/search_ramount',views.managerental_search_ramount,name="managerental_search_ramount"),
    path('managerental/search_area',views.managerental_search_area,name="managerentals_search_area"),
    path('managerental/search_status',views.managerental_search_status,name="managerental_search_status"),
    path('managerental/search_owner_id',views.managerental_search_owner_id,name="managerental_search_owner_id"),
    path('managerental/search_bond',views.managerental_search_bond,name="managerental_search_bond"),

]
