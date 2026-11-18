
# System Architecture

PlanFlow follows a client-server architecture with a Vue.js frontend, a Django REST Framework backend, and a PostgreSQL database.

## Architecture Diagram

```mermaid
flowchart TB
    User["User / Web Browser"]

    subgraph Docker["Docker Compose"]
        Nginx["Nginx<br/>Frontend Server & Reverse Proxy"]
        Vue["Vue 3 + TypeScript<br/>Frontend Application"]
        Backend["Django REST Framework<br/>Gunicorn"]
        DB[("PostgreSQL Database")]

        Nginx -->|"Serves static files"| Vue
        Nginx -->|"/api/ requests"| Backend
        Backend -->|"SQL queries"| DB
    end

    User -->|"HTTP"| Nginx
    User -.->|"Uses application"| Vue

    JWT["JWT Authentication"]
    JWT -.-> Backend
