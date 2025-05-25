from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import *


def index(request):
    return redirect('profile_page', user_id=request.user.id)


def meetings_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    users_meetings = UserMeeting.objects.filter(user=user_profile)
    user_meetings = [user_meeting.meeting for user_meeting in users_meetings]
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

    users_events = UserEvent.objects.filter(user=user_profile)
    user_events = [user_event.event for user_event in users_events]
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


# def event_info(request, event_id):
#     user = request.user
#     user_profile = UserProfile.objects.get(user=user)
#
#     event = Event.objects.get(id=event_id)


def applications_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    project_applications = ApllictationToProject.objects.filter(sender=user_profile)
    event_appplications = ApllictationToEvent.objects.filter(sender=user_profile)

    return render(request, 'applications.html', {
        'user': user,
        'profile': user_profile,
        'project_applications': project_applications,
        'event_appplications': event_appplications,
    })


def profile_page(request, user_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    profile = UserProfile.objects.get(user=User.objects.get(id=user_id))

    user_files = UserFile.objects.filter(user=profile)

    if UserProject.objects.filter(member=user_profile) != 0:
        user_project = UserProject.objects.get(member=user_profile)
        main_role = user_project.member_main_role
        second_role = user_project.member_second_role
        third_role = user_project.member_third_role

        return render(request, 'profile.html', {
            'user': user,
            'profile': profile,
            'have_project': True,
            'main_role': main_role,
            'second_role': second_role,
            'third_role': third_role,
            'files': user_files,
        })

    else:
        return render(request, 'profile.html', {
            'user': user,
            'profile': profile,
            'user_profile': user_profile,
            'have_project': False,
            'files': user_files,
        })


class ProfileEdit(APIView):
    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if UserProject.objects.filter(member=profile) != 0:
            user_project = UserProject.objects.get(member=profile)
            main_role = user_project.member_main_role
            second_role = user_project.member_second_role
            third_role = user_project.member_third_role

            return render(request, 'lk_edit.html', {
                'profile': profile,
                'have_project': True,
                'main_role': main_role,
                'second_role': second_role,
                'third_role': third_role
            })

        else:
            return render(request, 'lk_edit.html', {
                'profile': profile,
                'have_project': False
            })

    def post(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if request.FILES:
            files = request.FILES

            if f'profile{profile.id}_photo' in files:
                photo = files.pop(f'profile{profile.id}_photo')[0]
                profile.photo = photo

            if len(files) > 0:
                for file in files.values():
                    UserFile.objects.create(user=profile, file=file)

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

        if UserProject.objects.filter(member=profile) != 0:
            user_project = UserProject.objects.get(member=profile)
            if request.POST.get('role_1') is not None:
                user_project.member_main_role = request.POST.get('role_1')

            if request.POST.get('role_2') is not None:
                user_project.member_second_role = request.POST.get('role_2')

            if request.POST.get('role_3') is not None:
                user_project.member_third_role = request.POST.get('role_3')

            user_project.save()

        profile.save()
        return redirect(f'/profile/{user.id}/')
