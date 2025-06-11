from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import *


def index(request):
    return redirect('profile_page', user_id=request.user.id)


def meetings_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

    users_meetings = UserMeeting.objects.filter(user=user_profile)
    user_meetings = [user_meeting.meeting for user_meeting in users_meetings]
    meetings = {
        meeting: ', '.join([f'{user_meeting.user.short_name()}'
                            for user_meeting in UserMeeting.objects.filter(meeting=meeting)])
        for meeting in user_meetings
    }

    return render(request, 'meetings_list.html',
                  {
                      'user': user,
                      'user_profile': user_profile,
                      'statuses': statuses,
                      'meetings': meetings,
                  })


def project_team_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

    if len(UserProject.objects.filter(member=user_profile)) != 0:
        user_project = UserProject.objects.get(member=user_profile)
        project = user_project.project
        team_name = user_project.team_name
        team_members = [project_member for project_member in UserProject.objects.filter(team_name=team_name)]

        return render(request, 'project_team.html',
                      {
                          'user': user,
                          'user_profile': user_profile,
                          'statuses': statuses,
                          'project': project,
                          'team_name': team_name,
                          'team_members': team_members,
                      })


def tutor_teams_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

    tutor_teams = {}
    for project in Project.objects.filter(tutor=user_profile):
        for user_project in UserProject.objects.filter(project=project):
            tutor_teams[user_project.team_name] = {'project': project.name, 'direction': project.direction}

    return render(request, 'tutor_teams.html',
                  {
                      'user': user,
                      'user_profile': user_profile,
                      'statuses': statuses,
                      'tutor_teams': tutor_teams
                  })


def directions_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

    user_directions = Direction.objects.filter(director=user_profile)

    direction_teams_events = {
        direction.name: {
            'teams': len(Project.objects.filter(direction=direction)),
            'events': len(Event.objects.filter(direction=direction))
        }
        for direction in user_directions
    }

    return render(request, 'directions.html',
                  {
                      'user': user,
                      'user_profile': user_profile,
                      'statuses': statuses,
                      'directions': direction_teams_events
                  })


def events_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

    users_events = UserEvent.objects.filter(user=user_profile)
    user_events = [user_event.event for user_event in users_events]
    events = {
        event: ', '.join([f'{event_direction.direction.name}'
                          for event_direction in EventDirection.objects.filter(event=event)])
        for event in user_events
    }

    return render(request, 'events.html',
                  {'user': user,
                   'user_profile': user_profile,
                   'statuses': statuses,
                   'events': events,
                   })


def applications_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

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
    statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]
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
            'statuses': statuses,
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
            'statuses': statuses,
            'have_project': False,
            'files': user_files,
        })


class ProfileEdit(APIView):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        statuses = [user_status.status for user_status in UserStatus.objects.filter(user=user_profile)]

        if UserProject.objects.filter(member=user_profile) != 0:
            user_project = UserProject.objects.get(member=user_profile)
            main_role = user_project.member_main_role
            second_role = user_project.member_second_role
            third_role = user_project.member_third_role

            return render(request, 'lk_edit.html', {
                'profile': user_profile,
                'statuses': statuses,
                'have_project': True,
                'main_role': main_role,
                'second_role': second_role,
                'third_role': third_role
            })

        else:
            return render(request, 'lk_edit.html', {
                'profile': user_profile,
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
