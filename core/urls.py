from django.urls import path
from core import views
from core.views import home_view, update_delete_user

urlpatterns = [
    path("api/signup/", views.signup, name="signup"),  # <-- Correct this line
    path("api/login/", views.login, name="login"),  # <-- Correct this line
    path("", home_view, name="home"),
    path("users/", views.user_list, name="user_list"),
    path("profile/", update_delete_user, name="profile"),
    
]
