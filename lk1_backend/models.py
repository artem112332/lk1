from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    last_name = models.CharField(max_length=50)  # Фамилия
    first_name = models.CharField(max_length=50)  # Имя
    middle_name = models.CharField(max_length=50)  # Отчество
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    telegram = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    vk = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=200, null=True, blank=True)
    institute = models.CharField(max_length=200, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    year_of_study = models.CharField(max_length=4, null=True, blank=True)
    year_of_graduation = models.CharField(max_length=4, null=True, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    photo = models.ImageField(upload_to='users_photo/', blank=True, default='default_avatar.jpeg')

    def __str__(self):
        return f'{self.short_name()}'

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def first_and_last_name(self):
        return f'{self.first_name} {self.last_name}'

    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'


class UserStatus(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name='role_owner')
    status_choises = [
        ('Проектант', 'Проектант'),
        ('Куратор', 'Куратор'),
        ('Организатор', 'Организатор'),
        ('Руководитель направления', 'Руководитель направления'),
        ('Администратор', 'Администратор')
    ]
    status = models.CharField(max_length=24, choices=status_choises, default='Проектант')

    def __str__(self):
        return f'{self.user} - {self.status}'


class UserFile(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name='file_owner')
    file = models.FileField(upload_to='users_files/', default='default_avatar.jpeg')

    def __str__(self):
        return f'{self.id} {self.user} {self.file.name}'


class Skill(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name='skill_owner')
    name = models.CharField(max_length=50)
    level_choices = [
        ('Базовый', 'Базовый'),
        ('Средний', 'Средний'),
        ('Продвинутый', 'Продвинутый')
    ]
    level = models.CharField(max_length=11, choices=level_choices, default=level_choices[0])

    def __str__(self):
        return f'{self.user} {self.name}'


class Direction(models.Model):
    director = models.ForeignKey(UserProfile, models.SET_NULL, related_name='direction_director', null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
    tutor = models.ForeignKey(UserProfile, models.SET_NULL, related_name='project_tutor', null=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    direction = models.ForeignKey(Direction, models.SET_NULL, related_name="project_direction", null=True)

    def __str__(self):
        return f'{self.name}'


class UserProject(models.Model):
    project = models.ForeignKey(Project, models.SET_NULL, related_name='teams_project', null=True, blank=True)
    member = models.ForeignKey(UserProfile, models.SET_NULL, null=True, related_name='project_member')
    # role_choices = [
    #     ('Backend-разработчик', 'Backend-разработчик'),
    #     ('Frontend-разработчик', 'Frontend-разработчик'),
    #     ('Аналитик', 'Аналитик'),
    #     ('Дизайнер', 'Дизайнер'),
    #     ('Тимлид', 'Тимлид')
    # ]
    member_main_role = models.CharField(max_length=50, null=True, blank=True)
    member_second_role = models.CharField(max_length=50, null=True, blank=True)
    member_third_role = models.CharField(max_length=50, null=True, blank=True)
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.member} {self.member_main_role},{self.member_second_role},{self.member_third_role} {self.team_name} {self.project}'


class Meeting(models.Model):
    name = models.CharField(max_length=200)
    status_choices = [
        ('Анонсировано', 'Анонсировано'),
        ('Началось', 'Началось'),
        ('Закончилось', 'Закончилось')
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}, {self.team_name}'

    def set_started(self):
        self.status = self.status_choices[1]
        self.save()

    def set_ended(self):
        self.status = self.status_choices[2]
        self.save()


class MeetingTeam(models.Model):
    meeting = models.ForeignKey(Meeting, models.CASCADE, related_name='team_meeting')
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.team_name}'


class UserMeeting(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name='user_in_meeting')
    meeting = models.ForeignKey(Meeting, models.CASCADE, related_name='users_meeting')

    def __str__(self):
        return f'{self.user} - {self.meeting.name}'


class Event(models.Model):
    name = models.CharField(max_length=200)
    organizer = models.ForeignKey(UserProfile, models.SET_NULL, related_name='event_organizer', null=True)
    description = models.TextField(max_length=2000, blank=True)
    status_choices = [
        ('Анонсировано', 'Анонсировано'),
        ('Началось', 'Началось'),
        ('Закончилось', 'Закончилось')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default=status_choices[0])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    number_of_participants = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name}'

    def set_started(self):
        self.status = self.status_choices[1]
        self.save()

    def set_ended(self):
        self.status = self.status_choices[2]
        self.save()


class UserEvent(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name='event_participant')
    event = models.ForeignKey(Event, models.CASCADE, related_name='users_event')

    def __str__(self):
        return f'{self.user} - {self.event}'


class EventDirection(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, related_name='event')
    direction = models.ForeignKey(Direction, models.CASCADE, related_name='event_direction')

    def __str__(self):
        return f'{self.event} - {self.direction}'


class ApllictationToEvent(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, related_name='application_event')
    sender = models.ForeignKey(UserProfile, models.CASCADE, related_name='event_apllication_sender')
    status_choices = [
        ('На рассмотрении', 'На рассмотрении'),
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    send_date = models.DateField()

    def __str__(self):
        return f'Заявка {self.sender} на {self.event.name} - {self.status}'

    def set_accepted(self):
        self.status = self.status_choices[1]
        self.save()

    def set_rejected(self):
        self.status = self.status_choices[2]
        self.save()


class ApllictationToProject(models.Model):
    project = models.ForeignKey(Project, models.CASCADE, related_name='event')
    sender = models.ForeignKey(UserProfile, models.CASCADE, related_name='project_apllication_sender')
    status_choices = [
        ('На рассмотрении', 'На рассмотрении'),
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    send_date = models.DateField()

    def __str__(self):
        return f'Заявка {self.sender} на {self.project.name} - {self.status}'

    def set_accepted(self):
        self.status = self.status_choices[1]
        self.save()

    def set_rejected(self):
        self.status = self.status_choices[2]
        self.save()
