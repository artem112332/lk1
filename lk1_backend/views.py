from datetime import datetime, date
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *


def index(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    return redirect('profile_page', user_id=user.id)


# return render(request, 'index.html',
#               {'user': user,
#                'user_profile': user_profile,
#                })


def profile_page(request, user_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    profile = UserProfile.objects.get(user=User.objects.get(id=user_id))

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'user_profile': user_profile
    })


class ProfileEdit(APIView):
    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        return render(request, 'lk_edit.html', {
            'profile': profile,
        })

    def post(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if request.FILES:
            file = request.FILES[f'profile{profile.id}_photo']
            profile.photo = file

        full_name = request.POST.get('full_name').split()

        profile.last_name = full_name[0]
        profile.first_name = full_name[1]
        profile.middle_name = full_name[2]
        profile.telegram = request.POST.get('telegram')

        profile.save()
        return redirect(f'/profile/{user.id}/')
