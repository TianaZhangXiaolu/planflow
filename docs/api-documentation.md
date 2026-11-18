# API Documentation

PlanFlow provides RESTful APIs built with Django REST Framework (DRF).

The API handles user authentication, project management, and task management.

## Base URL

For local development:

```text
http://localhost:8001/api/
```

When running through Docker:

```text
http://localhost:8080/api/
```

## Authentication

PlanFlow uses JSON Web Token (JWT) authentication through Django REST Framework SimpleJWT.

Protected endpoints require an access token in the request header:

```http
Authorization: Bearer <access_token>
```

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/register/` | Register a new user | Not required |
| POST | `/api/token/` | Obtain access and refresh tokens | Not required |
| POST | `/api/token/refresh/` | Refresh an access token | Not required |

### Register a User

**Request**

```http
POST /api/register/
Content-Type: application/json
```

```json
{
  "username": "example_user",
  "password": "your_password"
}
```

### Obtain JWT Tokens

**Request**

```http
POST /api/token/
Content-Type: application/json
```

```json
{
  "username": "example_user",
  "password": "your_password"
}
```

The endpoint returns an access token and a refresh token.

### Refresh Access Token

**Request**

```http
POST /api/token/refresh/
Content-Type: application/json
```

```json
{
  "refresh": "<refresh_token>"
}
```

## Project Management

All project endpoints require JWT authentication.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/projects/` | Retrieve the current user's projects |
| POST | `/api/projects/` | Create a project |
| GET | `/api/projects/{id}/` | Retrieve a project |
| PUT | `/api/projects/{id}/` | Update a project |
| PATCH | `/api/projects/{id}/` | Partially update a project |
| DELETE | `/api/projects/{id}/` | Delete a project |

### Create a Project

**Request**

```http
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "name": "PlanFlow Development",
  "description": "Developing a full-stack application"
}
```

The project owner is assigned automatically based on the authenticated user.

### Update a Project

**Request**

```http
PATCH /api/projects/1/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "name": "Updated Project Name"
}
```

## Task Management

All task endpoints require JWT authentication.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | Retrieve the current user's tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/{id}/` | Retrieve a task |
| PUT | `/api/tasks/{id}/` | Update a task |
| PATCH | `/api/tasks/{id}/` | Partially update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

### Create a Task

**Request**

```http
POST /api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "title": "Implement API documentation",
  "project": 1,
  "category": null,
  "description": "Document the REST API endpoints",
  "is_completed": false
}
```

A task must belong to a project. Its category is optional and, when provided, must belong to the same project.

### Update Task Completion Status

**Request**

```http
PATCH /api/tasks/1/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "is_completed": true
}
```

## Authorization and Data Isolation

PlanFlow enforces user-specific data access.

- Users can only retrieve their own projects.
- Users cannot access or modify projects owned by other users.
- Users can only access tasks belonging to their own projects.
- The backend automatically associates newly created projects with the authenticated user.
- A task's category must belong to the same project as the task.

## HTTP Status Codes

| Status Code | Description |
|---|---|
| 200 OK | Request successful |
| 201 Created | Resource successfully created |
| 204 No Content | Resource successfully deleted |
| 400 Bad Request | Invalid request data |
| 401 Unauthorized | Authentication required or invalid |
| 404 Not Found | Resource does not exist or is not accessible |

## Notes

- All endpoints use JSON for request and response bodies, where applicable.
- Protected endpoints require a valid JWT access token.
- API responses and exact validation messages depend on the corresponding serializers and views.