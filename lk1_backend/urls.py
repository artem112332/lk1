from django.urls import path
from lk1_backend.views import *

urlpatterns = [
    path('profile/<int:user_id>/', profile_page, name='profile_page'),
    path('edit_profile/', ProfileEdit.as_view()),
    path('meetings/', meetings_page, name='meetings'),
    path('events/', events_page, name='events'),
    path('my_team/', project_team_page, name='project_team_page'),
    path('tutor_teams/', tutor_teams_page, name='tutor_teams_page'),
    path('applications/', applications_page, name='applications_page'),
    path('directions/', directions_page, name='directions_page'),
]
