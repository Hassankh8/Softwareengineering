from django.urls import path
from core import views
from core.views import home_view, main, update_delete_user, search_history_view

urlpatterns = [
    path("api/signup/", views.signup, name="signup"),  # <-- Correct this line
    path("api/login/", views.login, name="login"),  # <-- Correct this line
    path("", home_view, name="home"),
    path("api/users/<int:user_id>/", update_delete_user, name="update_delete_user"),
    path("login/", views.login_view, name="login"),
    path("main/", main, name="main"),
    path("user_list/", views.user_list, name="user_list"),
    path("search-history/", search_history_view, name="search_history"),
    path("media_search/", views.media_search, name="media_search"),
    path("delete_search/<int:search_id>/", views.delete_search, name="delete_search"),
    path("update_search/<int:search_id>/", views.update_search, name="update_search"),
]
