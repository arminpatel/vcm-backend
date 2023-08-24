from django.urls import path
from vcm_api.submission import views

urlpatterns = [
    path('', views.CreateSubmissionView.as_view()),
    path('<int:contestid>/', views.ListContestSubmission.as_view()),
    path('<int:contestid>/<str:username>/', views.ListUserContestSubmission.as_view()),
]
