from django.urls import path
from . import views
app_name='systemApp'
urlpatterns = [
  
   path('',views.home_page,name="home"),
   path('tweets',views.tweets,name="tweets"),
   path('dashboard/<str:data>',views.dashboard,name="dashboard"),
   path('get_data',views.get_data,name="get_data"),
   
   
 
    

]
