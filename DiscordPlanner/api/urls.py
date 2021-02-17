from django.urls import path
from .views import *
urlpatterns = [
    path('guild/create', CreateGuildView.as_view()),
    path('guild/get_all', GetAllGuildsView.as_view()),
    path('guild/get_user', GetUsersView.as_view()),
    path('user/create', CreateUserView.as_view()),
    path('user/join_guild', JoinGuildView.as_view()),
    path('user/create_and_join_guild', CreateUserAndJoinGuildView.as_view()),
]
