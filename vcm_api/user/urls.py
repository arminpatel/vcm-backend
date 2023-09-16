from django.urls import path

from vcm_api.user import views

urlpatterns = [
    path('<str:username>/', views.RetrieveUpdateProfileView.as_view()),
    path('', views.CreateUserView.as_view()),
]
