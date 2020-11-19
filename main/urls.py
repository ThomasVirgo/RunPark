from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("athletes/", views.athletes, name="athletes"),
    path("logout_page/", views.logout_page, name="logout_page"),
    path("results/", views.results, name="results"),
    path("my_results/<str:pk>", views.my_results, name="my_results"),
    path("cheeky/", views.cheeky, name="cheeky"),
    path("results_data/<str:obj>", views.resultsData, name="results_data"),
    path("my_results/delete/<str:pk>", views.delete_time, name="delete_time"),
    path("my_results/edit/<str:pk>", views.edit_time, name="edit time"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/<str:key>", views.change_details, name="change username"),
    path("nickname/", views.nick_name, name="nickname"),
    path("see_results/<str:pk>", views.SeeResults, name="see their results"),
    ]

