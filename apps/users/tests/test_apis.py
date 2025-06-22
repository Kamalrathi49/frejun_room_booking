# third party imports
import pytest
from rest_framework.test import APIClient

# django imports
from django.urls import reverse

# local imports
from apps.users.models import User

@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_user_signup(self):
        url = reverse("user-auth-signup")
        data = {
            "username": "newuser@example.com",
            "email": "newuser@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(email=data['email']).exists()

    def test_user_login(self):
        user = User.objects.create_user(username="testuser@example.com", email="testuser@example.com", password="testpassword")
        url = reverse("user-auth-login")
        data = {
            "username": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
        self.access_token = response.data['access']
        self.user = user

    def test_user_detail_and_update(self):
        user = User.objects.create_user(username="detailuser@example.com", email="detailuser@example.com", password="testpassword", first_name="Detail", last_name="User")
        self.client.force_authenticate(user=user)
        url = reverse("user-detail-update", kwargs={"uuid": user.uuid})
        # Get detail
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['email'] == user.email
        # Patch update
        data = {"first_name": "UpdatedName"}
        response = self.client.patch(url, data, format='json')
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.first_name == "UpdatedName" 