from django.urls import path
from .views import *


urlpatterns = [
    path('', index_login, name='index_login'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', user_logout),
    path('registration/', Register.as_view(), name='registration'),
]
