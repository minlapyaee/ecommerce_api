from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(),),
    path('login', views.Login.as_view(),),
    path('check-user', views.UserAuth.as_view(),),
    path('logout', views.LogoutView.as_view(),),
]
