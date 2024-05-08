from  django.urls import path
from . import views

urlpatterns = [
    path("", views.Home,name="home"),
    path('signup',views.SignUp,name="signup"),
    path('signin',views.SignIn,name="signin"),
    path('logout',views.Logout,name="logout"),
    path('profile/<str:pk>',views.Profile_view,name="profile"),
    path('setting',views.Setting,name="setting"),
    path('upload',views.Upload,name="upload"),
    path('like-post',views.Post_like,name="like-post"),



    
]