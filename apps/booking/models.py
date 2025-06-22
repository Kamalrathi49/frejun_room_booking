# django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# local imports
from apps.core.mixins import StatusMixin, UUIDMixin, EmailMixin
from apps.users.models import User

class Room(StatusMixin, UUIDMixin):
    PRIVATE = 'private'
    CONFERENCE = 'conference'
    SHARED = 'shared'

    ROOM_TYPES = [
        (PRIVATE, "Private"),
        (CONFERENCE, "Conference"),
        (SHARED, "Shared Desk"),
    ]

    name = models.CharField(_('Room Name/No.'), max_length=50, unique=True)
    description = models.TextField(_('Description'), blank=True)
    room_type = models.CharField(_('Room Type'), max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField(_('Capacity'))

    def __str__(self):
        return f"{self.name} ({self.room_type})"


class Team(StatusMixin, UUIDMixin):
    name = models.CharField(_('Team Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        on_delete=models.SET_NULL,
        related_name='teams_created_by',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name


class Member(StatusMixin, UUIDMixin, EmailMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ]

    name = models.CharField(_('Name'), max_length=100)
    age = models.PositiveIntegerField(_('Age'), null=True, blank=True)
    gender = models.CharField(
        _('Gender'), max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    team = models.ForeignKey(
        Team,
        verbose_name=_('Team'),
        related_name='members',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        on_delete=models.SET_NULL,
        related_name='members_created_by',
        null=True,
        blank=True
    )
    
    class Meta:
        unique_together = ['name', 'email', 'team']

    def is_child(self):
        return self.age < 10

    def __str__(self):
        return f"{self.name} ({self.age})"


class Booking(StatusMixin, UUIDMixin):
    room = models.ForeignKey(
        Room,
        verbose_name=_('Room'),
        on_delete=models.SET_NULL,
        related_name='room_bookings',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        null=True,
        blank=True,
        related_name='user_bookings',
        on_delete=models.SET_NULL
    )
    team = models.ForeignKey(
        Team,
        verbose_name=_('Team'),
        null=True,
        blank=True,
        related_name='team_bookings',
        on_delete=models.SET_NULL
    )
    date = models.DateField(_('Booking Date'), null=True, blank=True)
    slot = models.TimeField(_('Booking Slot'), null=True, blank=True)

    class Meta:
        unique_together = ['room', 'date', 'slot']

    def __str__(self):
        return f"{self.room.name} — {self.date} {self.slot}"

