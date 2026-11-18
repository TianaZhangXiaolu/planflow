from django.test import TestCase
from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model
from projects.models import Project

@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_projects():
    client = APIClient()
    
    response = client.get("/api/projects/")
    
    assert response.status_code == 401

@pytest.mark.django_db
def test_user_cannot_access_other_users_proj():
    User = get_user_model()
    
    user_a = User.objects.create_user(
        username="user_a",
        password="testpassword"
    )
    user_b = User.objects.create_user(
        username="user_b",
        password="testpassword"
    )
    
    project = Project.objects.create(
        user=user_a,
        name="User A Proj",
        description="user A"
    )
    client = APIClient()
    client.force_authenticate(user=user_b)
    
    response = client.get("/api/projects/")
    
    assert response.status_code == 200
    assert response.data == []
    

@pytest.mark.django_db
def test_user_cannot_access_other_users_project_detail():
    User = get_user_model()

    user_a = User.objects.create_user(
        username="user_a",
        password="testpassword"
    )
    user_b = User.objects.create_user(
        username="user_b",
        password="testpassword"
    )

    project = Project.objects.create(
        user=user_a,
        name="User A Project",
        description="This belongs to user A"
    )

    client = APIClient()
    client.force_authenticate(user=user_b)

    response = client.get(f"/api/projects/{project.id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_authenticated_user_can_create_project():
    User = get_user_model()

    user = User.objects.create_user(
        username="test_user",
        password="testpassword"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/projects/",
        {
            "name": "My First Project",
            "description": "Testing project creation"
        },
        format="json"
    )

    assert response.status_code == 201

    project = Project.objects.get(name="My First Project")

    assert project.user == user
