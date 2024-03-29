from django.urls import path
from vcm_api.contest import views

urlpatterns = [
    path('<int:pk>/', views.RetrieveUpdateContestView.as_view()),
    path('user/<str:username>/', views.ListParticipantContestView.as_view()),
    path('', views.CreateContestView.as_view()),
]
