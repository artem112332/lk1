from datetime import datetime, date
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import *


def index(request):
    return redirect('meetings')


def meetings_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    user_meetings = [user_meeting.meeting for user_meeting in UserMeeting.objects.filter(user=user_profile)]
    meetings = {
        meeting: ', '.join([f'{user_meeting.user.short_name()}'
                            for user_meeting in UserMeeting.objects.filter(meeting=meeting)])
        for meeting in user_meetings
    }

    return render(request, 'meetings_list.html',
                  {'user': user,
                   'user_profile': user_profile,
                   'meetings': meetings,
                   })


def events_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    user_events = [user_event.event for user_event in UserEvent.objects.filter(user=user_profile)]
    events = {
        event: ', '.join([f'{event_direction.direction.name}'
                          for event_direction in EventDirection.objects.filter(event=event)])
        for event in user_events
    }

    return render(request, 'events-manager.html',
                  {'user': user,
                   'user_profile': user_profile,
                   'events': events,
                   })


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
        profile.phone_number = request.POST.get('phone_number')
        profile.email = request.POST.get('email')
        profile.telegram = request.POST.get('telegram')
        profile.university = request.POST.get('university')
        profile.year_of_study = request.POST.get('year_of_study')
        profile.specialization = request.POST.get('specialization')

        profile.save()
        return redirect(f'/profile/{user.id}/')
