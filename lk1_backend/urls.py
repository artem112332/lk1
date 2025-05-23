from django.urls import path
from lk1_backend.views import *

urlpatterns = [
    path('profile/<int:user_id>/', profile_page, name='profile_page'),
    path('edit_profile/', ProfileEdit.as_view()),
    path('meetings/', meetings_page, name='meetings'),
    path('events/', events_page, name='events'),
    path('event/<int:event_id>/', event_info, name='event_details'),
]
