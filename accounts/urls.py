from django.contrib.auth import views 
#from .forms import LoginForm
from django.urls import include,path
from . import views

app_name='accounts'
urlpatterns = [
    #path('login',views.login,{'authentication_form':LoginForm}),
    #path('user_login/', views.user_login, name='user_login'),
    
    path('signup',views.signup,name="signup"),
    path('profile/',views.profile,name="profile"),
    path('home',views.home_page,name="home"),
    path('dashboard/<str:topic>',views.dashboard,name="dashboard"),
    path('tweets',views.tweets,name="tweets"),
    # path('search',views.search,name="search"),
    path('get_data',views.get_data,name="get_data"),
    path('create_report/<str:topic>',views.create_report,name="create_report"),
    path('save_topic/<str:topic>',views.save_topic,name="save_topic"),

     
     

]
