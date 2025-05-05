from django.urls import path
from lk1_backend.views import *

urlpatterns = [
    path('profile/<int:user_id>/', profile_page, name='profile_page'),
    path('edit_profile/', ProfileEdit.as_view()),
]
