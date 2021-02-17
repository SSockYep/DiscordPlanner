from django.urls import path
from . import views
urlpatterns = [
    path('new/', views.newPlanView),
    path('', views.planView),
]
