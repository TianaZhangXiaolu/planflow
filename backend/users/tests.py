import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post("/api/register/", 
                           data={
                               "username": "pytest_user",
                               "email": "pytest@example.com",
                               "password": "TestPassword"
                               }, 
                           format="json")
    assert response.status_code == 201
    assert User.objects.filter(username="pytest_user").exists()
    assert "password" not in response.data
