from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lk1_backend.models import UserProfile, UserStatus, UserProject, Project
from rest_framework.views import APIView
from lk1_backend.views import index


def index_login(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        return index(request)
    else:
        return redirect('login')


class Login(APIView):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index_login')
        else:
            return render(request, 'login.html', {'invalid': True})

    def get(self, request):
        return render(request, 'login.html', {'invalid': False})


def user_logout(request):
    logout(request)
    return redirect('login')


class Register(APIView):
    def get(self, request):
        return render(request, 'registration.html', {
            'username_taken': False,
            'short_password': False,
            'invalid_full_name': False
        })

    def post(self, request):
        username = request.POST['login']
        password = request.POST['password']
        full_name = request.POST['full_name'].split()
        existing_user = User.objects.filter(username=username)

        if len(existing_user) == 0 and len(password) >= 8 and len(full_name) == 3:
            user = User.objects.create_user(username, '', password)
            login(request, user)

            last_name = full_name[0]
            first_name = full_name[1]
            middle_name = full_name[2]

            user_profile = UserProfile.objects.create(
                user=user,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
            )

            UserStatus.objects.create(user=user_profile)

            # проект заглушка
            project = Project.objects.create()
            project.name = f'Проект №{project.id}'
            project.save()

            UserProject.objects.create(project=project, member=user_profile)

            return redirect('index_login')

        return render(request, 'registration.html', {
            'username_taken': len(existing_user) != 0,
            'short_password': len(password) < 8,
            'invalid_full_name': len(full_name) != 3
        })
