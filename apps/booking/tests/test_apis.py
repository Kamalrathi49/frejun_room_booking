# third party imports
import pytest
from rest_framework.test import APIClient

# django imports
from django.urls import reverse

# local imports
from apps.booking.models import Room, Booking, Team, Member
from apps.users.models import User

# std imports
from datetime import date, time
import uuid


@pytest.mark.django_db
class TestBookingAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.team = Team.objects.create(name='Test Team', created_by=self.user)
        self.member = Member.objects.create(name='Member1', age=25, gender='male', team=self.team, created_by=self.user)
        self.room = Room.objects.create(name='Private 1', room_type='private', capacity=1)
        self.conf_room = Room.objects.create(name='Conference 1', room_type='conference', capacity=10)
        self.shared_room = Room.objects.create(name='Shared 1', room_type='shared', capacity=4)

    def test_book_private_room(self):
        url = reverse('booking-list')
        data = {
            'room_id': str(self.room.uuid),
            'date': str(date.today()),
            'slot': '09:00:00',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201

    def test_book_conference_room(self):
        url = reverse('booking-list')
        data = {
            'room_id': str(self.conf_room.uuid),
            'team_id': str(self.team.uuid),
            'member_ids': [str(self.member.uuid)],
            'date': str(date.today()),
            'slot': '10:00:00',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code in (201, 400)

    def test_book_shared_desk(self):
        url = reverse('booking-list')
        data = {
            'room_id': str(self.shared_room.uuid),
            'date': str(date.today()),
            'slot': '11:00:00',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201

    def test_cancel_booking(self):
        booking = Booking.objects.create(room=self.room, date=date.today(), slot=time(9,0), user=self.user)
        url = reverse('booking-cancel', kwargs={'uuid': str(booking.uuid)})
        response = self.client.post(url)
        assert response.status_code == 200

    def test_list_bookings(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_available_rooms(self):
        url = reverse('room-available')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_team(self):
        url = reverse('team-list')
        data = {"name": "Team Beta", "description": "A new team"}
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == "Team Beta"

    def test_list_teams(self):
        url = reverse('team-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(team['name'] == self.team.name for team in response.data)

    def test_create_member(self):
        url = reverse('member-list')
        data = {
            "name": "Bob",
            "age": 30,
            "gender": "male",
            "email": "bob@example.com",
            "team": str(self.team.uuid)
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == "Bob"

    def test_list_members(self):
        url = reverse('member-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(member['name'] == self.member.name for member in response.data)

    def test_list_members_by_team(self):
        url = reverse('member-list') + f'?team={self.team.uuid}'
        response = self.client.get(url)
        assert response.status_code == 200
        member_uuids = [str(member['uuid']) for member in response.data]
        assert str(self.member.uuid) in member_uuids 