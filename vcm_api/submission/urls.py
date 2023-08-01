from django.urls import path
from vcm_api.submission import views

urlpatterns = [
    path('', views.CreateSubmissionView.as_view()),
]
