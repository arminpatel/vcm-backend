from django.urls import path
from vcm_api.contest import views

urlpatterns = [
    path('<int:pk>', views.RetrieveContestView.as_view()),
    path('user/<str:username>', views.ListParticipantContestView.as_view()),
]
