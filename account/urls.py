from django.urls import path
from account import views

urlpatterns = [
    path('indexpage', views.index_page, name="homepage"),
    path('', views.user_register, name="register"),
    path('login', views.user_login, name="login"),
    # path('logout', views.user_logout, name="logout"),
]